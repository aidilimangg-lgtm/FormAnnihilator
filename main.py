#!/usr/bin/env python3
"""
FormFlow – Google Form Automation Toolkit
Main entry point.
"""

import os
import sys
import pickle
import random
import time
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import *
from utils.proxy_manager import load_proxies
from utils.fingerprint import get_stealth_driver
from utils.captcha_solver import solve_captcha
from utils.humanize import human_delay, human_typing

fake = Faker()

def load_names():
    if not NAMES_FILE or not os.path.exists(NAMES_FILE):
        return []
    with open(NAMES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_cookies(driver, cookies_file):
    driver.get("https://accounts.google.com")
    with open(cookies_file, 'rb') as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    print(f"[+] Loaded {len(cookies)} cookies from {cookies_file}")

def fill_name(driver, name_list):
    if not name_list:
        return False
    questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
    for q in questions:
        try:
            title_elem = q.find_element(By.CSS_SELECTOR, "div[role='heading']")
            title = title_elem.text.lower()
            if "name" in title or "full name" in title or "your name" in title:
                input_elem = q.find_element(By.CSS_SELECTOR, "input[type='text'], textarea")
                if input_elem.is_displayed() and input_elem.is_enabled():
                    chosen = random.choice(name_list)
                    human_typing(input_elem, chosen)
                    print(f"[+] Filled name: {chosen}")
                    return True
        except:
            continue
    # Fallback: first text input
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
    for inp in inputs:
        if inp.is_displayed() and inp.is_enabled():
            human_typing(inp, random.choice(name_list))
            return True
    return False

def fill_remaining_fields(driver):
    # Text inputs
    all_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
    for elem in all_inputs:
        if elem.is_displayed() and elem.is_enabled() and elem.get_attribute("value") == "":
            human_typing(elem, fake.sentence())
    # Multiple choice (radio groups)
    mc_containers = driver.find_elements(By.CSS_SELECTOR, "[role='radiogroup']")
    for group in mc_containers:
        options = group.find_elements(By.CSS_SELECTOR, "[role='radio']")
        if options:
            choice = random.choice(options)
            driver.execute_script("arguments[0].click();", choice)
            human_delay(0.2, 0.5)

def submit_form(driver):
    submit_btn = driver.find_element(By.XPATH, "//div[@role='button' and .//span[text()='Submit']]")
    driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
    human_delay(0.5, 1.0)
    submit_btn.click()
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'response has been recorded')]"))
        )
        print("[+] Submission confirmed.")
        return True
    except TimeoutException:
        print("[-] No confirmation message. Submission may have failed.")
        return False

def run_account(cookies_file, proxy, submissions):
    name_list = load_names()
    driver = get_stealth_driver(proxy=proxy, headless=HEADLESS)
    try:
        load_cookies(driver, cookies_file)
        driver.get(FORM_URL)
        human_delay(1, 3)

        print("[*] Solving initial captcha...")
        solve_captcha(driver, timeout=CAPTCHA_TIMEOUT)

        success = 0
        for i in range(submissions):
            print(f"[*] Submission {i+1}/{submissions}")
            driver.get(FORM_URL)
            human_delay(1, 2)

            # Check if captcha still green
            try:
                driver.switch_to.default_content()
                iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
                driver.switch_to.frame(iframe)
                driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-checked")
                driver.switch_to.default_content()
                print("[*] Captcha still green.")
            except NoSuchElementException:
                driver.switch_to.default_content()
                print("[!] Captcha expired, re-solving...")
                solve_captcha(driver, timeout=CAPTCHA_TIMEOUT)

            if name_list:
                fill_name(driver, name_list)
            fill_remaining_fields(driver)

            if submit_form(driver):
                success += 1

            human_delay(DELAY_MIN, DELAY_MAX)
        return success
    finally:
        driver.quit()

def main():
    proxies = load_proxies(PROXY_FILE)
    if not proxies:
        print("[!] No proxies found. Running without proxy (risk of IP ban).")
        proxies = [None]

    cookie_files = []
    if os.path.exists(COOKIES_DIR):
        for f in os.listdir(COOKIES_DIR):
            if f.endswith('.pkl'):
                cookie_files.append(os.path.join(COOKIES_DIR, f))
    if not cookie_files:
        print("[!] No cookie files found. Run save_cookies.py first.")
        sys.exit(1)

    print(f"[*] Loaded {len(cookie_files)} accounts and {len(proxies)} proxies.")
    total_success = 0

    for idx, cookies_file in enumerate(cookie_files):
        proxy = proxies[idx % len(proxies)] if proxies[idx % len(proxies)] else None
        print(f"\n--- Account {idx+1}: {os.path.basename(cookies_file)} (proxy {proxy}) ---")
        try:
            success = run_account(cookies_file, proxy, SUBMISSIONS_PER_ACCOUNT)
            total_success += success
        except Exception as e:
            print(f"[-] Account failed: {e}")
        human_delay(ACCOUNT_COOLDOWN_MIN, ACCOUNT_COOLDOWN_MAX)

    print(f"\n[✔] Campaign complete. Total successful submissions: {total_success}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="FormFlow – Google Form Automation Toolkit")
    parser.add_argument("--url", help="Google Form URL")
    parser.add_argument("--count", type=int, help="Submissions per account")
    parser.add_argument("--delay-min", type=float, help="Minimum delay between submissions")
    parser.add_argument("--delay-max", type=float, help="Maximum delay between submissions")
    args = parser.parse_args()

    if args.url: FORM_URL = args.url
    if args.count: SUBMISSIONS_PER_ACCOUNT = args.count
    if args.delay_min: DELAY_MIN = args.delay_min
    if args.delay_max: DELAY_MAX = args.delay_max

    main()
