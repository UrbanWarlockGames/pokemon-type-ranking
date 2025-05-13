import pandas as pd
import os

# Determine the actual path of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define base filenames
combinations = {
    "monotype": ("monotype_combinations.csv", "monotype_combinations_defence.csv"),
    "dualtype": ("dualtype_combinations.csv", "dualtype_combinations_defence.csv"),
    "tripletype": ("tripletype_combinations.csv", "tripletype_combinations_defence.csv"),
}

def build_key(row, cols):
    return tuple(row[col] for col in cols if col in row and pd.notnull(row[col]))

for label, (main_file, defence_file) in combinations.items():
    main_path = os.path.join(script_dir, main_file)
    defence_path = os.path.join(script_dir, defence_file)

    if not os.path.exists(main_path):
        print(f"Main file missing: {main_path}")
        continue
    if not os.path.exists(defence_path):
        print(f"Defence file missing: {defence_path}")
        continue

    print(f"Processing {label}...")

    main_df = pd.read_csv(main_path)
    defence_df = pd.read_csv(defence_path)

    key_cols = [col for col in ["First Type", "Second Type", "Third Type"] if col in main_df.columns]

    main_df["combo_key"] = main_df.apply(lambda row: build_key(row, key_cols), axis=1)
    defence_df["combo_key"] = defence_df.apply(lambda row: build_key(row, key_cols), axis=1)

    defence_score_map = defence_df.set_index("combo_key")["Defensive Score"].to_dict()
    main_df["Defensive Score"] = main_df["combo_key"].map(defence_score_map)

    main_df.drop(columns=["combo_key"], inplace=True)

    output_file = os.path.join(script_dir, f"{label}_combinations.csv")
    main_df.to_csv(output_file, index=False)
    print(f"Updated file saved: {output_file}")
