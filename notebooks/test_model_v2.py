import pandas as pd
import joblib

DATASET_PATH = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"
MODEL_PATH = "model/webguard_model_v2.pkl"

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

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded!")

model = joblib.load(MODEL_PATH)

# Take the first row
row = df.iloc[0]

X = pd.DataFrame([row[FEATURES]])

prediction = model.predict(X)[0]
probabilities = model.predict_proba(X)[0]

print("\n===================================")
print("MODEL DIRECT TEST")
print("===================================")

print("URL:", row["URL"])
print("Actual label:", row["label"])
print("Predicted label:", prediction)

print(
    "Phishing probability:",
    round(probabilities[0] * 100, 2),
    "%"
)

print(
    "Legitimate probability:",
    round(probabilities[1] * 100, 2),
    "%"
)

if prediction == 1:
    print("Prediction: LEGITIMATE")
else:
    print("Prediction: PHISHING")