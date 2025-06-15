import os
import requests
from page_analyzer.html_parser import parse_html
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators

import db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def submit_url():
    raw_url = request.form.get('url')

    if not validators.url(raw_url) or len(raw_url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    parsed = urlparse(raw_url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}"

    existing = db.get_url_by_name(normalized_url)
    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', id=existing[0]))

    new_id = db.insert_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=new_id))


@app.route('/urls')
def list_urls():
    urls = db.get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def get_url(id):
    url = db.get_url_by_id(id)
    checks = db.get_url_checks_by_id(id)
    return render_template('url_detail.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url_name = db.get_url_name_by_id(id)
    if not url_name:
        flash('Сайт не найден', 'danger')
        return redirect(url_for('list_urls'))

    try:
        response = requests.get(url_name, timeout=10)
        response.raise_for_status()
        h1, title, description = parse_html(response.text)
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))

    db.insert_url_check(id, response.status_code, h1, title, description)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
