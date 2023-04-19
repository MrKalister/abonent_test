FROM python:3.8.10-slim-buster
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic --no-input
# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "factory.wsgi:application", "--bind", "0:8000" ] 