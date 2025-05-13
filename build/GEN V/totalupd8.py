import pandas as pd
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define relative filenames
filenames = [
    "monotype_combinations.csv",
    "dualtype_combinations.csv",
    "tripletype_combinations.csv"
]

for fname in filenames:
    full_path = os.path.join(script_dir, fname)

    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue

    df = pd.read_csv(full_path)

    if 'Offensive Score' in df.columns and 'Defensive Score' in df.columns:
        df['Total Score'] = df['Offensive Score'] + df['Defensive Score']
        df.to_csv(full_path, index=False)
        print(f"Updated: {fname}")
    else:
        print(f"Skipped {fname}: Missing required score columns.")
