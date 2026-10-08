import pandas as pd
import numpy as np

# Load datasets
track_df = pd.read_csv('data/player_track_backgrounds.csv')
combine_df = pd.read_csv('data/combine_results.csv')
players_df = pd.read_csv('data/players.csv')
madden_df = pd.read_csv('data/rookies_with_madden.csv')

# Merge
df = pd.merge(track_df, combine_df[['nfl_id', 'forty', 'ten_yd_split', 'combine_weight', 'combine_height', 'vertical', 'broad_jump', 'three_cone', 'short_shuttle']], on='nfl_id', how='left')

print(f"Total players in merged track analysis: {len(df)}")
print(f"Track background count: {df['has_track_background'].sum()}")

# Position breakdown of track athletes
print("\n--- TRACK ATHLETES BY POSITION ---")
print(df[df['has_track_background']]['nfl_position'].value_counts())

# Compare 40-yard dash: Track vs Non-Track for skill positions (WR, CB, SS, FS, RB)
skill_positions = ['WR', 'CB', 'SS', 'FS', 'RB']
skills = df[df['nfl_position'].isin(skill_positions)].dropna(subset=['forty'])

track_skills = skills[skills['has_track_background']]['forty']
non_track_skills = skills[~skills['has_track_background']]['forty']

print("\n--- 40-YARD DASH IN SKILL POSITIONS (WR, DB, RB) ---")
print(f"Track Athletes: N={len(track_skills)}, Mean 40={track_skills.mean():.3f}s, Median={track_skills.median():.3f}s")
print(f"Non-Track Athletes: N={len(non_track_skills)}, Mean 40={non_track_skills.mean():.3f}s, Median={non_track_skills.median():.3f}s")
print(f"Speed Difference: Track athletes are {non_track_skills.mean() - track_skills.mean():.3f}s FASTER on average!")

# Check 10-yard split ratio (First 10 yards vs next 30 yards)
# Flying 30 = 40_time - 10_yd_split
skills = skills.dropna(subset=['forty', 'ten_yd_split']).copy()
skills['flying_30'] = skills['forty'] - skills['ten_yd_split']
skills['burst_ratio'] = skills['ten_yd_split'] / skills['forty']

print("\n--- ACCELERATION vs TOP SPEED (10-YD SPLIT vs FLYING 30) ---")
track_split = skills[skills['has_track_background']]
non_track_split = skills[~skills['has_track_background']]

print(f"Track Flying 30 Mean: {track_split['flying_30'].mean():.3f}s")
print(f"Non-Track Flying 30 Mean: {non_track_split['flying_30'].mean():.3f}s")
print(f"Track 10-Yard Split Mean: {track_split['ten_yd_split'].mean():.3f}s")
print(f"Non-Track 10-Yard Split Mean: {non_track_split['ten_yd_split'].mean():.3f}s")

# Check Madden ratings comparison
if 'speed' in madden_df.columns:
    m_df = pd.merge(df, madden_df[['nfl_id', 'speed', 'acceleration', 'overallrating']], on='nfl_id', how='inner')
    m_skills = m_df[m_df['nfl_position'].isin(skill_positions)]
    print("\n--- MADDEN RATINGS: TRACK vs NON-TRACK ---")
    print(f"Track Madden Speed Mean: {m_skills[m_skills['has_track_background']]['speed'].mean():.2f}")
    print(f"Non-Track Madden Speed Mean: {m_skills[~m_skills['has_track_background']]['speed'].mean():.2f}")

# Top Track Stars
print("\n--- NOTABLE CONFIRMED TRACK ATHLETES ---")
top_track = df[df['has_track_background']][['display_name', 'nfl_position', 'college_name', 'forty', 'ten_yd_split', 'track_keywords']].sort_values(by='forty').head(10)
print(top_track.to_string(index=False))
