import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def extract_features(url):

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    domain = parsed.hostname or ""

    features = {}

    # --------------------------------
    # URL FEATURES
    # --------------------------------

    features["URLLength"] = len(url)

    features["DomainLength"] = len(domain)

    # Check whether domain is an IP
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    features["IsDomainIP"] = (
        1 if re.match(ip_pattern, domain) else 0
    )

    # HTTPS
    features["IsHTTPS"] = (
        1 if parsed.scheme == "https" else 0
    )

    # Subdomains
    domain_parts = domain.split(".")

    features["NoOfSubDomain"] = max(
        0,
        len(domain_parts) - 2
    )

    # Letters
    letters = sum(
        character.isalpha()
        for character in url
    )

    features["NoOfLettersInURL"] = letters

    features["LetterRatioInURL"] = (
        letters / len(url)
        if len(url) > 0
        else 0
    )

    # Digits
    digits = sum(
        character.isdigit()
        for character in url
    )

    features["NoOfDegitsInURL"] = digits

    features["DegitRatioInURL"] = (
        digits / len(url)
        if len(url) > 0
        else 0
    )

    # Special URL characters
    features["NoOfEqualsInURL"] = url.count("=")

    features["NoOfQMarkInURL"] = url.count("?")

    features["NoOfAmpersandInURL"] = url.count("&")

    special_chars = sum(
        not character.isalnum()
        for character in url
    )

    features["NoOfOtherSpecialCharsInURL"] = special_chars

    features["SpacialCharRatioInURL"] = (
        special_chars / len(url)
        if len(url) > 0
        else 0
    )

    # --------------------------------
    # WEBSITE CONTENT FEATURES
    # --------------------------------

    try:

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        html = response.text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Lines of HTML
        lines = html.splitlines()

        features["LineOfCode"] = len(lines)

        features["LargestLineLength"] = max(
            [len(line) for line in lines],
            default=0
        )

        # Title
        features["HasTitle"] = (
            1 if soup.title else 0
        )

        # Images
        features["NoOfImage"] = len(
            soup.find_all("img")
        )

        # JavaScript
        features["NoOfJS"] = len(
            soup.find_all("script")
        )

        # CSS
        features["NoOfCSS"] = len(
            soup.find_all(
                "link",
                rel="stylesheet"
            )
        )

        # IFrames
        features["NoOfiFrame"] = len(
            soup.find_all("iframe")
        )

        # Redirects
        features["NoOfURLRedirect"] = len(
            response.history
        )

        # Description
        description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        features["HasDescription"] = (
            1 if description else 0
        )

        # Submit buttons
        submit_buttons = soup.find_all(
            ["button", "input"]
        )

        has_submit = False

        for button in submit_buttons:

            button_type = button.get(
                "type",
                ""
            ).lower()

            if button_type == "submit":
                has_submit = True
                break

        features["HasSubmitButton"] = (
            1 if has_submit else 0
        )

        # Password fields
        password_fields = soup.find_all(
            "input",
            attrs={"type": "password"}
        )

        features["HasPasswordField"] = (
            1 if password_fields else 0
        )

        # --------------------------------
        # LINKS
        # --------------------------------

        self_refs = 0
        external_refs = 0
        empty_refs = 0

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link.get("href", "").strip()

            if href in (
                "",
                "#",
                "javascript:void(0)"
            ):

                empty_refs += 1
                continue

            absolute_url = urljoin(
                response.url,
                href
            )

            link_domain = (
                urlparse(
                    absolute_url
                ).hostname
                or ""
            )

            if link_domain == domain:
                self_refs += 1
            else:
                external_refs += 1

        features["NoOfSelfRef"] = self_refs

        features["NoOfEmptyRef"] = empty_refs

        features["NoOfExternalRef"] = external_refs

    except requests.RequestException:

        print(
            "Warning: Could not retrieve webpage."
        )

    return features