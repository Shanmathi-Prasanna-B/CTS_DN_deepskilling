import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import FluentWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ALERTS_URL = "https://www.lambdatest.com/selenium-playground/bootstrap-alert"
TABLE_URL = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"


def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,800")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def test_explicit_wait_alert():
    driver = create_driver()
    try:
        driver.get(ALERTS_URL)
        driver.find_element(By.ID, "successButton").click()
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert.text.lower()
        print(f"Alert text: {alert.text}")
    finally:
        driver.quit()


def compare_sleep_vs_explicit():
    driver = create_driver()
    try:
        driver.get(ALERTS_URL)
        start = time.time()
        driver.find_element(By.ID, "successButton").click()
        time.sleep(3)
        alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        sleep_duration = time.time() - start
        print(f"time.sleep(3) approach took: {sleep_duration:.2f}s")
        assert "successfully" in alert.text.lower()
    finally:
        driver.quit()

    driver = create_driver()
    try:
        driver.get(ALERTS_URL)
        start = time.time()
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "successButton"))
        )
        btn.click()
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        explicit_duration = time.time() - start
        print(f"Explicit wait approach took: {explicit_duration:.2f}s")
        # Explicit wait returns as soon as the condition is met — faster on fast
        # machines. time.sleep(3) always waits the full 3 seconds regardless, and
        # can still fail on slow machines if the alert needs longer than 3 seconds.
        assert "successfully" in alert.text.lower()
    finally:
        driver.quit()


def test_clickable_vs_visible():
    driver = create_driver()
    try:
        driver.get(ALERTS_URL)
        # element_to_be_clickable: visible AND enabled AND not obscured by another element.
        # visibility_of_element_located: present in DOM and visible, but may still be disabled.
        success_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "successButton"))
        )
        success_btn.click()
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert.text.lower()
        print("Clickable wait + visibility wait demonstrated.")
    finally:
        driver.quit()


def test_fluent_wait_table():
    driver = create_driver()
    try:
        driver.get(TABLE_URL)
        fluent_wait = FluentWait(driver, timeout=10, poll_frequency=0.5)
        fluent_wait = fluent_wait.ignoring(NoSuchElementException)
        rows = fluent_wait.until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "#table tbody tr")
        )
        assert len(rows) > 0
        print(f"Table loaded with {len(rows)} rows via FluentWait polling.")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_explicit_wait_alert()
    compare_sleep_vs_explicit()
    test_clickable_vs_visible()
    test_fluent_wait_table()
