import validators

def is_valid_url(url):
    return bool(url) and validators.url(url) and len(url) <= 255