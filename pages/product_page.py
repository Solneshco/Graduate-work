from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductPage(BasePage):
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".product-buttons__main-action[type='button']")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product-detail-page__title")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def get_product_title(self):
        return self.find_element(self.PRODUCT_TITLE).text
