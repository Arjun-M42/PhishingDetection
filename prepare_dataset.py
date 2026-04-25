import pandas as pd

def load_url_file(path):
    df = pd.read_csv(path)

    print(f"{path} columns:", df.columns)

    # Try common column names
    for col in df.columns:
        if "url" in col.lower() or "domain" in col.lower():
            return df[col].to_frame(name="url")

    # If no column found → assume first column is URL
    return df.iloc[:, 0].to_frame(name="url")


# Load datasets safely
benign = load_url_file("dataset/Benign_list_big_final.csv")
online = load_url_file("dataset/online-valid.csv")
legit = load_url_file("dataset/legitimate.csv")
phishing = load_url_file("dataset/phishing.csv")

# Add labels
benign["label"] = 0
online["label"] = 0
legit["label"] = 0
phishing["label"] = 1

# Combine
df = pd.concat([benign, online, legit, phishing], ignore_index=True)

# Shuffle
df = df.sample(frac=1).reset_index(drop=True)

# Save
df.to_csv("dataset/final_url_dataset.csv", index=False)

print("Final dataset created successfully!")
print(df.head())