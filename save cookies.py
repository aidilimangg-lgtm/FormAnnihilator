import pickle
import undetected_chromedriver as uc
import argparse
import os

parser = argparse.ArgumentParser(description="Export Google session cookies.")
parser.add_argument("--account", required=True, help="Account name (e.g., acc1)")
args = parser.parse_args()

driver = uc.Chrome()
driver.get("https://accounts.google.com/signin")
input(f"Log into account '{args.account}' manually, then press Enter...")

os.makedirs("cookies", exist_ok=True)
cookies_path = f"cookies/{args.account}.pkl"
with open(cookies_path, "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print(f"Cookies saved to {cookies_path}")
driver.quit()
