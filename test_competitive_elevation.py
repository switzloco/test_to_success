import pandas as pd
import numpy as np

# Load combine tracking and player data
df = pd.read_csv('data/combine_tracking.csv', usecols=['draft_year', 'event_id', 'nfl_id', 'drill_type', 'attempt', 'time', 's', 'a'])
df = df.dropna(subset=['nfl_id'])
df['nfl_id'] = df['nfl_id'].astype(int)
df['datetime'] = pd.to_datetime(df['time'])

# Filter to 40-Yard Dash Attempt 1
forty = df[(df['drill_type'] == 'FORTY_YARD_DASH') & (df['attempt'] == 1)]
runs = forty.groupby(['draft_year', 'nfl_id', 'event_id']).agg(
    start_time=('datetime', 'min'),
    max_speed=('s', 'max'),
    max_accel=('a', 'max')
).reset_index()

# Load players and combine results to get weight and position
players = pd.read_csv('data/players.csv')
combine = pd.read_csv('data/combine_results.csv')

runs = pd.merge(runs, players[['nfl_id', 'display_name', 'nfl_position', 'draft_year', 'college_name']], on=['nfl_id', 'draft_year'])
runs = pd.merge(runs, combine[['nfl_id', 'combine_weight', 'forty', 'ten_yd_split']], on='nfl_id')

# Sort strictly by chronological start time within each draft year to recreate the exact queue
runs = runs.sort_values(by=['draft_year', 'start_time']).reset_index(drop=True)

# Calculate "Speed Over Expected" based on position and weight
# Simple baseline model: expected max speed = f(weight, position)
runs['weight_centered'] = runs['combine_weight'] - runs['combine_weight'].mean()
# Group mean by position
pos_mean = runs.groupby('nfl_position')['max_speed'].transform('mean')
runs['expected_max_speed'] = pos_mean - 0.015 * runs['weight_centered']
runs['speed_over_expected'] = runs['max_speed'] - runs['expected_max_speed']

# Look at the PRIOR runner in the queue
runs['prev_player_name'] = runs.groupby('draft_year')['display_name'].shift(1)
runs['prev_max_speed'] = runs.groupby('draft_year')['max_speed'].shift(1)
runs['prev_forty'] = runs.groupby('draft_year')['forty'].shift(1)
runs['time_since_prev_run_sec'] = runs.groupby('draft_year')['start_time'].diff().dt.total_seconds()

# Filter to runs that occurred within 5 minutes of the previous runner (same session group)
queue_runs = runs[(runs['time_since_prev_run_sec'] > 0) & (runs['time_since_prev_run_sec'] < 300)].copy()

print(f"Total queue pairs analyzed (runners within 5 mins of each other): {len(queue_runs)}")

# Split previous runner into: BLAZING FAST (< 4.40 40) vs NORMAL vs SLOW (> 4.60)
queue_runs['prev_tier'] = pd.cut(queue_runs['prev_forty'], bins=[0, 4.40, 4.55, 4.75, 6.0], labels=['Blazing (<4.40)', 'Fast (4.40-4.55)', 'Average (4.55-4.75)', 'Heavy (>4.75)'])

print("\n--- PERFORMANCE OVER EXPECTED BY PREVIOUS RUNNER'S SPEED ---")
tier_summary = queue_runs.groupby('prev_tier')['speed_over_expected'].agg(['count', 'mean', 'median'])
print(tier_summary.round(4))

# Correlation between predecessor speed and runner's speed over expected
corr_stimulus = queue_runs['prev_max_speed'].corr(queue_runs['speed_over_expected'])
print(f"\nCorrelation between Predecessor Max Speed and Runner's Speed Over Expected: {corr_stimulus:.3f}")

# Who surged the most after watching a blazing run?
blazing_follows = queue_runs[queue_runs['prev_forty'] < 4.42].sort_values(by='speed_over_expected', ascending=False)
print("\n--- TOP ATHLETES WHO SURGED OVER EXPECTED FOLLOWING A BLAZING RUN ---")
print(blazing_follows[['display_name', 'nfl_position', 'forty', 'prev_player_name', 'prev_forty', 'speed_over_expected']].head(5).to_string(index=False))
