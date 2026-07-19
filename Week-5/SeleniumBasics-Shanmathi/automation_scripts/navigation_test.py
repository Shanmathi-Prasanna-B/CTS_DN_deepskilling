import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"
SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "playground_screenshot.png")


def create_driver():
    options = Options()
    options.add_argument("--window-size=1280,800")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def run_navigation_test():
    driver = create_driver()
    try:
        driver.get(BASE_URL)

        driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
        assert "simple-form-demo" in driver.current_url

        driver.back()

        driver.execute_script('window.open("https://www.google.com");')
        handles = driver.window_handles
        print(f"Open tabs: {handles}")

        driver.switch_to.window(handles[1])
        print(f"Google tab title: {driver.title}")

        driver.switch_to.window(handles[0])

        size = driver.get_window_size()
        print(f"Original window size: {size}")

        driver.set_window_size(1280, 800)
        # Consistent window size matters for responsive UI automation because
        # viewport dimensions control which elements are visible, how they are
        # laid out, and whether breakpoints trigger different DOM structures.
        # Fixed size ensures screenshots and locators behave identically every run.

        driver.save_screenshot(SCREENSHOT_PATH)
        print(f"Screenshot saved: {SCREENSHOT_PATH}")
        assert os.path.exists(SCREENSHOT_PATH)
    finally:
        driver.quit()


if __name__ == "__main__":
    run_navigation_test()
