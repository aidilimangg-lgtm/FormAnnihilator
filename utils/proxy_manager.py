import requests

def load_proxies(filepath="proxies.txt"):
    if not filepath or not isinstance(filepath, str):
        return []
    try:
        with open(filepath) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("[!] Proxy file not found, running without proxies.")
        return []

def test_proxy(proxy, timeout=5):
    try:
        r = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=timeout)
        return r.status_code == 200
    except:
        return False

def get_working_proxies(count=5, filepath="proxies.txt"):
    raw = load_proxies(filepath)
    working = []
    for p in raw:
        if test_proxy(p):
            working.append(p)
        if len(working) >= count:
            break
    return working
