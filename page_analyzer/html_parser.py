from bs4 import BeautifulSoup


def parse_html(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.h1.get_text(strip=True) if soup.h1 and soup.h1.string else None
    title = soup.title.get_text(strip=True) if soup.title else None

    desc_tag = soup.find(name='meta', attrs={'name': 'description'})
    if desc_tag and desc_tag.has_attr('content'):
        description = desc_tag['content'].strip()
    else:
        description = None

    return h1, title, description
