# Для запуска бота необходимо: 
1. поставить Python 3.12.1

# Создать виртуальное окружение и активировать его:
2. python -m venv venv 
3. source venv/bin/activate

# Установить зависимости:
4. pip install -r requirements.txt

# Создать .env файл в котором необходимо создать 2 парметра:
6. 
    - BOT_TOKEN = 'ваш токен'
    - ADMIN_ID = 'id пользователя телеграмма которому будут приходить отчеты из бота'

# Далее установить redis и postgres (пример для Ubuntu)
7. apt-get install redis
8. apt-get install postgresql

# Создать в postgresql базу данных 'users':
9. psql -U postgres
10. CREATE DATABASE users;
11. GRANT ALL PRIVILEGES ON DATABASE users TO postgres;

# Запустить main.py 
- Для проверки работоспособности введите из териманала python main.py
- Для запуска на сервере рекомендуется использовать pm2 / systemctl / docker. 
Команда для запуска проекта - python main.py