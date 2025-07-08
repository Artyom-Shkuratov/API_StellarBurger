import requests
import allure
from urls import Urls


class Order:

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(order_data, token=None):
        headers = {"Authorization": token} if token else None
        return requests.post(url=Urls.CREATE_ORDER, json=order_data, headers=headers)

    @staticmethod
    @allure.step("Получение списка заказов")
    def get_orders(token=None):
        headers = {"Authorization": token} if token else None
        return requests.get(url=Urls.USER_ORDERS, headers=headers)

    @staticmethod
    @allure.step("Получение списка ингредиентов")
    def get_ingredients_list():
        response = requests.get(f'{Urls.INGREDIENTS}')
        return response.json().get('data', [])

    @staticmethod
    @allure.step("Получение заказов конкретного пользователя")
    def getting_order_list(token=None):
        if token:
            headers = {"Authorization": token}
            response = requests.get(f'{Urls.USER_ORDERS}', headers=headers)
            return response.status_code, response.json()
        return requests.get(f'{Urls.USER_ORDERS}')

    @staticmethod
    @allure.step("Изменение хеша ингредиентов")
    def modify_ingredient_hashes(ingredients):
        return [hash_[:-1] for hash_ in ingredients]