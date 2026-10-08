import pandas as pd
import glob
import os

print("Loading Madden Parquet files...")
# Load Madden 2024 and 2025 (which correspond to the rookie classes we're looking at)
files = ['madden_data/data/madden/dataset/2024.parquet', 'madden_data/data/madden/dataset/2025.parquet']

df_list = []
for file in files:
    if os.path.exists(file):
        df = pd.read_parquet(file)
        df_list.append(df)

if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Select columns most relevant to the Combine tracking data
    cols_to_keep = [
        'madden_id', 'fullname', 'position', 'season', 'team', 
        'overallrating', 'speed', 'acceleration', 'agility', 
        'changeofdirection', 'awareness', 'jumping', 'strength'
    ]
    
    # Filter only available columns
    cols = [c for c in cols_to_keep if c in combined_df.columns]
    extract = combined_df[cols]
    
    # Save to CSV in the root
    out_path = 'madden_extracted_ratings.csv'
    extract.to_csv(out_path, index=False)
    
    print(f"Success! Extracted {len(extract)} player rating records to {out_path}.")
    print("\nPreview:")
    print(extract.head())
else:
    print("Could not find the parquet files.")
