# FormAnnihator

Multi-account Google Form spammer with **reCAPTCHA v2 audio bypass**,
**proxy rotation**, and **human‑like behavior**.

> Built by **aidilimangg-lgtm** – break barriers responsibly.

🔒 *Educational use only – only on forms you own or have explicit permission to test.*

## Features

- ✅ **reCAPTCHA v2 bypass** – audio challenge solving using [GoogleRecaptchaBypass](https://github.com/sarperavci/GoogleRecaptchaBypass)
- ✅ **Multi-account support** – load Google session cookies, no password needed
- ✅ **Proxy rotation** – HTTP/HTTPS proxies from file, with automatic testing
- ✅ **Custom name injection** – uses a real name list (`names.txt`)
- ✅ **Stealth mode** – randomized fingerprints, human‑like delays, WebRTC/DNS leak prevention
- ✅ **VM‑ready** – designed for Kali Linux snapshots & anonymity
- ✅ **Headless capable** – can run without a display

## Quick Start

### 1. Clone & install
```bash
git clone https://github.com/aidilimangg-lgtm/FormAnnihilator.git
cd FormAnnihilator
git clone https://github.com/sarperavci/GoogleRecaptchaBypass.git recaptcha_bypass
pip install -r requirements.txt
