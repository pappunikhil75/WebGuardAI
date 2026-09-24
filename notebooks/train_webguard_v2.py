import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

dataset_path = (
    project_folder
    / "dataset"
    / "PhiUSIIL_Phishing_URL_Dataset.csv"
)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully! ✅")


# --------------------------------------------------
# 3. Features our live analyzer can reproduce
# --------------------------------------------------

features = [
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


# --------------------------------------------------
# 4. Check that all features exist
# --------------------------------------------------

missing_features = [
    feature
    for feature in features
    if feature not in df.columns
]

if missing_features:

    print("ERROR: These features are missing:")
    print(missing_features)

    exit()


# --------------------------------------------------
# 5. Create X and y
# --------------------------------------------------

X = df[features].copy()

y = df["label"]


# --------------------------------------------------
# 6. Convert to numeric
# --------------------------------------------------

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.fillna(0)


# --------------------------------------------------
# 7. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print()
print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# --------------------------------------------------
# 8. Create model
# --------------------------------------------------

print()
print("Creating Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# 9. Train
# --------------------------------------------------

print("Training model...")
print("Please wait...")

model.fit(
    X_train,
    y_train
)

print("Training completed! ✅")


# --------------------------------------------------
# 10. Test
# --------------------------------------------------

print()
print("Testing model...")

y_pred = model.predict(X_test)


# --------------------------------------------------
# 11. Accuracy
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print()
print("===================================")
print("WEBGUARD AI V2 RESULTS")
print("===================================")

print()

print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"Accuracy percentage: {accuracy * 100:.2f}%"
)


# --------------------------------------------------
# 12. Classification report
# --------------------------------------------------

print()
print("Classification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# --------------------------------------------------
# 13. Confusion matrix
# --------------------------------------------------

print()
print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# --------------------------------------------------
# 14. Save model
# --------------------------------------------------

model_folder = (
    project_folder / "model"
)

model_folder.mkdir(
    exist_ok=True
)

model_path = (
    model_folder
    / "webguard_model_v2.pkl"
)

joblib.dump(
    model,
    model_path
)

print()
print("Model saved! ✅")

print(
    model_path
)