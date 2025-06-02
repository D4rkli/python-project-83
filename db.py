import psycopg2
from datetime import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def get_url_by_name(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (name,))
            return cur.fetchone()

def insert_url(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id',
                (name, datetime.now())
            )
            return cur.fetchone()[0]

def get_all_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT urls.id, urls.name,
                       MAX(url_checks.created_at) AS last_check,
                       MAX(url_checks.status_code) AS status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id
                ORDER BY urls.id DESC
            ''')
            return cur.fetchall()

def get_url_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, created_at FROM urls WHERE id = %s', (id,))
            return cur.fetchone()

def get_url_checks_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC', (id,))
            return cur.fetchall()

def get_url_name_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
            row = cur.fetchone()
            return row[0] if row else None

def insert_url_check(url_id, status_code, h1, title, description):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (url_id, status_code, h1, title, description, datetime.now()))
            conn.commit()
