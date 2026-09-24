import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from backend.feature_extractor import extract_features


DATASET_PATH = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

FEATURES = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "IsHTTPS",
    "NoOfSubDomain",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "LineOfCode",
    "LargestLineLength",
    "HasTitle",
    "NoOfImage",
    "NoOfJS",
    "NoOfCSS",
    "NoOfiFrame",
    "NoOfURLRedirect",
    "HasDescription",
    "HasSubmitButton",
    "HasPasswordField",
    "NoOfSelfRef",
    "NoOfEmptyRef",
    "NoOfExternalRef"
]


url = "https://www.google.com"

print("Loading dataset...")
df = pd.read_csv(DATASET_PATH)

print("Extracting live features...")
live = extract_features(url)

print("\n===================================")
print("LIVE FEATURE VALUES")
print("===================================")

for feature in FEATURES:
    print(f"{feature}: {live[feature]}")


print("\n===================================")
print("DATASET STATISTICS")
print("===================================")

for feature in FEATURES:
    values = pd.to_numeric(
        df[feature],
        errors="coerce"
    )

    print(
        f"{feature}: "
        f"min={values.min():.2f}, "
        f"mean={values.mean():.2f}, "
        f"max={values.max():.2f}"
    )