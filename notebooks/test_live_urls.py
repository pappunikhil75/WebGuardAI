import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from backend.predictor import predict_url


urls = [
    "https://www.google.com",
    "https://www.microsoft.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.amazon.com"
]


print("\n===================================")
print("WEBGUARD AI LIVE URL TEST")
print("===================================")


for url in urls:

    print("\nTesting:", url)

    try:
        result = predict_url(url)

        print("Prediction:", result["prediction"])
        print(
            "Phishing Probability:",
            result["phishing_probability"],
            "%"
        )
        print(
            "Legitimate Probability:",
            result["legitimate_probability"],
            "%"
        )

    except Exception as e:

        print("ERROR:", e)