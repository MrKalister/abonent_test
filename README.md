# abonent_test
Для запуска в докере необходимо:
1. Собрать образ
```
docker build -t abonent_test_img .
```
2. Создать и запустить контейнер
```
docker run --name abonent_test -it -p 8000:8000 abonent_test_img 
```
3. Перейти на веб-страницу localhost.