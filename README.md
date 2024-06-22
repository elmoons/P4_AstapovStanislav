# Сервис для шифрования и дешифрования

## Требования
- Python 3.8+
- pip

## Установка

1. Клонируйте репозиторий:

   ```sh
   git clone https://github.com/elmoons/P4_AstapovStanislav.git
   cd service_of_encryption
   ```

2. Создайте и активируйте виртуальное окружение (рекомендуется):

   - Для Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - Для macOS/Linux:
     ```sh
     python -m venv venv
     source venv/bin/activate
     ```

3. Установите зависимости:

   ```sh
   pip install -r requirements.txt
   ```

## Запуск

1. Запустите сервер FastAPI:

   ```sh
   uvicorn app.main:app --reload
   ```

   Здесь `app.main` - путь к вашему основному модулю приложения.

2. Перейдите в браузере по адресу:

   ```
   http://127.0.0.1:8000
   ```

3. Документацию по API можно посмотреть по адресу:

   ```
   http://127.0.0.1:8000/docs
   ```
