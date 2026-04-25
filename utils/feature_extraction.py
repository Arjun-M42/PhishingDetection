import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    # 1 Have_IP
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)

    # 2 Have_At
    features.append(1 if "@" in url else 0)

    # 3 URL_Length
    if len(url) < 54:
        features.append(0)
    elif len(url) <= 75:
        features.append(1)
    else:
        features.append(2)

    # 4 URL_Depth
    features.append(len(parsed.path.split('/')))

    # 5 Redirection
    features.append(1 if url.count("//") > 1 else 0)

    # 6 Prefix/Suffix
    features.append(1 if "-" in domain else 0)

    # 7 Subdomains
    features.append(domain.count("."))

    # 8 HTTPS
    features.append(1 if parsed.scheme == "https" else 0)

    # 9–16 extra features
    features.append(len(url))
    features.append(url.count("."))
    features.append(sum(c.isdigit() for c in url))
    features.append(len(re.findall(r'[^\w]', url)))
    features.append(len(domain))
    features.append(1 if "https" in domain else 0)
    features.append(len(parsed.path))
    features.append(1 if "?" in url else 0)

    return features