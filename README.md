FormFlow – Google Form Automation Toolkit
==========================================

Automate Google Forms with reCAPTCHA v2 solving, multi-account support, and human-like interaction. Built for **authorized security testing**, accessibility research, and educational exploration.

⚠️ Use only on forms you own or have explicit written permission to test.

---

What it does
------------

- Solves reCAPTCHA v2 audio challenges automatically (speech-to-text)
- Rotates between multiple Google accounts using saved cookies (no passwords stored)
- Supports HTTP/HTTPS proxies with automatic health checking
- Fills "Name" fields from a custom list of real names
- Randomises browser fingerprint, disables WebRTC, types like a human
- Detects already-solved captchas to save time
- Modular design – easy to extend

---

Repository structure
--------------------

FormFlow/
├── main.py                  # entry point
├── save_cookies.py          # export Google session cookies
├── config.py                # all user settings
├── names.txt                # list of real names (one per line)
├── proxies.txt              # proxies (optional)
├── requirements.txt         # Python dependencies
├── cookies/                 # saved .pkl cookie files
├── recaptcha_bypass/        # GoogleRecaptchaBypass (submodule)
└── utils/
    ├── captcha_solver.py
    ├── fingerprint.py
    ├── proxy_manager.py
    └── humanize.py

---

Quick start
-----------

1. Clone the repo and install dependencies

   git clone https://github.com/aidilimangg-lgtm/FormFlow.git
   cd FormFlow
   git clone https://github.com/sarperavci/GoogleRecaptchaBypass.git recaptcha_bypass
   pip install -r requirements.txt
   pip install -r recaptcha_bypass/requirements.txt

2. Export cookies for your test Google accounts

   python save_cookies.py --account test_acc1

   (repeat for each account)

3. Add your data

   - Edit names.txt with one full name per line.
   - (Optional) Add proxies to proxies.txt (one per line).

4. Configure the form

   Open config.py and set the FORM_URL to your target form.
   Adjust SUBMISSIONS_PER_ACCOUNT, delays, etc.

5. Run the tool

   python main.py

   Or override with command line arguments:
   python main.py --url "https://forms.gle/..." --count 10 --delay-min 2 --delay-max 5

---

Configuration
-------------

Edit config.py or pass arguments:

  FORM_URL               – Google Form URL
  SUBMISSIONS_PER_ACCOUNT – forms each account submits
  DELAY_MIN / DELAY_MAX  – random wait between submissions (seconds)
  ACCOUNT_COOLDOWN_MIN / MAX – wait between switching accounts
  PROXY_FILE             – path to proxy list
  NAMES_FILE             – path to name list
  COOKIES_DIR            – folder containing .pkl cookie files
  CAPTCHA_TIMEOUT        – max seconds to solve a captcha
  HEADLESS               – True to run without visible browser

---

How it works
------------

1. The script loads a saved Google session (cookies) for an account.
2. It opens the form, solves the reCAPTCHA v2 (audio challenge).
3. Fills the "Name" field with a random line from names.txt.
4. Fills all other text fields with random sentences, and picks random choices for multiple‑choice questions.
5. Submits the form and checks for the confirmation message.
6. Waits a random interval, then reloads the form. If the captcha is still green it skips re‑solving.
7. After reaching the submission limit for that account, it switches to the next account and proxy, with a cooldown.

---

Running on Kali Linux (VM)
--------------------------

For anonymity:

- Use a fresh Kali VM snapshot.
- Install required packages: sudo apt install python3-pip ffmpeg
- Before each run, randomise MAC address: sudo macchanger -r eth0
- Consider using a VPN inside the VM instead of proxy lists.
- After the run, revert the VM to its clean snapshot – no traces remain.

---

Ethical use
-----------

This tool is intended for:

- Security researchers testing their own Google Forms
- Educational demonstrations of web automation and captcha solving
- Penetration testing with explicit permission

Do not use it on forms you do not own or have not been authorised to test.

---

Dependencies
------------

All Python dependencies are listed in requirements.txt:

  undetected-chromedriver
  selenium
  fake-useragent
  faker
  pydub
  SpeechRecognition
  requests
  colorama

Also install the dependencies of the recaptcha_bypass submodule.

---

Contributing
------------

Pull requests are welcome. Please open an issue first to discuss any changes.

---

License
-------

MIT License – see LICENSE file.

---

Acknowledgements
----------------

- GoogleRecaptchaBypass (https://github.com/sarperavci/GoogleRecaptchaBypass) – the audio captcha solver.
- undetected-chromedriver (https://github.com/ultrafunkamsterdam/undetected-chromedriver) – for stealth browser automation.

---

Built by aidilimangg-lgtm.
Stay curious, stay ethical.
