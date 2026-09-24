import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Find the project folder
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

# Dataset path
file_path = project_folder / "dataset" / "PhiUSIIL_Phishing_URL_Dataset.csv"


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(file_path)

print("Dataset loaded successfully! ✅")
print()


# --------------------------------------------------
# 3. Basic information
# --------------------------------------------------

print("Dataset shape:")
print(df.shape)

print()

print("Columns:")
print(df.columns.tolist())

print()


# --------------------------------------------------
# 4. Check missing values
# --------------------------------------------------

print("Checking missing values...")

missing_values = df.isnull().sum()

print(missing_values[missing_values > 0])

print()


# --------------------------------------------------
# 5. Check label distribution
# --------------------------------------------------

print("Label distribution:")

print(df["label"].value_counts())

print()


# --------------------------------------------------
# 6. Separate features and target
# --------------------------------------------------

X = df.drop("label", axis=1)

y = df["label"]

print("Features shape:")
print(X.shape)

print()

print("Target shape:")
print(y.shape)
# --------------------------------------------------
# 8. Split dataset into training and testing
# --------------------------------------------------

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training data:")
print(X_train.shape)

print()

print("Testing data:")
print(X_test.shape)

print()

print("Training labels:")
print(y_train.shape)

print()

print("Testing labels:")
print(y_test.shape)
# --------------------------------------------------
# 8. Split dataset into training and testing
# --------------------------------------------------

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print()
print("Training data:")
print(X_train.shape)

print()
print("Testing data:")
print(X_test.shape)

print()
print("Training labels:")
print(y_train.shape)

print()
print("Testing labels:")
print(y_test.shape)