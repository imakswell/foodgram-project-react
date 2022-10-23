#Проект «Продуктовый помощник»

### Автор проекта
[Максим Фагин](https://github.com/imakswell/) 

---
## Описание проекта «Продуктовый помощник»
Это сайт, на котором пользователи могут публиковать рецепты, добавлять чужие
рецепты в избранное и подписываться на публикации других авторов. Сервис 
«Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для 
приготовления выбранных блюд, и скачивать их в виде текстового файла.

---
## Основные endpoint'ы

* signup — регистрация пользователя.
* token — получение токена для аутентификации пользователя.
* users — работа с пользователями.
* recipes — работа с рецептами.
* tags — просмотр тегов.
* ingredients — просмотр ингридиентов.

## Используемые технологии
* Node.js
* Django REST Framework
* Djoser

## Инструкция по запуску проекта

Все операции выполняются в командной строке.


* Клонировать репозиторий:
```
git clone git@github.com:imakswell/foodgram-project-react.git
```

В дериктории infra/ cоздать файл .env, в котором указать переменные окружения для работы с базой данных:
```
cp .env.example .env
```

* Из дериктории infra/ запустить docker-compose командой:
```
sudo docker-compose up -d --build
```
* Загрузить статические файлы:
```
sudo docker-compose exec backend python manage.py collectstatic
```
* Выполнить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```

* Создать суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```

* При необходимости загрузить тестовые данные:
```
sudo docker-compose exec backend python manage.py runscript scripts.load_data
```
![foodgram_workflow](https://github.com/imakswell/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Сервис доступен по адресу [http://84.201.128.16/recipes](http://84.201.128.16/recipes)