# Задание №3
# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Создайте маршрут для обновления информации о пользователе (метод PUT).
# Создайте маршрут для удаления информации о пользователе (метод DELETE).
# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.
# Реализуйте валидацию данных запроса и ответа

from fastapi import FastAPI, Request, HTTPException
from typing import Optional, Annotated
from pydantic import BaseModel
import logging

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="./Flask_seminar_5/templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


user_1 = User(id=1, name='Pavel', email='pavel@ya.ru', password='123456')
user_2 = User(id=2, name='Ivan', email='ivan@ya.ru', password='111111')
user_3 = User(id=3, name='Petr', email='petr@ya.ru', password='654321')

users = [user_1, user_2, user_3]


@app.get("/users/")
async def get_users():
    global users
    logger.info(f'Обработан запрос для вывода списка пользователей')
    return {"users": users}


@app.get("/users/list", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})



@app.post("/user/")
async def create_user(user: User):
    users.append(user)
    logger.info('Отработал POST запрос для создания пользователя.')
    return user
#
#
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    for i in range(len(users)):
        if users[i].id == user_id:
            users[i] = user
    logger.info(f'Отработал PUT запрос для пользователя = {user_id}.')
    return user


@app.delete("/users/{user_id}")
async def delete_task(user_id: int):
    for i in range(len(users)):
        if users[i].id == user_id:
            return {"user_id": users.pop(i)}
    return HTTPException(status_code=404, detail='Пользователь не найден')