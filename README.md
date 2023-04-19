# Инструкция по запуску.
## Через docker-compose:
1. Перейти в директорию:
```
cd infra
```
2. Создать env файл и заполнить:
```
touch .env
```
Требуется указать:
* DB_ENGINE=django.db.backends.postgresql # database
* DB_NAME=postgres # name database
* POSTGRES_USER=postgres # login for connect to database
* POSTGRES_PASSWORD=12345 # password for connect to database
* DB_HOST=db # name container with database
* DB_PORT=5432 # login for connect to database

Необязательны:
* DEBUG=False
* SECRET_KEY=12345 # secret key for Django project 
3. Создать и запустить контейнеры:
```
docker-compose up -d --build
```
4. Открыть bash терминал в контейнере с проектом:
```
docker-compose exec backend bash
```
5. Создать и применить миграции:
```
python manage.py makemigrations
python manage.py migrate
```
6. Опционально можно загрузить тестовую базу, 
если в этом нет необходимости переходить к шагу 8.
Открыть редактор shell:
```
python manage.py shell
```
7. Произвести очитку БД:
```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```
8. Загрузить тестовую БД:
```
python manage.py loaddata data/test_db.json
```
9. Создать Администратора(суперпользователя) при необходимости:
```
python factory/manage.py createsuperuser
```
10. Открыть в браузере localhost/admin

## Для запуска в докере локально:
1. Собрать образ:
```
docker build -t abonent_test_img .
```
2. Создать и заполнить .env файл при необходимости:
Создать:
```
touch .env
```
3. Создать и запустить контейнер:
```
docker run --name abonent_test -it -p 8000:8000 abonent_test_img 
```
4. Открыть localhost:8000 в браузере.

## Без создания образа:
1. Создать и активировать виртуальное окружение:
Команда для Mac или Linux:
```
python3 -m venv env
source env/bin/activate
```
Команда для Windows:
```
python -m venv venv
. venv/Scripts/activate
```
2. Установить зависимости из requirements.txt:
```
pip install -r requirements.txt
```
3. Запустить миграции:
```
python factory/manage.py makemigrations
python factory/manage.py migrate
```
4. Запустить сервер разработки
```
python factory/manage.py runserver
```