from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CSS_SELECTOR, ".cart-item")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart-item__quantity .chg-ui-input-number__input")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".cart-item__delete-button")
    TOTAL_SUM = (By.CSS_SELECTOR, ".info-item__value")

    def get_items_count(self):
        return len(self.driver.find_elements(*self.CART_ITEM))

    def get_cart_items_count(self):
        return self.get_items_count()

    def update_quantity(self, index, new_quantity):
        inputs = self.driver.find_elements(*self.QUANTITY_INPUT)
        inputs[index].clear()
        inputs[index].send_keys(str(new_quantity))

    def remove_item(self, index):
        buttons = self.driver.find_elements(*self.REMOVE_BUTTON)
        buttons[index].click()

    def get_total_sum(self):
        sums = self.driver.find_elements(*self.TOTAL_SUM)
        return sums[3].text
        
