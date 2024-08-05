# User Management REST API

Этот проект представляет собой простой REST API для управления пользователями, реализованный на чистом Python без использования фреймворков.

## Структура проекта

- **user.py**: Определяет сущность `User` с атрибутами `id`, `lastname`, `firstname` и `middlename`. Также содержит метод `to_dict`, который преобразует объект пользователя в словарь.

- **repository.py**: Содержит реализацию репозиториев для хранения пользователей. Включает абстрактный класс `UserRepository`, а также две реализации: `InMemoryUserRepository` для хранения данных в памяти и `DatabaseUserRepository` для хранения данных в базе данных (используя SQLAlchemy).

- **main.py**: Основной файл, который запускает HTTP сервер и определяет обработчики запросов для создания, изменения, получения и удаления пользователей. Также включает логику инициализации репозитория на основе конфигурационного файла.

- **config.py**: (Этот файл не был указан в вашем запросе, но предполагается, что он может существовать для загрузки конфигурации) Загружает настройки из `config.json`, определяя тип репозитория (в памяти или база данных) и URL базы данных.

## Установка и запуск

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Установите зависимости:
    ```sh
    pip install sqlalchemy
    ```

3. Создайте конфигурационный файл `config.json` в корневой директории проекта:
    ```json
    {
        "repo_type": "in_memory",
        "db_url": "sqlite:///users.db"
    }
    ```

4. Запустите сервер:
    ```sh
    python main.py
    ```

## Использование API

### Создание пользователя

- **URL:** `/user`
- **Метод:** `POST`
- **Тело запроса:**
    ```json
    {
        "id": 1,
        "lastname": "Ivanov",
        "firstname": "Ivan",
        "middlename": "Ivanovich"
    }
    ```

### Изменение пользователя

- **URL:** `/user/{id}`
- **Метод:** `PUT`
- **Тело запроса:**
    ```json
    {
        "lastname": "Petrov"
    }
    ```

### Получение пользователя

- **URL:** `/user/{id}`
- **Метод:** `GET`

### Удаление пользователя

- **URL:** `/user/{id}`
- **Метод:** `DELETE`

## Пример запросов

Примеры запросов с использованием `curl`:

- **Создание пользователя:**
    ```sh
    curl -X POST http://localhost:8000/user -H "Content-Type: application/json" -d "{\"id\": 1, \"lastname\": \"Ivanov\", \"firstname\": \"Ivan\", \"middlename\": \"Ivanovich\"}"
    ```

- **Изменение пользователя:**
    ```sh
    curl -X PUT http://localhost:8000/user/1 -H "Content-Type: application/json" -d "{\"lastname\": \"Petrov\"}"
    ```

- **Получение пользователя:**
    ```sh
    curl -X GET http://localhost:8000/user/1
    ```

- **Удаление пользователя:**
    ```sh
    curl -X DELETE http://localhost:8000/user/1
    ```

## Лицензия

Этот проект лицензирован на условиях MIT License.
