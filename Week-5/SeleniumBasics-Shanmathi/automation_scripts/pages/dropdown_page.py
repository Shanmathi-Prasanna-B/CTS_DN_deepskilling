from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DropdownPage(BasePage):
    DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name):
        element = self.wait_for_element(self.DROPDOWN)
        Select(element).select_by_visible_text(day_name)

    def get_selected_day_text(self):
        element = self.wait_for_element(self.DROPDOWN)
        return Select(element).first_selected_option.text
