import pandas as pd
from pathlib import Path

# Get the main project folder
project_folder = Path(__file__).resolve().parent.parent

# Build the dataset path
file_path = project_folder / "dataset" / "PhiUSIIL_Phishing_URL_Dataset.csv"

print("Looking for dataset at:")
print(file_path)
print()

# Check whether the file exists
if not file_path.exists():
    print("ERROR: Dataset file was not found!")
    print("Please check the filename and location.")
    exit()

print("Dataset found!")
print("Loading dataset...")

# Load CSV
df = pd.read_csv(file_path)

print()
print("Dataset loaded successfully! ✅")

print()
print("Dataset shape:")
print(df.shape)

print()
print("Column names:")
print(df.columns.tolist())

print()
print("First 5 rows:")
print(df.head())