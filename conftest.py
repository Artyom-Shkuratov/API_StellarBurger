import random
import pytest
import allure
from helpers import GeneratorData, User, Order


pytest.fixture
def registered_user():
        random_user_data = GeneratorData.generate_payload()
        response = User.register_user(random_user_data)
        yield response, random_user_data
        User.delete_user(random_user_data)
        
        
@pytest.fixture
def random_user():
    user_data=GeneratorData.generate_payload
    yield user_data
    User.delete_user(user_data)

@pytest.fixture
def get_random_ingridients():
    ingridients = Order.get_ingredients_list()
    return random.sample(ingridients, k=3)
    