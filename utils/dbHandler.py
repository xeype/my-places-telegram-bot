import sqlite3
from utils import queries

conn = sqlite3.connect('db/db.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, username: str):
    cursor.execute(queries.add_user, (user_id, username))
    conn.commit()


def add_place(user_id: int, place_name: str, rating: int, place_desc: str):
    cursor.execute(queries.add_place, (user_id, place_name, rating, place_desc))
    conn.commit()


def get_places(user_id):
    places = []
    query_str = queries.get_places.format(user_id)
    query = cursor.execute(query_str)
    for place_name, rating, desc in query:
        places.append((place_name, rating, desc))
    return places
