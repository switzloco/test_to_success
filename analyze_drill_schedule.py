import pandas as pd
import numpy as np

# Load tracking data
print("Loading combine tracking data...")
df = pd.read_csv('data/combine_tracking.csv', usecols=['draft_year', 'event_id', 'nfl_id', 'drill_type', 'drill_name', 'attempt', 'time'])
df = df.dropna(subset=['nfl_id'])
df['nfl_id'] = df['nfl_id'].astype(int)
df['datetime'] = pd.to_datetime(df['time'])

# Load players and combine results
players = pd.read_csv('data/players.csv')
combine_res = pd.read_csv('data/combine_results.csv')

# Each drill attempt start and end time
attempts = df.groupby(['draft_year', 'nfl_id', 'drill_type', 'drill_name', 'attempt']).agg(
    start_time=('datetime', 'min'),
    end_time=('datetime', 'max'),
    duration_sec=('datetime', lambda x: (x.max() - x.min()).total_seconds())
).reset_index()

attempts = attempts.sort_values(by=['nfl_id', 'start_time'])
attempts = pd.merge(attempts, players[['nfl_id', 'display_name', 'nfl_position', 'draft_year']], on=['nfl_id', 'draft_year'], how='left')

print(f"\nTotal players with optical tracking: {attempts['nfl_id'].nunique()}")
print(f"Total drill attempts tracked: {len(attempts)}")

# Show drill sequences for 3 different position groups
print("\n--- SAMPLE DRILL SCHEDULE FOR INDIVIDUAL PLAYERS ---")
for pos in ['WR', 'CB', 'T', 'DE']:
    sample_p = attempts[attempts['nfl_position'] == pos]['nfl_id'].unique()
    if len(sample_p) > 0:
        pid = sample_p[0]
        p_attempts = attempts[attempts['nfl_id'] == pid]
        p_name = p_attempts['display_name'].iloc[0]
        print(f"\n{p_name} ({pos}, Draft Year: {p_attempts['draft_year'].iloc[0]}):")
        for idx, r in p_attempts.iterrows():
            print(f"  {r['start_time'].strftime('%Y-%m-%d %H:%M:%S')} | {r['drill_type']} - {r['drill_name']} (Attempt {r['attempt']}, dur: {r['duration_sec']:.1f}s)")

# Analyze drill order patterns across all players
# What drill comes first, second, third, etc. for each player?
attempts['drill_order'] = attempts.groupby('nfl_id').cumcount() + 1

print("\n--- WHAT DRILL TYPES APPEAR FIRST FOR PLAYERS? ---")
first_drills = attempts[attempts['drill_order'] == 1]['drill_type'].value_counts()
print(first_drills)

print("\n--- WHAT DRILL TYPES APPEAR LAST FOR PLAYERS? ---")
last_attempt_idx = attempts.groupby('nfl_id')['drill_order'].transform('max')
last_drills = attempts[attempts['drill_order'] == last_attempt_idx]['drill_type'].value_counts()
print(last_drills)

# Timing across the day: when do drills start?
attempts['hour'] = attempts['start_time'].dt.hour
print("\n--- DISTRIBUTION OF DRILL START TIMES (HOUR OF DAY, UTC / LOCAL) ---")
print(attempts['hour'].value_counts().sort_index())

# Rest intervals between drills
attempts['prev_end_time'] = attempts.groupby('nfl_id')['end_time'].shift(1)
attempts['rest_minutes'] = (attempts['start_time'] - attempts['prev_end_time']).dt.total_seconds() / 60.0

print("\n--- REST TIME BETWEEN DRILLS (MINUTES) ---")
rest_valid = attempts['rest_minutes'].dropna()
rest_within_day = rest_valid[(rest_valid > 0) & (rest_valid < 300)]
print(rest_within_day.describe())

# Save structured schedule summary
attempts.to_csv('data/player_drill_schedules.csv', index=False)
print("\nSaved player drill schedules to data/player_drill_schedules.csv")
