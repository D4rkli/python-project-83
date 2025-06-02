import requests
from bs4 import BeautifulSoup

def fetch_url_data(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    h1_tag = soup.h1.string.strip() if soup.h1 and soup.h1.string else None
    title_tag = soup.title.string.strip() if soup.title and soup.title.string else None
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag and desc_tag.has_attr('content') else None

    return response, h1_tag, title_tag, description