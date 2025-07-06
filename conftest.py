import random
import pytest
from helpers import GeneratorData
from logic.user_logic import User
from logic.order_logic import Order


@pytest.fixture
def registered_user(random_user):
    User.register_user(random_user)
    yield random_user
    User.delete_user(random_user)
      
@pytest.fixture
def random_user():
    user_data = GeneratorData.generate_payload()
    yield user_data


@pytest.fixture
def get_random_ingridients():
    ingridients = Order.get_ingredients_list()
    return random.sample(ingridients, k=3)
    