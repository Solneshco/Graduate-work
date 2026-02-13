from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class MainPage(BasePage):
    SEARCH_INPUT = (By.ID, "app-search")
    FIRST_RESULT_LINK = (By.CSS_SELECTOR, "a.product-card__title[href*='/product/']")

    def search_book(self, book_title):
        search = self.find_element(self.SEARCH_INPUT)
        search.clear()
        search.send_keys(book_title)
        search.send_keys(Keys.ENTER)

    def open_first_result(self):
        all_result = self.find_elements(self.FIRST_RESULT_LINK)
        all_result[0].click()
