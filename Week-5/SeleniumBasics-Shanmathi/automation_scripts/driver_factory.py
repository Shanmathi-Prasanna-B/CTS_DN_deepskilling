from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_service():
    return Service(ChromeDriverManager().install())
