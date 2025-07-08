import allure
from logic.user_logic import User
from logic.order_logic import Order


class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем с ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user):
        token = User.get_access_token(User.login_user(registered_user))
        ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
        response = Order.create_order({"ingredients": ingredients}, token=token)
        
        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
        response = Order.create_order({"ingredients": ingredients})
        
        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Создание заказа с пустым списком ингредиентов")
    def test_create_order_with_empty_ingredients(self):
        response = Order.create_order({"ingredients": []})
        
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_with_modified_ingredient_hashes(self):
        valid_ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
        invalid_ingredients = Order.modify_ingredient_hashes(valid_ingredients)
        response = Order.create_order({"ingredients": invalid_ingredients})
        
        assert response.status_code == 500
        assert "Internal Server Error" in response.text


class TestOrderRetrieval:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_with_auth(self, registered_user):
        token = User.get_access_token(User.login_user(registered_user))
        ingredients = [item['_id'] for item in Order.get_ingredients_list()[:3]]
        Order.create_order({"ingredients": ingredients}, token=token)
        response = Order.get_orders(token=token)
        
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert isinstance(response.json().get("orders"), list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_without_auth(self):
        response = Order.get_orders()
        
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "You should be authorised"