import re
import ipaddress
from urllib.parse import urlparse


def extract_url_features(url):

    # Make sure URL has a scheme
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc

    # Remove username/password if present
    if "@" in domain:
        domain = domain.split("@")[-1]

    # Remove port
    domain = domain.split(":")[0]

    # -----------------------------
    # Basic URL features
    # -----------------------------

    url_length = len(url)

    domain_length = len(domain)

    # Check whether domain is an IP address
    is_domain_ip = 0

    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0

    # HTTPS
    is_https = 1 if parsed.scheme == "https" else 0

    # Subdomains
    domain_parts = domain.split(".")

    if len(domain_parts) >= 3:
        no_of_subdomain = len(domain_parts) - 2
    else:
        no_of_subdomain = 0

    # -----------------------------
    # Character-based features
    # -----------------------------

    letters = sum(c.isalpha() for c in url)

    digits = sum(c.isdigit() for c in url)

    equals = url.count("=")

    question_marks = url.count("?")

    ampersands = url.count("&")

    # Characters that aren't letters,
    # digits, slash, dot, colon or hyphen
    other_special = sum(
        1 for c in url
        if not (
            c.isalpha()
            or c.isdigit()
            or c in "/.:_-"
        )
    )

    # Ratios
    letter_ratio = (
        letters / url_length
        if url_length > 0
        else 0
    )

    digit_ratio = (
        digits / url_length
        if url_length > 0
        else 0
    )

    special_ratio = (
        other_special / url_length
        if url_length > 0
        else 0
    )

    # -----------------------------
    # Suspicious URL patterns
    # -----------------------------

    has_at_symbol = 1 if "@" in url else 0

    has_double_slash_redirect = (
        1 if "//" in url[8:] else 0
    )

    has_hex_encoding = (
        1 if re.search(r"%[0-9a-fA-F]{2}", url)
        else 0
    )

    has_punycode = (
        1 if "xn--" in domain.lower()
        else 0
    )

    has_ip_in_url = is_domain_ip

    # Number of hyphens
    no_of_hyphens = url.count("-")

    # Number of dots
    no_of_dots = url.count(".")

    # Number of slashes
    no_of_slashes = url.count("/")

    # Number of path components
    path = parsed.path

    path_depth = len(
        [x for x in path.split("/") if x]
    )

    # Query length
    query_length = len(parsed.query)

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "is_domain_ip": is_domain_ip,
        "is_https": is_https,
        "no_of_subdomain": no_of_subdomain,
        "letters": letters,
        "letter_ratio": letter_ratio,
        "digits": digits,
        "digit_ratio": digit_ratio,
        "equals": equals,
        "question_marks": question_marks,
        "ampersands": ampersands,
        "other_special": other_special,
        "special_ratio": special_ratio,
        "has_at_symbol": has_at_symbol,
        "has_double_slash_redirect": has_double_slash_redirect,
        "has_hex_encoding": has_hex_encoding,
        "has_punycode": has_punycode,
        "no_of_hyphens": no_of_hyphens,
        "no_of_dots": no_of_dots,
        "no_of_slashes": no_of_slashes,
        "path_depth": path_depth,
        "query_length": query_length
    }