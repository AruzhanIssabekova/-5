import psycopg2
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
    user_name = input("Введите логин пользователя, для которого нужно обновить пароль: ")
    new_password = input("Введите новый пароль: ")
    try:
        cur.execute(
            """
            UPDATE users 
            SET password = %s 
            WHERE username = %s
            """,
            (new_password, user_name)
        )
        if cur.rowcount == 0:
            print("Пользователь с таким логином не найден.")
        else:
            print("Пароль успешно обновлен.")
        connect.commit()
    except Exception as e:
        print("Произошла ошибка:", e)
        connect.rollback()

    with connect.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        print(users)