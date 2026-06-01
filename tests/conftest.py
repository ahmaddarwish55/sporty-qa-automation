import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from api.client import SportyApiClient  # Import our new API Object Model
import json
import config  # Import the central config


@pytest.fixture(scope="session")
def app_config():
    """Provides global configuration variables to UI tests."""
    return {
        "base_url": config.BASE_URL,
        "user_id": config.USER_ID
    }

@pytest.fixture(scope="function")
def driver():
    """Sets up the Selenium Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")   
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10) 
    yield driver  
    driver.quit()

@pytest.fixture(scope="session")
def api_client():
    """
    Instantiates the API client once per test session and 
    provides it to any test that requests it.
    """
    return SportyApiClient(base_url=config.BASE_URL, user_id=config.USER_ID)

@pytest.fixture(scope="session")
def test_data():
    """
    Loads the external JSON file containing all test data.
    Makes it available to any test that requests it.
    """
    with open("data/test_data.json", "r") as file:
        return json.load(file)