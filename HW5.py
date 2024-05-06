import psycopg2

user_id = input("Введите ID пользователя, которого вы хотите удалить: ")
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
        try:
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            connect.commit()
            print("Пользователь успешно удален!")
        except psycopg2.Error as error:
            print("Ошибка при удалении пользователя:", error)
            connect.rollback()

    with connect.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        print(users)

