# Game Di - Сайт по продаже детективных игр

Этот проект разрабатывается с использованием Django и представляет собой веб-сайт, посвященный продаже детективных игр. Проект находится в стадии активной разработки.

## Технологии

- Python
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript

## Запуск проекта

Проект разделен на 3 контейнера: nginx, PostgreSQL, Django.
Для запуска проекта выполните следующие шаги:

1. Склонируйте репозиторий `gamedi` на свой компьютер:
   ```bash
    git clone https://github.com/platsajacki/gamedi.git
    ```

2. Создайте и заполните файл `.env` по образцу `.env.example`, разместите его в директории проекта.

3. Из директории проекта запустите проект с помощью Docker Compose:
    ```bash
    docker compose up -d
    ```

4. В контейнере с Django проведите миграцию и скопируйте статику:
    ```bash
    docker compose exec gamedi python manage.py migrate
    docker compose exec gamedi cp -r /app/staticfiles/. /static/
    ```

5. Если потребуется работа в панели администратора, создайте суперпользователя:
    ```bash
    docker compose exec gamedi python manage.py createsuperuser
    ```

6. Теперь вы можете обращаться к API по адресу: http://127.0.0.1:8000/

