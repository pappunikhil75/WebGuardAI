import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


DATASET_PATH = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"
MODEL_PATH = "model/webguard_url_model.pkl"


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
    "SpacialCharRatioInURL"
]


print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")

print("\nPreparing URL features...")

X = df[FEATURES].copy()
y = df["label"]


# Convert everything to numeric
X = X.apply(pd.to_numeric, errors="coerce")

# Replace missing values
X = X.fillna(0)


print("Training data preparation completed!")

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


print("\nCreating Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)


print("Training model...")
print("Please wait...")

model.fit(X_train, y_train)

print("Training completed! ✅")


print("\nTesting model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n===================================")
print("WEBGUARD AI URL MODEL RESULTS")
print("===================================")

print("Accuracy:", accuracy)
print("Accuracy percentage:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Save model

joblib.dump(model, MODEL_PATH)

print("\nURL model saved! ✅")
print(MODEL_PATH)