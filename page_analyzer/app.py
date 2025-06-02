import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime
import validators

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def submit_url():
    raw_url = request.form.get('url')

    if not validators.url(raw_url) or len(raw_url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    parsed_url = urlparse(raw_url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s',
                        (normalized_url,))
            row = cur.fetchone()
            if row:
                flash('Страница уже существует', 'info')
                return redirect(url_for('get_url', id=row[0]))

            cur.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s)'
                ' RETURNING id', (normalized_url, datetime.now())
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('get_url', id=new_id))


@app.route('/urls')
def list_urls():
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
            urls = cur.fetchall()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def get_url(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, created_at FROM urls WHERE id = %s',
                        (id,))
            url = cur.fetchone()
            cur.execute(
                'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC',
                (id,)
            )
            checks = cur.fetchall()
    return render_template('url_detail.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
            row = cur.fetchone()
            if not row:
                flash('Сайт не найден', 'danger')
                return redirect(url_for('list_urls'))
            url_name = row[0]

    try:
        response = requests.get(url_name, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))

    soup = BeautifulSoup(response.text, 'html.parser')

    h1_tag = soup.h1.string.strip() if soup.h1 and soup.h1.string else None
    title_tag = soup.title.string.strip() \
        if soup.title and soup.title.string else None
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag['content'].strip() \
        if desc_tag and desc_tag.has_attr('content') else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO url_checks (url_id, status_code,
                 h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (id, response.status_code, h1_tag,
                  title_tag, description, datetime.now()))
            conn.commit()
            flash('Страница успешно проверена', 'success')

    return redirect(url_for('get_url', id=id))