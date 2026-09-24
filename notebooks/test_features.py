import sys
from pathlib import Path


project_folder = Path(__file__).resolve().parent.parent

sys.path.append(str(project_folder))


from backend.feature_extractor import extract_features


url = input("Enter URL: ")

features = extract_features(url)


print("\nExtracted Features")
print("=" * 50)

for name, value in features.items():
    print(f"{name}: {value}")


print()
print("Total features extracted:", len(features))