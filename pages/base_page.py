import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config  # Import our new central config

class BasePage:
    """
    The foundational page object. 
    Contains generic methods for interacting with the browser securely.
    """
    def __init__(self, driver):
        self.driver = driver
        # Now your explicit wait is globally configurable too!
        self.wait = WebDriverWait(self.driver, config.EXPLICIT_WAIT_TIMEOUT)

    # ... (Keep all your existing navigate, find, click, type_text, get_text, extract_number methods) ...

    def pause(self, seconds=config.UI_SYNC_PAUSE):
        """
        A hard pause to allow backend syncs. 
        Defaults to the global UI_SYNC_PAUSE, but can be overridden per call.
        """
        time.sleep(seconds)

    def navigate(self, url):
        self.driver.get(url)

    def find(self, locator):
        """Waits for an element to be visible, then returns it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Waits for an element to be clickable, then clicks it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text):
        """Waits, clears the input field, and types the given text."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Waits and retrieves the text from an element."""
        return self.find(locator).text
    
    # --- ABSTRACT UTILITIES ---
    
    def extract_number(self, text_string):
        """Globally extracts decimals from UI strings (e.g., '€90.00' -> 90.0)"""
        match = re.search(r"[\d\.]+", text_string)
        return float(match.group(0)) if match else 0.0

 