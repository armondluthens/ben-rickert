import sqlite3
import os.path

DATABASE = "ben_rickert.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DATABASE)
SELECT_ALL_QUERY = "SELECT * FROM {};"


def drop(table):
    execute_query('DROP TABLE IF EXISTS {}'.format(table))


def clear(table):
    execute_query('DELETE FROM {}'.format(table))


def create(create_statement):
    execute_query(create_statement)


def get_all(table):
    return select_multi_rows(SELECT_ALL_QUERY.format(table))


def execute_query(query):
    conn = get_database_connection()
    c = conn.cursor()
    c.execute(query)
    conn.commit()


def get_database_connection():
    return sqlite3.connect(DB_PATH)


def show_tables():
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())


def select_single_row(query):
    connection = get_database_connection()
    c = connection.cursor()
    c.execute(query)
    rows = c.fetchall()
    return rows[0] if rows else None


def select_multi_rows(query):
    connection = get_database_connection()
    c = connection.cursor()
    c.execute(query)
    rows = c.fetchall()
    return rows
