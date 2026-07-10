import time
import random

def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def human_typing(element, text, min_delay=0.05, max_delay=0.15):
    """Type character by character with slight delays."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))
