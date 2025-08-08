import pandas as pd

# Load .txt or .csv with prompt,label format
df = pd.read_csv("data/injection_prompts.txt", names=["prompt", "label"])

# Optional: strip quotes
df["prompt"] = df["prompt"].str.strip('"')

# Map labels to numeric
df["label"] = df["label"].map({"safe": 0, "unsafe": 1})

# Shuffle the dataset for good measure
df = df.sample(frac=1).reset_index(drop=True)

# Check stats
print(" Dataset Loaded")
print(df["label"].value_counts())

# Preview
print(df.head())

# Save to CSV (optional)
df.to_csv("data/cleaned_injection_prompts.csv", index=False)
