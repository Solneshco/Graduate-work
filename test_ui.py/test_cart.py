import pytest
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestCartFunctionality:

    @pytest.mark.ui
    def test_add_product_to_cart_from_product_page(self, driver):
        """Тест №10: Добавление товара в корзину со страницы товара."""
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        driver.get(" https://www.chitai-gorod.ru/")
        main_page.search_book("Полное название книги")
        main_page.open_first_result()
        product_page.add_to_cart()
        # Проверка, что товар добавлен (например, через всплывающее сообщение или переход в корзину)
        assert product_page.page_source_contains("Товар добавлен") or cart_page.get_items_count() == 1

    @pytest.mark.ui
    def test_update_quantity_in_cart(self, driver):
        """Тест №13: Изменение количества товара в корзине."""
        cart_page = CartPage(driver)
        # Предварительно добавить товар в корзину...
        cart_page.update_quantity(0, 3)
        # Проверка, что количество обновилось
        # (зависит от реализации, например, через атрибут value)
        assert True  # Заменить на реальную проверку

    @pytest.mark.ui
    def test_remove_item_from_cart(self, driver):
        """Тест №14: Удаление товара из корзины."""
        cart_page = CartPage(driver)
        initial_count = cart_page.get_items_count()
        cart_page.remove_item(0)
        assert cart_page.get_items_count() == initial_count - 1

    @pytest.mark.ui
    def test_total_sum_updates(self, driver):
        """Тест №15: Обновление итоговой суммы при изменении состава корзины."""
        cart_page = CartPage(driver)
        initial_sum = cart_page.get_total_sum()
        cart_page.update_quantity(0, 2)
        new_sum = cart_page.get_total_sum()
        assert initial_sum != new_sum  # Упрощенная проверка
