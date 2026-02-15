import pytest
import requests

BASE_URL = "https://web-agr.chitai-gorod.ru"


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
    )
    return session


def get_anonymous_token(session: requests.Session) -> str:
    response = session.post(f"{BASE_URL}/web/api/v1/auth/anonymous", timeout=20)
    response.raise_for_status()
    token = response.json()["token"]["accessToken"]
    return token


def search_products(session: requests.Session, token: str, phrase: str) -> dict:
    response = session.get(
        f"{BASE_URL}/web/api/v2/search/product",
        params={"phrase": phrase},
        headers={"Authorization": token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def extract_products(search_payload: dict) -> list[dict]:
    return [item for item in search_payload.get("included", []) if item.get("type") == "product"]


def extract_pagination(search_payload: dict) -> dict:
    return search_payload["data"]["relationships"]["products"]["meta"]["pagination"]


@pytest.mark.api
def test_search_by_full_book_title(api_session):
    """Тест №1: Поиск по полному названию книги."""
    token = get_anonymous_token(api_session)
    payload = search_products(api_session, token, "Мастер и Маргарита")
    products = extract_products(payload)

    assert products, "Ожидались результаты поиска по названию книги."
    assert any(
        "мастер и маргарита" in p["attributes"]["title"].lower() for p in products
    ), "В результатах не найдено название книги."


@pytest.mark.api
def test_search_by_author(api_session):
    """Тест №2: Поиск по автору."""
    token = get_anonymous_token(api_session)
    payload = search_products(api_session, token, "Булгаков")
    products = extract_products(payload)

    assert products, "Ожидались результаты поиска по автору."
    assert any(
        any(a.get("lastName", "").lower() == "булгаков" for a in p["attributes"].get("authors", []))
        for p in products
    ), "В результатах не найден автор Булгаков."


@pytest.mark.api
def test_search_with_typo(api_session):
    """Тест №4: Поиск с опечатками (проверка работы \"нечеткого\" поиска)."""
    token = get_anonymous_token(api_session)
    typo_phrase = "мастер и маргарида"
    payload = search_products(api_session, token, typo_phrase)
    products = extract_products(payload)

    strategy = payload["data"]["attributes"].get("strategy", "")
    transformed = payload["data"]["attributes"].get("transformedPhrase", "")

    assert products, "Ожидались результаты поиска при опечатке."
    assert "correction" in strategy.lower(), "Ожидалась стратегия с исправлением опечаток."
    assert transformed and transformed != typo_phrase, "Ожидалось исправление поисковой фразы."


@pytest.mark.api
def test_search_nonexistent_product(api_session):
    """Тест №5: Поиск по несуществующему товару."""
    token = get_anonymous_token(api_session)
    payload = search_products(api_session, token, "несуществующаякнигаqwerty")
    products = extract_products(payload)
    pagination = extract_pagination(payload)

    assert products == [], "Не ожидались товары в результатах."
    assert pagination["total"] == 0, "Ожидалось нулевое количество найденных товаров."


@pytest.mark.api
def test_search_results_count_matches_pagination(api_session):
    """Тест №6: Отображение количества найденных товаров."""
    token = get_anonymous_token(api_session)
    payload = search_products(api_session, token, "Мастер и Маргарита")
    products = extract_products(payload)
    pagination = extract_pagination(payload)

    assert products, "Ожидались результаты поиска."
    assert pagination["count"] == len(products), "Количество на странице не совпадает с числом товаров."
    assert pagination["total"] >= pagination["count"], "Общее количество меньше количества на странице."
