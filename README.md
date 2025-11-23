📝 SPA Comments — Тестовое задание

Полностью рабочее приложение: бекенд (Django + DRF + Channels) + фронтенд (Vue3) + Docker.

📌 Описание проекта

SPA-приложение для публикации комментариев, включая:
вложенные комментарии (бесконечная глубина),
пагинацию,
сортировку,
CAPTCHA-проверку,
real-time обновление комментариев через WebSocket,
защиту от HTML-инъекций, XSS и SQL-инъекций.

🚀 Функционал
👤 Пользователь может:
оставлять комментарии;
отвечать на другие комментарии (каскадная структура);
вводить данные:
User Name — обязательное поле
Email — обязательное
Home Page — опционально
CAPTCHA — обязательное
Text — обязательное

📄 Главная страница:

вывод корневых комментариев в виде таблицы;
сортировка по:
User Name
Email
Дате создания (ASC/DESC)
25 комментариев на странице (пагинация);
вложенные ответы выводятся каскадно.

🔐 Безопасность

защита от XSS — HTML очищается, разрешены только:

<b>, <i>, <strong>, <em>, <a>

защита от SQL-инъекций (Django ORM)
защита CAPTCHA (django-simple-captcha)

🔄 Real-time обновление

Через WebSocket (Django Channels):
когда пользователь оставляет комментарий → он появляется у всех пользователей без перезагрузки.

🛠 Технологии
Компонент	Технология
Backend	Django 5, Django REST Framework, Django Channels
Database	PostgreSQL
Frontend	Vue 3 (Vite)
WebSockets	Channels + Daphne
CAPTCHA	django-simple-captcha
Docker	docker-compose
Web Server	Nginx (reverse-proxy + WS support)

📁 Архитектура проекта
backend/
  project/
    settings.py
    urls.py
    asgi.py
  comments/
    models.py
    serializers.py
    views.py
    consumers.py
    routing.py
    utils.py
  static/
frontend/
  src/
    components/
    views/
    App.vue
    services/api.js
docker/
  nginx.conf
docker-compose.yml
README.md

⚙️ Установка и запуск локально (без Docker)
1. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  (Windows)
2. Установить зависимости
pip install -r backend/requirements.txt
3. Миграции
python backend/manage.py migrate
python backend/manage.py createsuperuser
4. Собрать CAPTCHA
python backend/manage.py collectstatic
5. Запуск бэкенда
daphne -b 0.0.0.0 -p 8000 project.asgi:application
6. Запуск фронтенда
cd frontend
npm install
npm run dev

🐳 Запуск через Docker
1. Собрать и запустить
docker-compose up --build -d

Сервисы:

Сервис	URL
Backend (Django + API + WS)	http://localhost:8000

Frontend (Vue SPA)	http://localhost:5173

WebSocket	ws://localhost:8000/ws/comments/
Admin panel	http://localhost:8000/admin

🔗 API Endpoints
📌 Получить комментарии
GET /api/comments/?ordering=username&ordering=-created_at&page=1
📌 Создать комментарий
POST /api/comments/

Body:

{
  "username": "Alex",
  "email": "alex@test.com",
  "homepage": "https://google.com",
  "captcha_key": "bd9e00c8ef5",
  "captcha_value": "FQ4D",
  "text": "Hello world!",
  "parent": 1
}

🔐 CAPTCHA

Используем django-simple-captcha.

Получить изображение CAPTCHA
GET /captcha/image/<key>/

Проверка CAPTCHA при создании комментария

В utils.py:

from captcha.models import CaptchaStore

def validate_captcha(key, value):
    try:
        captcha = CaptchaStore.objects.get(hashkey=key)
        return captcha.response.lower() == value.lower()
    except CaptchaStore.DoesNotExist:
        return False

🔄 WebSockets (Real-Time)

URL:

ws://localhost:8000/ws/comments/

При создании комментария бекенд отправляет всем клиентам:

{
  "id": 14,
  "username": "Alex",
  "email": "test@gmail.com",
  "text": "Hello world",
  "created_at": "2025-11-20T15:10:22",
  "parent": null
}

🖥 WebSocket клиент (Vue)
const ws = new WebSocket("ws://localhost:8000/ws/comments/");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  this.comments.unshift(data);
};

🧪 Чек-лист тестировщика
Форма создания комментария

✔ Поле username — обязательное
✔ Поле email — обязательное, формат email
✔ Поле homepage — опционально
✔ CAPTCHA обязательна
✔ Text очищается от HTML кроме разрешённых
✔ Нельзя вставлять <script> (XSS)

Функционал комментариев

✔ Корневые комментарии отображаются в таблице
✔ Вложенные выводятся каскадно
✔ Доступна сортировка по 3 полям (asc/desc)
✔ Пагинация — 25 элементов
✔ Создание комментария создаёт событие WebSocket
✔ Другие клиенты видят комментарий без перезагрузки

Backend

✔ Django
✔ DRF
✔ PostgreSQL
✔ Channels (WS)
✔ Docker image работает

Frontend

✔ SPA (Vue3)
✔ WebSocket клиент
✔ Список обновляется real-time

🧰 Команды разработчика
Backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Frontend
npm run dev
npm run build

Docker
docker-compose build
docker-compose up -d
docker-compose logs -f backend
