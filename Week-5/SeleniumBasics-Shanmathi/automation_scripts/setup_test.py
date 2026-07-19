"""
Selenium Architecture — Three Main Components:

1. WebDriver:
   A language-specific API (Python, Java, etc.) that sends commands to the browser
   through a browser-specific driver (e.g. ChromeDriver). Communication uses the
   W3C WebDriver protocol — your script issues commands like click(), send_keys(),
   and get() which the driver translates into browser actions.

2. Selenium Grid:
   Solves parallel test execution across multiple machines, browsers, and OS
   combinations. A Hub receives test requests and routes them to registered Nodes,
   each running a specific browser — enabling cross-browser CI pipelines at scale.

3. Selenium IDE:
   A browser extension for record-and-playback of user interactions. Used for quick
   prototyping, exploratory testing, and generating starter test code — not suited
   for production-grade test suites that require maintainability and version control.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    # Implicit wait applies globally to every find_element call, slowing each lookup
    # by up to the timeout even when elements are already present. Explicit waits
    # (Hands-On 5) target a specific element and condition, making tests faster
    # and more reliable — especially on pages with mixed load times.
    driver.implicitly_wait(10)
    return driver


def run_basic_setup():
    driver = create_driver(headless=False)
    try:
        driver.get(BASE_URL)
        print(f"Page title: {driver.title}")
    finally:
        driver.quit()


def run_headless_setup():
    driver = create_driver(headless=True)
    try:
        driver.get(BASE_URL)
        print(f"Headless page title: {driver.title}")
    finally:
        driver.quit()


if __name__ == "__main__":
    run_basic_setup()
    run_headless_setup()
