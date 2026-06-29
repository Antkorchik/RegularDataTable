import requests
import json

r = requests.get("http://localhost:8000/")
print("Сервер:", r.json())

register_data = {"login": "testuser", "password": "123456"}
r = requests.post("http://localhost:8000/register", json=register_data)
print("Регистрация:", r.json())

login_data = {"login": "testuser", "password": "123456"}
r = requests.post("http://localhost:8000/login", json=login_data)
print("Вход в аккаунт:", r.json())

r = requests.get("http://localhost:8000/users/testuser")
print("Поиск:", r.json())


r = requests.get("http://localhost:8000/users/nonexistent")
print("Несуществующий:", r.json())