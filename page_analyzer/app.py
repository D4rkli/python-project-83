import os
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


@app.route('/', methods=['POST'])
def submit_url():
    raw_url = request.form.get('url')

    if not validators.url(raw_url) or len(raw_url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    normalized_url = urlparse(raw_url).netloc

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (normalized_url,))
            row = cur.fetchone()
            if row:
                flash('Страница уже существует', 'info')
                return redirect(url_for('get_url', id=row[0]))

            cur.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id',
                (normalized_url, datetime.now())
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('get_url', id=new_id))


@app.route('/urls')
def list_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name FROM urls ORDER BY id DESC')
            urls = cur.fetchall()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def get_url(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, created_at FROM urls WHERE id = %s', (id,))
            url = cur.fetchone()
    return render_template('url_detail.html', url=url)