from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOX = (By.XPATH, "(//input[@type='checkbox' and not(@disabled)])[{}]")

    def _locator_for_index(self, index):
        return (By.XPATH, self.CHECKBOX[1].format(index + 1))

    def check_option(self, index=0):
        checkbox = self.wait_for_clickable(self._locator_for_index(index))
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, index=0):
        checkbox = self.wait_for_clickable(self._locator_for_index(index))
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index=0):
        return self.wait_for_element(self._locator_for_index(index)).is_selected()
