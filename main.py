from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

app = FastAPI()

# Пример массива машин
cars = [
    {"id": 1, "name": "Tesla Model S", "year": "2022"},
    {"id": 2, "name": "BMW M3", "year": "2020"},
    {"id": 3, "name": "Audi A6", "year": "2021"},
    # Добавьте еще несколько машин для тестирования
]

# Роут для получения списка машин с пагинацией
@app.get("/cars")
def get_cars(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]

# Роут для получения машины по id
@app.get("/cars/{car_id}")
def get_car(car_id: int):
    car = next((car for car in cars if car["id"] == car_id), None)
    if car:
        return car
    raise HTTPException(status_code=404, detail="Not found")

from fastapi.responses import HTMLResponse

# Пример массива пользователей
users = [
    {"id": 1, "email": "test@test.com", "first_name": "Aibek", "last_name": "Bekturov", "username": "deadly_knight95"},
    {"id": 2, "email": "hello@world.com", "first_name": "John", "last_name": "Doe", "username": "john_doe"},
    # Добавьте больше пользователей для тестов
]

# Роут для отображения всех пользователей в виде HTML таблицы
@app.get("/users", response_class=HTMLResponse)
def get_users(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    paginated_users = users[start:end]
    
    html_content = "<table>"
    for user in paginated_users:
        html_content += f"""
        <tr>
            <td>{user['username']}</td>
            <td><a href="/users/{user['id']}">{user['first_name']} {user['last_name']}</a></td>
        </tr>
        """
    html_content += "</table>"
    
    # Добавим ссылки для пагинации
    html_content += f'<a href="/users?page={page-1}&limit={limit}">Previous</a> | '
    html_content += f'<a href="/users?page={page+1}&limit={limit}">Next</a>'
    
    return html_content

# Роут для получения конкретного пользователя по id
@app.get("/users/{user_id}", response_class=HTMLResponse)
def get_user(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return f"""
        <h1>{user['first_name']} {user['last_name']}</h1>
        <p>Email: {user['email']}</p>
        <p>Username: {user['username']}</p>
        """
    raise HTTPException(status_code=404, detail="Not found")


