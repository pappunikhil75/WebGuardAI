import pandas as pd


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
    "SpacialCharRatioInURL"
]


print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded!")

print("\n===================================")
print("LABEL COUNTS")
print("===================================")

print(df["label"].value_counts())

print("\n0 = Phishing")
print("1 = Legitimate")


print("\n===================================")
print("FEATURE MEANS BY LABEL")
print("===================================")

means = df.groupby("label")[FEATURES].mean().T

print(means.to_string())


print("\n===================================")
print("SAMPLE LEGITIMATE URLS")
print("===================================")

legitimate = df[df["label"] == 1]

print(
    legitimate[
        ["URL"] + FEATURES
    ].head(10).to_string(index=False)
)


print("\n===================================")
print("SAMPLE PHISHING URLS")
print("===================================")

phishing = df[df["label"] == 0]

print(
    phishing[
        ["URL"] + FEATURES
    ].head(10).to_string(index=False)
)