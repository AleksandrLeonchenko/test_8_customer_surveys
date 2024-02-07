# Тестовое задание

## Cоздание сервиса опросов с учетом пользователя и динамическим отображением вопросов.

### Создайте веб-приложение на базе Django для проведения опросов и возможностью динамического отображения вопросов в зависимости от ответов пользователя.

Приложение должно включать в себя модели для опросов, вопросов и ответов, а также следующие функции:

- Создание и редактирование опросов и вопросов через админку.
- Реализацию веб-интерфейса, позволяющего пользователям проходить опросы и отвечать на вопросы.
- Сохранение ответов пользователей в связке с соответствующими опросами.
- Логику, позволяющую определить, какие вопросы показывать или скрывать в зависимости от предыдущих ответов пользователя (т.е. дерево)
- Вывод результатов опросов, включая статистику ответов на каждый вопрос, после завершения опроса.
    
    Реализовать с помощью минимального кол-ва SQL-запросов *без использования ORM*:
    
    - Общее кол-во участников опроса (например, 100)
    - На каждый вопрос:
        - Кол-во ответивших и их доля от общего кол-ва участников опроса (например, 95 / 95%)
        - Порядковый номер вопроса по кол-ву ответивших. Если кол-во совпадает, то и номер должен совпадать (например, для трех вопросов с 95, 95, 75 ответивших получаются соответствующие им номера 1, 1, 2)
        - Кол-во ответивших на каждый из вариантов ответа и их доля от общего кол-ва ответивших на этот вопрос после завершения опроса.

    
## Технологии
- Django 5.0.1
- PostgreSQL 15
- Django Rest Framework 3.14.0

## Установка и настройка

### Предварительные требования
- Python 3.11
- pip
- virtualenv
- Django 5.0.1
- PostgreSQL 15
- Django Rest Framework 3.14.0

### Установка
1. Клонируйте репозиторий:
```bash
https://github.com/AleksandrLeonchenko/test_8_customer_surveys.git
```
2. Создайте и активируйте виртуальное окружение:
```bash
virtualenv venv
source venv/bin/activate  # на Linux/macOS
.\venv\Scripts\activate   # на Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Настройте базу данных в settings.py и выполните миграции:
```bash
python manage.py migrate
```

## Запуск проекта
```bash
python manage.py runserver
```
Сервер работает на http://127.0.0.1:8000/

## Дополнительно:
- home/- домашняя страница
- register/- страница регистрации
- login/- страница входа
- logout/- выход
- survey/1/'- интерфейс, позволяющий пользователям проходить опросы и отвечать на вопросы
- survey/1>/respondents/- получение общего количества участников опроса по его ID
- survey/1/statistics/- получение статистики опроса
- survey/1/respondents/30/- кол-во ответивших и их доля от общего кол-ва участников опроса
- survey/1/ordering/- порядковый номер вопроса по количеству ответивших
- survey/1/response_rate/30/- подсчет количества выбравших каждый вариант ответа

Здесь 1 - это номер опроса, 30 - это номер вопроса.