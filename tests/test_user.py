import pytest
import allure
from helpers import GeneratorData, User


@allure.feature("Создание пользователя")
@allure.story("Успешная регистрация нового пользователя")
def test_register_user_successfully():
    user_data = GeneratorData.generate_payload()
    response = User.register_user(user_data)
    assert response.status_code == 200
    assert response.json().get("success") is True


@allure.feature("Создание пользователя")
@allure.story("Создание пользователя без обязательного поля")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_register_user_without_required_field(missing_field):
    response = User.register_user_without_required_field(missing_field)
    assert response.status_code in (403, 400)
    assert response.json().get("success") is False


@allure.feature("Авторизация пользователя")
@allure.story("Логин под существующим пользователем")
def test_login_existing_user():
    user_data = GeneratorData.generate_payload()
    User.register_user(user_data)
    response = User.login_user(user_data)
    assert response.status_code == 200
    assert "accessToken" in response.json()


@allure.feature("Авторизация пользователя")
@allure.story("Логин с некорректными данными")
def test_login_with_wrong_credentials():
    wrong_data = {
        "email": GeneratorData.generate_email(),
        "password": "incorrect123"
    }
    response = User.login_user(wrong_data)
    assert response.status_code == 401
    assert response.json().get("success") is False


@allure.feature("Изменение данных пользователя")
@allure.story("Успешное изменение данных пользователя")
def test_update_user_data():
    user_data = GeneratorData.generate_payload()
    User.register_user(user_data)
    response = User.update_user_data(user_data)
    assert response.status_code == 200
    assert response.json().get("success") is True