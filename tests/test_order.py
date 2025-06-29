import pytest
import allure
from helpers import GeneratorData, User, Order


@allure.feature("Создание заказа")
@allure.story("Создание заказа авторизованным пользователем с ингредиентами")
def test_create_order_with_auth_and_ingredients(registered_user):
    token = User.get_access_token(User.login_user(registered_user))
    ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
    response = Order.create_order({"ingredients": ingredients}, token=token)

    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.feature("Создание заказа")
@allure.story("Создание заказа без авторизации")
def test_create_order_without_auth():
    ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
    response = Order.create_order({"ingredients": ingredients})
    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.feature("Создание заказа")
@allure.story("Создание заказа с пустым списком ингредиентов")
def test_create_order_with_empty_ingredients():
    response = Order.create_order({"ingredients": []})
    assert response.status_code == 400
    assert response.json()["success"] is False


@allure.feature("Создание заказа")
@allure.story("Создание заказа с невалидными ингредиентами")
@pytest.mark.parametrize("invalid_ingredients", [
    ["invalid_id_1"],
    ["123456789012345678901234"],
    ["", None],
    ["!@#$%^"]
])
def test_create_order_with_invalid_ingredients(invalid_ingredients):
    response = Order.create_order({"ingredients": invalid_ingredients})
    assert response.status_code in (400, 500)


@allure.feature("Получение заказов")
@allure.story("Получение заказов авторизованным пользователем")
def test_get_orders_with_auth(registered_user):
    token = User.get_access_token(User.login_user(registered_user))
    ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
    Order.create_order({"ingredients": ingredients}, token=token)
    response = Order.get_orders(token=token)
    assert response.status_code == 200
    assert isinstance(response.json().get("orders"), list)
    

@allure.feature("Получение заказов")
@allure.story("Получение заказов неавторизованным пользователем")
def test_get_orders_without_auth():
    response = Order.get_orders()
    assert response.status_code in (401, 403)
    assert response.json().get("success") is False