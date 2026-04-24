from urllib import urlparse


def normalize_url(url):
    if not url.startwith(("http://", "https://")):
        return f"http://{url}"
    
    return url


def extract_url_parts(url):
    normalized_url = normalize_url(url)
    parsed = urlparse(normalized_url)

    return {
        "normalized_url": normalized_url,
        "scheme": parsed.scheme,
        "hostname": parsed.hostname or "",
        "path": parsed.path or "",
        "query": parsed.query or ""
    }


def is_ip_address_host(hostname):
    parts = hostname.split(".")

    if len(parts) != 4:
        return False
    
    for part in parts:
        if not part.isdigit():
            return False
        
        if not 0 <= int(part) <= 255:
            return False
        
        return True