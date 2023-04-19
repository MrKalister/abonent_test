FROM python:3.9.16-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY factory/ .
RUN python3 manage.py collectstatic --no-input
ENV DEBUG True
# Выполнить запуск сервера разработки при старте контейнера.
CMD ["python3", "manage.py", "runserver", "0:8000"] 