# Запуск
Для того что бы запустить проект необходимо:

- [запустить админ](#запуск-админ-панели)
- [запустить контейнер парсера](#запуск-парсера)

# Запуск Админ Панели
- Админ панель запускается с помощью команды `docker compose up --build`.
- Создание админ пользователя `docker exec -it sitesoft-test-job-admin_panel-1 python manage.py createsuperuser --username sitesoft --email sitesoft@example.com`
- Введите пароль который будете использовать
- После запуска на нее можно перейти по ссылке `localhost:8100`
- Введите ваш логин пароль

# Запуск парсера
Запуск парсера происходит только когда запущена админ панель, это связанно с тем что с админ панелью поднимается база данных.

Запуск:

- внутри папки *habr_parser* запустите команду `docker build . -t sitesoft_parser && docker run --name sitesoft_parser sitesoft_parser`

Парсер будет выполнять свои функции в полном обьеме.