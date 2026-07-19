from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SIMPLE_FORM_URL = "https://www.lambdatest.com/selenium-playground/simple-form-demo"
CHECKBOX_URL = "https://www.lambdatest.com/selenium-playground/checkbox-demo"


def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,800")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def _verify_message_input(element):
    assert element.get_attribute("id") == "user-message"
    assert element.is_displayed()


def demonstrate_locators():
    driver = create_driver()
    try:
        driver.get(SIMPLE_FORM_URL)

        # 1. By.ID
        _verify_message_input(driver.find_element(By.ID, "user-message"))

        # 2. By.NAME
        _verify_message_input(driver.find_element(By.NAME, "user-message"))

        # 3. By.CLASS_NAME
        message_input = next(
            el for el in driver.find_elements(By.CLASS_NAME, "form-control")
            if el.get_attribute("id") == "user-message"
        )
        _verify_message_input(message_input)

        # 4. By.TAG_NAME — locate the input tag
        message_input = next(
            el for el in driver.find_elements(By.TAG_NAME, "input")
            if el.get_attribute("id") == "user-message"
        )
        _verify_message_input(message_input)

        # 5. By.XPATH — absolute path
        _verify_message_input(
            driver.find_element(
                By.XPATH,
                "/html/body/div/div/main/div/section[2]/div/div/div/div/div[2]/div/div/input",
            )
        )

        # 6. By.XPATH — relative path using attributes
        _verify_message_input(
            driver.find_element(By.XPATH, "//input[@id='user-message']")
        )

        # CSS Selector 1: by ID (#id)
        _verify_message_input(driver.find_element(By.CSS_SELECTOR, "#user-message"))

        # CSS Selector 2: by attribute ([name='value'])
        _verify_message_input(
            driver.find_element(By.CSS_SELECTOR, "input[id='user-message']")
        )

        # CSS Selector 3: parent-child relationship (div > input)
        _verify_message_input(
            driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
        )

        driver.get(CHECKBOX_URL)

        option_one_label = driver.find_element(
            By.XPATH, "//label[text()='Option 1']"
        )
        assert option_one_label.is_displayed()
        print(f"Option 1 label found: {option_one_label.text}")

        option_labels = driver.find_elements(
            By.XPATH, "//label[contains(text(),'Option')]"
        )
        print(f"Found {len(option_labels)} option labels via contains()")
        for label in option_labels:
            print(f"  Label text: {label.text.strip()}")

        # Locator ranking (most to least preferred for maintainable automation):
        # 1. ID          — unique, fast, highly readable
        # 2. NAME        — stable when IDs are absent or dynamic
        # 3. CSS_SELECTOR — concise, performant, handles attribute/class patterns
        # 4. CLASS_NAME  — usable when the class uniquely identifies the element
        # 5. XPATH (relative) — needed for text/axis traversal CSS cannot express
        # 6. TAG_NAME / XPATH (absolute) — brittle; break on any DOM restructure

        print("All locator strategies verified successfully.")
    finally:
        driver.quit()


if __name__ == "__main__":
    demonstrate_locators()
