

# FormFlow – Google Form Automation Toolkit

Automate Google Forms with reCAPTCHA v2 solving, multi‑account support, and human‑like interaction.  
Built for **authorized security testing**, accessibility research, and educational exploration.

⚠️ **Use only on forms you own or have explicit written permission to test.**

---

## ✨ Features

- **reCAPTCHA v2 Audio Bypass** – solves audio challenges using speech‑to‑text ([GoogleRecaptchaBypass](https://github.com/sarperavci/GoogleRecaptchaBypass))
- **Multi‑Account Rotation** – loads Google sessions from saved cookies (no passwords stored)
- **Proxy Support** – HTTP/HTTPS proxy list with automatic health checking
- **Real Name Injection** – fills the “Name” field from a custom `names.txt` file
- **Stealth Engine** – WebRTC leak prevention, navigator spoofing, random screen resolutions, human‑like typing delays
- **Smart Captcha Detection** – skips re‑solving when the token is still valid
- **Modular Design** – easily extend with new captcha solvers or field fillers
- **VM Ready** – built for Kali Linux snapshots and disposable environments

---

## 📁 Repository Structure

```

FormFlow/
├── main.py                  # entry point / orchestrator
├── save_cookies.py          # export Google session cookies
├── config.py                # all user‑configurable settings
├── names.txt                # real name list (one per line)
├── proxies.txt              # HTTP proxies (optional)
├── requirements.txt         # Python dependencies
├── cookies/                 # saved .pkl cookie files
├── recaptcha_bypass/        # GoogleRecaptchaBypass submodule
└── utils/
├── captcha_solver.py
├── fingerprint.py
├── proxy_manager.py
└── humanize.py

```

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/aidilimangg-lgtm/FormFlow.git
cd FormFlow
git clone https://github.com/sarperavci/GoogleRecaptchaBypass.git recaptcha_bypass
pip install -r requirements.txt
pip install -r recaptcha_bypass/requirements.txt
```

2. Export Google Account Cookies

· Open a normal Chrome window and log into a Google test account.
· Run the cookie exporter:

```bash
python save_cookies.py --account test_acc1
```

· Repeat for each additional account. Cookies are saved to cookies/test_acc1.pkl.

3. Prepare Data Files

· names.txt – add one full name per line (used for the “Name” field).
· proxies.txt (optional) – add proxies in the format http://ip:port or http://user:pass@ip:port.

4. Configure the Target Form

Edit config.py:

```python
FORM_URL = "https://docs.google.com/forms/d/e/.../viewform"
SUBMISSIONS_PER_ACCOUNT = 5   # forms each account submits
DELAY_MIN = 3                 # minimum seconds between submissions
DELAY_MAX = 8                 # maximum seconds
```

5. Run the Tool

```bash
python main.py
```

Or override settings via command‑line:

```bash
python main.py --url "https://forms.gle/..." --count 10 --delay-min 2 --delay-max 5
```

---

⚙️ Configuration Reference

All options can be set in config.py or passed as command‑line arguments.

Parameter Description Default
FORM_URL Target Google Form URL –
SUBMISSIONS_PER_ACCOUNT How many times each account submits 5
DELAY_MIN / DELAY_MAX Random wait between submissions (seconds) 3 / 8
ACCOUNT_COOLDOWN_MIN / MAX Wait between switching accounts 10 / 20
PROXY_FILE Path to proxy list file proxies.txt
NAMES_FILE Path to name list file names.txt
COOKIES_DIR Folder containing .pkl cookie files cookies
CAPTCHA_TIMEOUT Max seconds to solve a captcha 60
HEADLESS Run Chrome without a GUI (not recommended) False

Command‑line arguments:

```
--url, --count, --delay-min, --delay-max
```

---

🧠 How It Works

1. The script loads a saved Google session (cookies) for an account.
2. It opens the target form and solves the reCAPTCHA v2 (audio challenge if needed).
3. The “Name” field is filled with a random line from names.txt.
4. All other text fields are filled with random sentences; multiple‑choice questions get a random option.
5. The form is submitted, and the confirmation page is verified.
6. After a random delay, the form is reloaded. If the captcha is still solved, it skips the solver.
7. Once the account reaches its submission limit, the next account and proxy are used, with a cooldown.

---

🛡️ Running on Kali Linux (VM)

For maximum anonymity and ease of cleanup:

```bash
# Inside a fresh Kali VM
sudo apt install python3-pip ffmpeg
git clone https://github.com/aidilimangg-lgtm/FormFlow.git
cd FormFlow
# ... install dependencies as above ...

# Randomize MAC address before each run
sudo macchanger -r eth0

# Optionally, use a VPN instead of proxies
# Then run the tool
python main.py
```

· Take a snapshot before running. Revert to it after – zero traces.
· The script already disables WebRTC and DNS prefetch to prevent IP leaks.
· A fresh browser fingerprint is generated for each session.

---

❗ Ethical Use

This tool is intended for:

· Security researchers testing their own Google Forms
· Educational demonstrations of web automation & captcha solving
· Penetration testing with explicit permission

Do not use it on forms you do not own or have not been authorised to test.
Violating Google’s Terms of Service may result in account suspension or legal action.

---

📦 Dependencies

· undetected-chromedriver – stealth Chrome driver
· selenium – browser automation
· fake-useragent – random user agents
· faker – fake data generation
· pydub – audio processing for captcha solving
· SpeechRecognition – speech‑to‑text
· requests – HTTP requests
· colorama – coloured terminal output

Install with:

```bash
pip install -r requirements.txt
pip install -r recaptcha_bypass/requirements.txt
```

---

🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss what you’d like to change.

---

📜 License

MIT License – see the LICENSE file.

---

🙏 Acknowledgements

· GoogleRecaptchaBypass by sarperavci – the audio captcha solver.
· undetected-chromedriver – stealth browser automation.

---

Built by aidilimangg-lgtm.
Stay curious, stay ethical. 🐾


