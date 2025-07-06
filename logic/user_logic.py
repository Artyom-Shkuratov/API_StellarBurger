import requests
import allure
from urls import Urls
from helpers import GeneratorData


class User:

    @staticmethod
    @allure.step("Регистрация пользователя")
    def register_user(user_data):
        return requests.post(Urls.CREATE_USER, json=user_data)

    @staticmethod
    @allure.step("Создание пользователя без обязательного поля: {missing_field}")
    def register_user_without_required_field(missing_field):
        user_data = GeneratorData.generate_payload()
        user_data.pop(missing_field, None)
        return requests.post(url=Urls.CREATE_USER, json=user_data)

    @staticmethod
    @allure.step("Получить access token из ответа сервера")
    def get_access_token(response):
        data = response.json()
        allure.attach(str(data), name="Тело ответа", attachment_type=allure.attachment_type.JSON)
        return data.get("accessToken")

    @staticmethod
    @allure.step("Логин пользователя")
    def login_user(user_data):
        payload = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        return requests.post(Urls.LOGIN_USER, json=payload)

    @staticmethod
    @allure.step("Изменение данных пользователя")
    def update_user_data(user_data):
        login_response = User.login_user(user_data)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token}
        updated_data = {
            "email": GeneratorData.generate_email(),
            "name": GeneratorData.generate_name()
        }
        return requests.patch(Urls.USER_DATA, headers=headers, json=updated_data)

    @staticmethod
    @allure.step("Удаление пользователя после теста")
    def delete_user(user_data):
        login_response = User.login_user(user_data)
        if login_response.status_code == 200:
            token = login_response.json().get("accessToken")
            headers = {"Authorization": token}
            requests.delete(url=Urls.DELETE_USER, headers=headers)