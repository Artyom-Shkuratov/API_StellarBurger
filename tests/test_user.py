import pytest
import allure
from helpers import GeneratorData, User


@allure.suite("Регистрация пользователя")
class TestUserRegistration:

    @allure.title("Успешная регистрация нового пользователя")
    def test_register_user_successfully(self):
        user_data = GeneratorData.generate_payload()
        response = User.register_user(user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_user_without_required_field(self, missing_field):
        response = User.register_user_without_required_field(missing_field)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"


@allure.suite("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self):
        user_data = GeneratorData.generate_payload()
        User.register_user(user_data)
        response = User.login_user(user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Логин с некорректными данными")
    def test_login_with_wrong_credentials(self):
        wrong_data = {
            "email": GeneratorData.generate_email(),
            "password": "incorrect123"
        }
        response = User.login_user(wrong_data)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"


@allure.suite("Редактирование данных пользователя")
class TestUserUpdate:

    @allure.title("Успешное изменение данных пользователя")
    def test_update_user_data(self):
        user_data = GeneratorData.generate_payload()
        User.register_user(user_data)
        response = User.update_user_data(user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "user" in response.json()
        assert "email" in response.json()["user"]
        assert "name" in response.json()["user"]