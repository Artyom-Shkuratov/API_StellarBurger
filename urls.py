class Urls:
    BASE_URL = "https://stellarburgers.nomoreparties.site"

    # url для пользователя
    CREATE_USER = f"{BASE_URL}/api/auth/register"
    LOGIN_USER = f"{BASE_URL}/api/auth/login"
    USER_DATA = f"{BASE_URL}/api/auth/user" 
    DELETE_USER = f"{BASE_URL}/auth/user" 
    # url для заказов
    CREATE_ORDER = f"{BASE_URL}/api/orders"  
    USER_ORDERS = f"{BASE_URL}/api/orders"   
    # url для ингредиентов
    INGREDIENTS = f"{BASE_URL}/api/ingredients"
    
    