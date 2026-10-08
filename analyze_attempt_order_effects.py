import pandas as pd
import numpy as np

# Load tracking data for 40-yard dash specifically
df = pd.read_csv('data/combine_tracking.csv', usecols=['draft_year', 'event_id', 'nfl_id', 'drill_type', 'attempt', 'time', 's', 'a', 'dis'])
df = df.dropna(subset=['nfl_id'])
df['nfl_id'] = df['nfl_id'].astype(int)
df['datetime'] = pd.to_datetime(df['time'])

forty_df = df[df['drill_type'] == 'FORTY_YARD_DASH'].copy()

# Calculate per-attempt metrics
# Peak speed (s), peak acceleration (a), duration
attempt_stats = forty_df.groupby(['draft_year', 'nfl_id', 'attempt']).agg(
    start_time=('datetime', 'min'),
    end_time=('datetime', 'max'),
    max_speed=('s', 'max'),
    max_accel=('a', 'max'),
    total_dist=('dis', 'sum')
).reset_index()

attempt_stats['run_duration'] = (attempt_stats['end_time'] - attempt_stats['start_time']).dt.total_seconds()

# Pivot to compare Attempt 1 vs Attempt 2 for each player
p1 = attempt_stats[attempt_stats['attempt'] == 1].rename(columns={
    'start_time': 'start_1', 'end_time': 'end_1', 'max_speed': 'speed_1', 'max_accel': 'accel_1', 'run_duration': 'dur_1'
})
p2 = attempt_stats[attempt_stats['attempt'] == 2].rename(columns={
    'start_time': 'start_2', 'end_time': 'end_2', 'max_speed': 'speed_2', 'max_accel': 'accel_2', 'run_duration': 'dur_2'
})

paired = pd.merge(p1, p2, on=['draft_year', 'nfl_id'], how='inner')
paired['rest_minutes'] = (paired['start_2'] - paired['end_1']).dt.total_seconds() / 60.0
paired['speed_diff'] = paired['speed_2'] - paired['speed_1']  # positive = faster in attempt 2
paired['dur_diff'] = paired['dur_2'] - paired['dur_1']      # negative = faster in attempt 2

print(f"Total players with both Attempt 1 and Attempt 2 tracked: {len(paired)}")

print("\n--- ATTEMPT 1 vs ATTEMPT 2 IN 40-YARD DASH ---")
print(f"Attempt 1 Max Speed Mean: {paired['speed_1'].mean():.3f} yd/s")
print(f"Attempt 2 Max Speed Mean: {paired['speed_2'].mean():.3f} yd/s")
print(f"Mean Speed Change (Att 2 - Att 1): {paired['speed_diff'].mean():.3f} yd/s")
print(f"Percentage of players FASTER in Attempt 2: {(paired['speed_diff'] > 0).mean()*100:.1f}%")
print(f"Percentage of players SLOWER in Attempt 2: {(paired['speed_diff'] < 0).mean()*100:.1f}%")

print("\n--- REST TIME BETWEEN 40-YARD DASH ATTEMPTS ---")
print(paired['rest_minutes'].describe().round(2))

# Correlation between rest time and performance improvement
valid_rest = paired[(paired['rest_minutes'] > 0) & (paired['rest_minutes'] < 120)]
corr_rest_speed = valid_rest['rest_minutes'].corr(valid_rest['speed_diff'])
print(f"\nCorrelation between rest time between attempts and speed improvement: {corr_rest_speed:.3f}")

# Group by Rest Bracket
valid_rest = valid_rest.copy()
valid_rest['rest_bracket'] = pd.cut(valid_rest['rest_minutes'], bins=[0, 15, 25, 35, 60], labels=['<15 min', '15-25 min', '25-35 min', '>35 min'])
print("\nSpeed improvement by rest bracket:")
print(valid_rest.groupby('rest_bracket')['speed_diff'].agg(['count', 'mean']).round(3))

# Queue position within session
# What position were they in the running order?
p1 = p1.sort_values(by=['draft_year', 'start_1'])
p1['queue_position'] = p1.groupby('draft_year').cumcount() + 1
corr_queue = p1['queue_position'].corr(p1['speed_1'])
print(f"\nCorrelation between queue order in draft class and Attempt 1 speed: {corr_queue:.3f}")
