import pandas as pd
import joblib
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

model_path = project_folder / "model" / "webguard_model.pkl"
dataset_path = project_folder / "dataset" / "PhiUSIIL_Phishing_URL_Dataset.csv"

# Load model
model = joblib.load(model_path)

# Load dataset
df = pd.read_csv(dataset_path)

# Remove columns not used by the model
columns_to_remove = [
    "FILENAME",
    "URL",
    "Domain",
    "Title"
]

X = df.drop(columns=["label"] + columns_to_remove)

# Make sure everything is numeric
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

# Get feature importance
importance = model.feature_importances_

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 15 important features:\n")

print(feature_importance.head(15).to_string(index=False))