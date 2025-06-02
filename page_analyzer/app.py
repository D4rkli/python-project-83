from db import get_connection, find_url_by_name, insert_url, get_all_urls, get_url_with_checks, insert_check, find_url_by_id
from flask import Flask, render_template, request, redirect, url_for, flash
from parser import parse_website_content
from validators import is_valid_url
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def submit_url():
    raw_url = request.form.get('url')

    if not is_valid_url(raw_url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    parsed_url = urlparse(raw_url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    existing_url = find_url_by_name(normalized_url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', id=existing_url[0]))

    new_id = insert_url(normalized_url, datetime.now())
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=new_id))


@app.route('/urls')
def list_urls():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def get_url(id):
    url, checks = get_url_with_checks(id)
    return render_template('url_detail.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url_data = find_url_by_id(id)
    if not url_data:
        flash('Сайт не найден', 'danger')
        return redirect(url_for('list_urls'))

    url_name = url_data[0]

    try:
        result = parse_website_content(url_name)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))

    insert_check(id, result, datetime.now())
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))

