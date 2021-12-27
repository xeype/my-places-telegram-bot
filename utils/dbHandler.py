import sqlite3
import queries

conn = sqlite3.connect('db/db.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, username: str):
    cursor.execute(queries.add_user, (user_id, username))
    conn.commit()
