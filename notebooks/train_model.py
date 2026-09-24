import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import joblib


# --------------------------------------------------
# 1. Find project folder
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder
    / "dataset"
    / "PhiUSIIL_Phishing_URL_Dataset.csv"
)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(file_path)

print("Dataset loaded successfully! ✅")


# --------------------------------------------------
# 3. Remove unnecessary text columns
# --------------------------------------------------

columns_to_remove = [
    "FILENAME",
    "URL",
    "Domain",
    "Title"
]

X = df.drop(
    columns=["label"] + columns_to_remove
)

y = df["label"]


# --------------------------------------------------
# 4. Convert data to numeric
# --------------------------------------------------

X = X.apply(pd.to_numeric, errors="coerce")

# Replace any invalid values with 0
X = X.fillna(0)


# --------------------------------------------------
# 5. Split dataset
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
# 6. Create Random Forest model
# --------------------------------------------------

print()
print("Creating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# 7. Train model
# --------------------------------------------------

print("Training model...")
print("This may take some time...")

model.fit(X_train, y_train)

print("Model training completed! ✅")


# --------------------------------------------------
# 8. Make predictions
# --------------------------------------------------

print()
print("Testing model...")

y_pred = model.predict(X_test)


# --------------------------------------------------
# 9. Calculate accuracy
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print()
print("================================")
print("MODEL RESULTS")
print("================================")

print()
print("Accuracy:", accuracy)

print()
print("Accuracy percentage:", accuracy * 100)


# --------------------------------------------------
# 10. Classification report
# --------------------------------------------------

print()
print("Classification Report:")
print(classification_report(y_test, y_pred))


# --------------------------------------------------
# 11. Confusion matrix
# --------------------------------------------------

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 12. Save model
# --------------------------------------------------

model_folder = project_folder / "model"

model_folder.mkdir(exist_ok=True)

model_path = model_folder / "webguard_model.pkl"

joblib.dump(model, model_path)

print()
print("Model saved successfully! ✅")

print()
print("Model location:")
print(model_path)