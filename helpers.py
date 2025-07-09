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
    
    
