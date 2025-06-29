import random
import requests
import string
import allure
from faker import Faker
from data import email_domains
from urls import Urls


fake = Faker()


class GeneratorData:
    
    #создаем случайное имя
    @staticmethod
    def generate_name():
        return fake.first_name()
    
    #создаем случайный пароль
    @staticmethod
    def generate_password(length=10):
        return fake.password()
    
    #создаем случайную почту
    @staticmethod
    def generate_email(length=8):
        local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return f"{local}{random.choice(email_domains)}"
    
    
    @staticmethod
    def generate_payload():
        payload =  {
            "email": GeneratorData.generate_email(),
            "password": GeneratorData.generate_password(),
            "name": GeneratorData.generate_name()
        }
        return payload
    
    
class User:
        
        @staticmethod
        @allure.step("Регистрация пользователя")
        def register_user(user_data):
            response = requests.post(Urls.CREATE_USER, json=user_data)
            return response
        
        @staticmethod
        @allure.step("Создание пользователя без обязательного поля: {missing_field}")
        def register_user_without_required_field(missing_field):
            user_data = GeneratorData.generate_user()
            user_data.pop(missing_field, None) 
            response = requests.post(url=Urls.CREATE_USER, json=user_data)
            return response
        
        
        @staticmethod
        @allure.step("Получить access token из ответа сервера")
        def get_access_token(response):
            data = response.json()
            allure.attach(str(data), name="Тело ответа", attachment_type=allure.attachment_type.JSON)
            return data.get("accessToken")
        
        @staticmethod
        @allure.step("Изменение данных пользователя")
        def update_user_data(user_data):
            login_response = GeneratorData.User.login_user(user_data)
            token = login_response.json().get("accessToken")
            headers = {"Authorization": token}
            
            updated_data = {
                "email": GeneratorData.generate_email(),
                "name": GeneratorData.generate_name()
            }

            response = requests.patch(Urls.EDIT_USER, headers=headers, json=updated_data)
            return response
        
        @staticmethod
        @allure.step("Логин пользователя")
        def login_user(user_data):
            payload = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            response = requests.post(Urls.LOGIN_USER, json=payload)
            return response
        
        @staticmethod
        @allure.step("Удаление пользователя после теста")
        def delete_user(user_data):
            login_response = GeneratorData.User.login_user(user_data)
            if login_response.status_code == 200:
                token = login_response.json().get("accessToken")
                headers = {"Authorization": token}
                return requests.delete(url=Urls.DELETE_USER, headers=headers)
            return login_response
        
class Order:
        
        @staticmethod
        @allure.step("Создание заказа")
        def create_order(order_data, token=None):
            headers = {"Authorization": token} if token else None
            response = requests.post(url=Urls.CREATE_ORDER, json=order_data, headers=headers)
            return response
        
        @staticmethod
        @allure.step("Получение списка заказов")
        def get_orders(token=None):
            headers = {"Authorization": token} if token else None
            response = requests.get(url=Urls.USER_ORDERS, headers=headers)
            return response
        
        @staticmethod
        @allure.step("Получение списка ингредиентов")
        def get_ingredients_list():
            response = requests.get(f'{Urls.INGREDIENTS}')
            return response.json()['data', []]
        
        @staticmethod
        @allure.step("Получение списка заказов конкретного пользователя")
        def getting_order_list(token=None):
            if token:
                headers = {"Authorization": token}
                response = requests.get(f'{Urls.USER_ORDERS}', headers=headers)
                return response.status_code, response.json()
            else:
                return requests.get(f'{Urls.USER_ORDERS}')
        
        @staticmethod
        @allure.step("Изменение хеша ингредиентов")
        def modify_ingredient_hashes(ingredients):
            return [hash_[:-1] for hash_ in ingredients]