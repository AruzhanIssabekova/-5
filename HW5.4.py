import re
import psycopg2
import secrets
import string
with psycopg2.connect(
        dbname="lesson_third",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432",
) as connect:
    with connect.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS users 
                    (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(100)
                    )
                    """)
        connect.commit()
    with connect.cursor() as cur:
        name = input("Введите логин: ")
        password = input("Введите пароль (оставьте пустым, если хотите сгенерировать случайный пароль): ")
        if not password:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            while True:
                password = ''.join(secrets.choice(alphabet) for i in range(8))
                if (any(c.islower() for c in password) and
                        any(c.isupper() for c in password) and
                        any(c.isdigit() for c in password) and
                        any(c in string.punctuation for c in password)):
                    break
            print("Сгенерирован надежный пароль:", password)
        if len(password) >= 8 and bool(re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:"<>?`\-=[\];\',./])').match(password))==True:
            try:
                cur.execute("""
                    INSERT INTO users (username, password) VALUES (%s, %s)
                            """, (name, password))
                connect.commit()
            except psycopg2.errors.UniqueViolation as error:
                pass
            finally:
                connect.rollback()
        else:
            print(
                "Пароль слишком простой. Он должен содержать минимум 8 символов, хотя бы одну букву верхнего регистра, хотя бы одну букву нижнего регистра, хотя бы одну цифру и хотя бы один специальный символ.")


    with connect.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        print(users)
