import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def analyze_url(url):

    print("\nAnalyzing:")
    print(url)

    # Add HTTPS if the user doesn't provide it
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # -----------------------------
        # URL information
        # -----------------------------

        parsed_url = urlparse(response.url)

        domain = parsed_url.hostname or ""

        print("\nBasic information:")
        print("Final URL:", response.url)
        print("Domain:", domain)
        print("HTTPS:", parsed_url.scheme == "https")

        # -----------------------------
        # Webpage information
        # -----------------------------

        title = ""

        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        images = soup.find_all("img")
        scripts = soup.find_all("script")
        stylesheets = soup.find_all("link", rel="stylesheet")
        iframes = soup.find_all("iframe")
        forms = soup.find_all("form")
        links = soup.find_all("a")

        print("\nPage information:")
        print("Page title:", title)
        print("Lines of HTML:", len(html.splitlines()))
        print("Images:", len(images))
        print("JavaScript:", len(scripts))
        print("CSS:", len(stylesheets))
        print("IFrames:", len(iframes))
        print("Forms:", len(forms))
        print("Links:", len(links))

        print("\nHTTP information:")
        print("Status code:", response.status_code)
        print("Redirects:", len(response.history))

        return {
            "url": response.url,
            "domain": domain,
            "title": title,
            "html_length": len(html),
            "line_count": len(html.splitlines()),
            "images": len(images),
            "scripts": len(scripts),
            "css": len(stylesheets),
            "iframes": len(iframes),
            "forms": len(forms),
            "links": len(links),
            "status_code": response.status_code,
            "redirects": len(response.history)
        }

    except requests.RequestException as e:

        print("\nCould not retrieve website.")
        print("Reason:", e)

        return None


# -----------------------------------------
# Run program
# -----------------------------------------

if __name__ == "__main__":

    website = input("\nEnter website URL: ")

    result = analyze_url(website)

    if result:
        print("\nAnalysis completed successfully! ✅")