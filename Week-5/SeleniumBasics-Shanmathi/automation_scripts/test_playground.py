import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")
    message_input = driver.find_element(By.ID, "user-message")
    message_input.clear()
    message_input.send_keys(message)
    driver.find_element(By.ID, "showInput").click()
    displayed = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed.text == message


def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo")
    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[type='checkbox']:not([disabled])")
        )
    )
    if not checkbox.is_selected():
        checkbox.click()
    assert checkbox.is_selected()
    checkbox.click()
    assert not checkbox.is_selected()


def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo")
    dropdown_element = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_element)
    select.select_by_visible_text("Wednesday")
    assert select.first_selected_option.text == "Wednesday"
