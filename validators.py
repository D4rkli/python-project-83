import validators

def is_valid_url(url):
    return validators.url(url) and len(url) <= 255