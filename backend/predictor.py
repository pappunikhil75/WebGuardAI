import os
import sys
import joblib
import pandas as pd

# Add notebooks folder to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

NOTEBOOKS_PATH = os.path.join(
    PROJECT_ROOT,
    "notebooks"
)

sys.path.append(NOTEBOOKS_PATH)

from url_features import extract_url_features


# Model location
MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "model",
    "webguard_live_url_model.pkl"
)


# Load trained model
model = joblib.load(MODEL_PATH)


def predict_url(url):

    # Extract the same 23 features
    # used during model training
    features = extract_url_features(url)

    # Convert features to DataFrame
    X = pd.DataFrame([features])

    # Prediction
    prediction = model.predict(X)[0]

    # Probabilities
    probabilities = model.predict_proba(X)[0]

    phishing_probability = float(probabilities[0])
    legitimate_probability = float(probabilities[1])


    # Dataset labels:
    # 0 = phishing
    # 1 = legitimate

    if prediction == 1:
        result = "LEGITIMATE"
    else:
        result = "PHISHING"


    # Risk category
    if phishing_probability < 0.20:

        risk_level = "LOW"

    elif phishing_probability < 0.60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    return {
        "url": url,
        "prediction": result,
        "risk_level": risk_level,
        "phishing_probability": round(
            phishing_probability * 100,
            2
        ),
        "legitimate_probability": round(
            legitimate_probability * 100,
            2
        )
    }


# Direct terminal testing
if __name__ == "__main__":

    test_url = input(
        "Enter URL to analyze: "
    )

    try:

        result = predict_url(test_url)

        print("\n===================================")
        print("WEBGUARD AI LIVE URL MODEL")
        print("===================================")

        print(
            "URL:",
            result["url"]
        )

        print(
            "Prediction:",
            result["prediction"]
        )

        print(
            "Risk Level:",
            result["risk_level"]
        )

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

        print("\nError analyzing URL:")
        print(e)