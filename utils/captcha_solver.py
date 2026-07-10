import sys
# The cloned recaptcha_bypass folder should be on the path
sys.path.append("recaptcha_bypass")
from recaptcha_solver import RecaptchaSolver

def solve_captcha(driver, timeout=60):
    """Solve reCAPTCHA v2 audio challenge."""
    solver = RecaptchaSolver(driver)
    solver.solve_captcha()
    return True
