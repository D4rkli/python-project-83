from bs4 import BeautifulSoup

def parse_html(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.h1.string.strip() if soup.h1 and soup.h1.string else None
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag and desc_tag.has_attr('content') else None

    return h1, title, description