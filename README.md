### Hexlet tests and linter status:
[![Actions Status](https://github.com/D4rkli/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/D4rkli/python-project-83/actions)

# 🔍 Page Analyzer

**Page Analyzer** — это веб-приложение, которое позволяет добавлять сайты, запускать их проверки и сохранять результаты (код ответа, заголовки, описание). Подходит для анализа SEO-данных и доступности сайтов.

## Проверить: [Website](https://python-project-83-s5yf.onrender.com/)

## 🚀 Возможности
- Добавление и нормализация URL-адресов
- Проверка сайтов по HTTP-запросу
- Извлечение и сохранение:
  - Статуса ответа (HTTP Status)
  - `<title>`
  - `<h1>`
  - `<meta name="description">`
- Просмотр истории всех проверок
- Удобный интерфейс с Bootstrap 5

---

## 🛠 Стек технологий

- Python 3.13
- Flask
- PostgreSQL
- BeautifulSoup
- Docker / Docker Compose
- Playwright + Pytest (для end-to-end тестирования)

---

## ⚙️ Установка

```bash
git clone https://github.com/your_username/page-analyzer.git
cd page-analyzer
make setup
make run
