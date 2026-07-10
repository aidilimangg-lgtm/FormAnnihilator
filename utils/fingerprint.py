import random
import undetected_chromedriver as uc

def apply_stealth(driver):
    # Disable WebRTC to prevent IP leak
    driver.execute_cdp_cmd("Network.setWebRTCIPHandlingPolicy", {"policy": "disable_non_proxied_udp"})
    # Override navigator properties
    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    """)
    # Randomize screen resolution slightly
    width = random.choice([1366, 1440, 1536, 1600, 1920])
    height = random.choice([768, 900, 864, 900, 1080])
    driver.set_window_size(width, height)

def get_stealth_driver(proxy=None, headless=False):
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
    options.add_argument("--dns-prefetch-disable")
    if headless:
        options.add_argument("--headless=new")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    driver = uc.Chrome(options=options, use_subprocess=True)
    apply_stealth(driver)
    return driver
