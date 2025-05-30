# Python-WEB_team-project Instruction
Фінальний командний проєкт для курсу Python WEB (школа GO.IT)

## Інструкція для частини проекту в Docker-образі
Для детальної інструкції щодо використання Docker перегляньте [README.docker.md](README.docker.md).

I. Загальна інформація про додаток
==================================
    Цей веб-застосунок "Персональний асистент" (Personal Assistant) допоможе вам залишатися організованими, надаючи такі можливості: 
        * Створення та керування нотатками на будь-яку тему.
        * Збереження та керування контактами.
        * Зберігання файлів невеликого розміру на хмарному сервісі та управління цими файлами.
        * Новинна стрічка зі спортивними подіями, українською політикою, курсами валют та прогнозом погоди.

    Для доступу до всіх функцій необхідна реєстрація, щоб забезпечити безпеку та конфіденційність ваших даних.
    Кожен користувач має доступ лише до своїх особистих даних, які недоступні іншим користувачам та неавторизованим особам.

II. Встановлення додатку
========================
1) Відкрийте VSCode або PyCharm та склонуйте цей репозиторій.

2) Створіть базу даних PostgreSQL у Docker. 
    1. Відкрийте Docker Desktop
    2. Відкрийте командний рядок та виконайте команду:
        ```
        docker run --name web_project_db -p 5432:5432 -e POSTGRES_PASSWORD=web_project_db_pass -d postgres
        ```
    3. Якщо ви використовуєте команду вище без змін, то ви можете використовувати стандартні облікові дані з файлу .env.example (позначені як #Default).

    Важливо:

    Якщо PostgreSQL вже встановлений локально на вашому комп’ютері, змініть зовнішній порт на 5433 (або інший вільний порт), щоб уникнути конфлікту:
        ```
        docker run --name web_project_db -p 5433:5432 -e POSTGRES_PASSWORD=web_project_db_pass -d postgres
        ```
    Якщо ви використовуєте власні облікові дані, збережіть ім’я бази та пароль, оскільки вони знадобляться у файлі .env.

3)  Створіть та активуйте віртуальне середовище (venv). 
    1. Створіть venv за допомогою команди в терміналі VSCode:
        ```
        python -m venv venv
        ```
4) Активуйте venv:
    4a. Для Windows додайте і виконайте таку команду в терміналі:
        ```
        venv\Scripts\Activate
        ```
    4b. Якщо ви використовуєте cmd:
        ```
        venv\Scripts\activate.bat
        ```
    4c. Якщо використовуєте poetry:
        ```
        poetry shell
        ```

5) Встановіть poetry (якщо він ще не встановлений):
        ```
        pip install poetry
        ```

6) Встановіть усі залежності проєкту:
    ```
    poetry install
    ```

7) Створіть файл .env:
    1. У кореневій папці створіть файл .env (можна взяти .env.example як зразок).
    2. Згенеруйте SECRET_KEY за допомогою команди:
        ```
        poetry run python src/utils/gen_secret_key.py
        ```
        В терміналі отримаєте ключ. Додайте отриманий ключ у файл .env.
    
    3. Конфігурація Cloudinary:
        Ви можете використовувати заздалегідь налаштований акаунт Cloudinary, скопіювавши облікові дані з .env.example (позначені як #Default).
        Ці дані дозволяють додатку взаємодіяти з Cloudinary, але не дають доступу до акаунту. 
        Якщо бажаєте використовувати власний акаунт Cloudinary, то перейдіть за посиланням [Cloudinary](https://cloudinary.com/), зареєструйтесь, отримайте облікові дані (CLOUD_NAME, API_KEY, API_SECRET) та додайте їх у файл .env.

8) Застосуйте міграції до бази даних:
    ```
    poetry run python src/manage.py migrate
    ```
9) Запустіть сервер:
    ```
    python src/manage.py runserver
    ```
10) Відкрийте браузер за посиланням http://127.0.0.1:8000/ Можна працювати з Персональним Асистентом (Personal Assistant) через веб-інтерфейс.

11) Для використання сервісу необхідна реєстрація.

12) Якщо ви забули пароль, натисніть кнопку "Забули пароль", і вам на пошту прийде лист з посиланням на його відновлення. Слідуйте отриманим інструкціям.

13) Всі дані зберігаються у базі даних PostgreSQL всередині Docker-контейнера.

14) Завантажені файли будуть автоматично сортуватися у 6 категорій (зображення, документи, відео, аудіо, архіви, інше) та зберігатися у відповідних папках у Cloudinary. Ви можете завантажувати, переглядати (якщо формат підтримується), завантажувати або видаляти файли.

15) Обмеження щодо завантаження файлів::
    Максимальний розмір зображень – 10 МБ
    Максимальний розмір відео – 100 МБ
    Максимальний розмір необробленого файлу – 10 МБ
    MМаксимальна кількість мегапікселів для зображення – 25 MP
    Максимальна кількість мегапікселів у всіх кадрах – 50 MP
    --------------------------------------
    Заборонені розширення: .exe, .bat
    --------------------------------------

16) Якщо вам потрібні тестові дані, ви можете створити 50 фейкових контактів і 50 фейкових нотаток:
    ```
    poetry run python src/utils/gen_fake_data.py
    ```
    (Перед виконанням команди зареєструйте хоча б одного користувача).

17) Обмеження щодо навантаження дефолтного аккаунта для відправки повідомлень про відновлення пароля - до 100 листів на день, якщо надсилати через SMTP із додатка, як у випадку налаштувань даного додатка.

18) Щоб зупинити Персонального Асистента, перейдіть у термінал, де працює сервер, і натисніть Ctrl+C. 
Всі ваші дані (обліковий запис, контакти, нотатки, теги та файли) залишаться збереженими в базі Postgres в Docker-контейнері.


III. Системні вимоги
====================
    Операційна система: Windows, macOS або Linux
    Версія Python: 3.11 або вище, але нижче ніж 3.13
    Менеджер пакетів: Poetry
    База даних: PostgreSQL (створюється в Docker)
    Додаткові вимоги: Docker (для запуску PostgreSQL у контейнері)


IV. Запуск тестів
====================
    Щоб запустити всі тести:
        ```
        python src/manage.py test
        ``` 
    --------------------------------
    Щоб запустити тести для окремого застосунку (наприклад, для files):
        ```
        python src/manage.py test files 
        ```
        (Замініть "files" на назву необхідного блоку: contacts, files, news, notes, users)
    -----------------------------
    Щоб запустити окремий клас тестів (наприклад, FileUploadTest у застосунку files):
        ```
        python src/manage.py test files.tests.FileUploadTest
        ```
        (Замініть "files" на назву необхідного блоку: contacts, files, news, notes, users; 
        також замініть "FileUploadTest" на назву необхідного класу тестів)
    ------------------------
    Щоб запустити конкретний тест (наприклад, test_upload_file_success):
        ```
        python src/manage.py test files.tests.FileUploadTest.test_upload_file_success
        ```
        (Замініть "files" на назву необхідного блоку: contacts, files, news, notes, users; 
        також замініть "FileUploadTest" на назву необхідного класу тестів,
        та замініть "test_upload_file_success" на назву відповідного тесту.)

