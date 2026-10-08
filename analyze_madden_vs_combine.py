import pandas as pd
import numpy as np

# Load datasets
players = pd.read_csv('data/players.csv')
combine = pd.read_csv('data/combine_results.csv')
madden = pd.read_csv('madden_extracted_ratings.csv')

print(f"Total rookie cohort players: {len(players)}")
print(f"Combine results rows: {len(combine)}")
print(f"Madden rating rows: {len(madden)}")

# Merge players with combine results
rookie_df = pd.merge(players, combine, on=['nfl_id', 'draft_year'], how='left')

# Clean display names for matching
rookie_df['clean_name'] = rookie_df['display_name'].str.strip().str.lower()
madden['clean_name'] = madden['fullname'].str.strip().str.lower()

# For Madden, get the most recent rating for each player (or their rookie year)
madden_latest = madden.sort_values(by='season', ascending=False).drop_duplicates(subset=['clean_name'])

# Merge rookie cohort with Madden ratings
merged = pd.merge(rookie_df, madden_latest, on='clean_name', how='inner')
print(f"Successfully matched {len(merged)} of {len(rookie_df)} rookies to Madden ratings!")

# Print position breakdown of matches
print("\nMatched players by position:")
print(merged['nfl_position'].value_counts())

# Analysis 1: 40-yard dash vs Madden Speed
has_40 = merged.dropna(subset=['forty', 'speed'])
corr_speed = has_40['forty'].corr(has_40['speed'])
print(f"\nCorrelation between 40-yard dash (lower is faster) and Madden Speed: {corr_speed:.3f}")

# Analysis 2: 10-yard split vs Madden Acceleration
has_10yd = merged.dropna(subset=['ten_yd_split', 'acceleration'])
corr_accel = has_10yd['ten_yd_split'].corr(has_10yd['acceleration'])
print(f"Correlation between 10-yard split and Madden Acceleration: {corr_accel:.3f}")

# Analysis 3: 3-cone vs Madden Agility / Change of Direction
has_3cone = merged.dropna(subset=['three_cone', 'changeofdirection'])
if len(has_3cone) > 0:
    corr_cod = has_3cone['three_cone'].corr(has_3cone['changeofdirection'])
    print(f"Correlation between 3-Cone drill and Madden Change of Direction: {corr_cod:.3f}")

# Finding the Biggest Discrepancies:
# Standardize 40 time (invert so higher is faster) and Madden Speed to z-scores
has_40 = has_40.copy()
has_40['z_forty_speed'] = - (has_40['forty'] - has_40['forty'].mean()) / has_40['forty'].std()
has_40['z_madden_speed'] = (has_40['speed'] - has_40['speed'].mean()) / has_40['speed'].std()
has_40['speed_gap'] = has_40['z_forty_speed'] - has_40['z_madden_speed']

print("\n--- TOP 5 PLAYERS WHERE MADDEN 'UNDERRATED' SPEED RELATIVE TO COMBINE 40 ---")
top_underrated = has_40.sort_values(by='speed_gap', ascending=False)[
    ['display_name', 'nfl_position', 'draft_year', 'forty', 'speed', 'speed_gap']
].head(5)
print(top_underrated.to_string(index=False))

print("\n--- TOP 5 PLAYERS WHERE MADDEN 'OVERRATED' SPEED RELATIVE TO COMBINE 40 ---")
top_overrated = has_40.sort_values(by='speed_gap', ascending=True)[
    ['display_name', 'nfl_position', 'draft_year', 'forty', 'speed', 'speed_gap']
].head(5)
print(top_overrated.to_string(index=False))

# Save the matched dataset
merged.to_csv('data/rookies_with_madden.csv', index=False)
print("\nSaved matched dataset to data/rookies_with_madden.csv")
