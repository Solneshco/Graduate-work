import pytest
from pages.main_page import MainPage


class TestSearchFunctionality:

    @pytest.mark.ui
    def test_search_by_full_book_title(self, driver):
        """Тест №1: Поиск по полному названию книги."""
        main_page = MainPage(driver)
        driver.get(" https://www.chitai-gorod.ru/")
        main_page.search_book("Мастер и Маргарита")
        # Проверка, что результаты содержат искомую книгу
        assert "Мастер и Маргарита" in driver.page_source