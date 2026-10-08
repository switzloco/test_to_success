import pandas as pd
import numpy as np
import math

# Lucas Oil Stadium coordinates (Indianapolis, IN) - Eastern Time
INDY_LAT = 39.7601
INDY_LON = -86.1639

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Comprehensive College Geocoding & Timezone dictionary (112 colleges)
# (lat, lon, timezone_diff_from_ET: 0 for ET, 1 for CT, 2 for MT, 3 for PT)
COLLEGE_LOCS = {
    'Alabama': (33.2098, -87.5692, 1),
    'Alabama A&M': (34.7842, -86.5724, 1),
    'Appalachian State': (36.2142, -81.6817, 0),
    'Arizona': (32.2319, -110.9501, 2),  # Mountain (MST)
    'Arizona State': (33.4242, -111.9281, 2),
    'Arkansas': (36.0687, -94.1748, 1),
    'Arkansas-Pine Bluff': (34.2483, -92.0199, 1),
    'Auburn': (32.5934, -85.4952, 1),
    'Baylor': (31.5493, -97.1143, 1),
    'Boise State': (43.6027, -116.1999, 2),
    'Boston College': (42.3355, -71.1685, 0),
    'Bowling Green': (41.3781, -83.6366, 0),
    'Brigham Young': (40.2518, -111.6493, 2),
    'California': (37.8719, -122.2585, 3),  # Pacific (PT)
    'Central Arkansas': (35.0782, -92.4593, 1),
    'Central Florida': (28.6024, -81.2001, 0),
    'Central Michigan': (43.5898, -84.7770, 0),
    'Chattanooga': (35.0456, -85.3097, 0),
    'Cincinnati': (39.1329, -84.5150, 0),
    'Clemson': (34.6784, -82.8374, 0),
    'Coastal Carolina': (33.7944, -79.0141, 0),
    'Colorado': (40.0076, -105.2659, 2),
    'Colorado State': (40.5734, -105.0865, 2),
    'Connecticut': (41.8077, -72.2540, 0),
    'Duke': (36.0014, -78.9382, 0),
    'Eastern Michigan': (42.2505, -83.6241, 0),
    'Ferris State': (43.6845, -85.4842, 0),
    'Florida': (29.6436, -82.3549, 0),
    'Florida A&M': (30.4284, -84.2882, 0),
    'Florida State': (30.4419, -84.2985, 0),
    'Georgia': (33.9480, -83.3773, 0),
    'Georgia Tech': (33.7756, -84.3963, 0),
    'Holy Cross': (42.2389, -71.8080, 0),
    'Houston': (29.7199, -95.3422, 1),
    'Houston Christian': (29.6946, -95.5152, 1),
    'Howard': (38.9227, -77.0194, 0),
    'Illinois': (40.1020, -88.2272, 1),
    'Indiana': (39.1653, -86.5264, 0),
    'Iowa': (41.6627, -91.5549, 1),
    'Iowa State': (42.0267, -93.6465, 1),
    'Jacksonville State': (33.8234, -85.7663, 1),
    'Kansas': (38.9543, -95.2558, 1),
    'Kansas State': (39.1974, -96.5847, 1),
    'Kentucky': (38.0307, -84.5040, 0),
    'Liberty': (37.3524, -79.1802, 0),
    'Louisiana State': (30.4133, -91.1800, 1),
    'Louisiana-Lafayette': (30.2144, -92.0198, 1),
    'Louisville': (38.2123, -85.7585, 0),
    'Maryland': (38.9869, -76.9426, 0),
    'Memphis': (35.1187, -89.9372, 1),
    'Miami': (25.7174, -80.2781, 0),
    'Michigan': (42.2780, -83.7382, 0),
    'Michigan State': (42.7018, -84.4822, 0),
    'Minnesota': (44.9740, -93.2277, 1),
    'Mississippi': (34.3647, -89.5384, 1),
    'Mississippi State': (33.4549, -88.7895, 1),
    'Missouri': (38.9404, -92.3277, 1),
    'Navy': (38.9822, -76.4839, 0),
    'Nebraska': (40.8202, -96.7005, 1),
    'Nevada': (39.5440, -119.8164, 3),
    'Nevada-Las Vegas': (36.1070, -115.1444, 3),
    'North Carolina': (35.9049, -79.0469, 0),
    'North Carolina State': (35.7847, -78.6821, 0),
    'North Carolina-Charlotte': (35.3071, -80.7352, 0),
    'North Dakota State': (46.8972, -96.8024, 1),
    'Northwestern': (42.0565, -87.6753, 1),
    'Notre Dame': (41.7056, -86.2353, 0),
    'Ohio State': (40.0067, -83.0305, 0),
    'Oklahoma': (35.2059, -97.4457, 1),
    'Oklahoma State': (36.1257, -97.0699, 1),
    'Old Dominion': (36.8853, -76.3059, 0),
    'Oregon': (44.0448, -123.0726, 3),
    'Oregon State': (44.5638, -123.2834, 3),
    'Penn State': (40.7982, -77.8599, 0),
    'Pittsburgh': (40.4444, -79.9608, 0),
    'Princeton': (40.3440, -74.6514, 0),
    'Purdue': (40.4237, -86.9212, 0),
    'Rice': (29.7174, -95.4018, 1),
    'Rutgers': (40.5008, -74.4474, 0),
    'San Jose State': (37.3352, -121.8811, 3),
    'South Alabama': (30.6954, -88.1788, 1),
    'South Carolina': (33.9972, -81.0274, 0),
    'South Dakota': (42.7877, -96.9253, 1),
    'South Dakota State': (44.3188, -96.7836, 1),
    'Southeast Missouri': (37.3153, -89.5312, 1),
    'Southern California': (34.0224, -118.2851, 3),
    'Southern Methodist': (32.8412, -96.7845, 1),
    'Southern Mississippi': (31.3297, -89.3332, 1),
    'Stanford': (37.4275, -122.1697, 3),
    'Syracuse': (43.0392, -76.1351, 0),
    'Tennessee': (35.9544, -83.9295, 0),
    'Texas': (30.2849, -97.7341, 1),
    'Texas A&M': (30.6187, -96.3365, 1),
    'Texas Christian': (32.7096, -97.3628, 1),
    'Texas Tech': (33.5843, -101.8783, 1),
    'Texas-San Antonio': (29.5838, -98.6199, 1),
    'Toledo': (41.6578, -83.6137, 0),
    'Troy': (31.7994, -85.9568, 1),
    'Tulane': (29.9407, -90.1203, 1),
    'UCLA': (34.0689, -118.4452, 3),
    'Utah': (40.7649, -111.8421, 2),
    'Utah State': (41.7452, -111.8097, 2),
    'Virginia': (38.0336, -78.5080, 0),
    'Virginia Tech': (37.2284, -80.4234, 0),
    'Wake Forest': (36.1353, -80.2790, 0),
    'Washington': (47.6553, -122.3035, 3),
    'Washington State': (46.7325, -117.1643, 3),
    'West Virginia': (39.6358, -79.9559, 0),
    'Western Kentucky': (36.9857, -86.4557, 1),
    'Western Michigan': (42.2828, -85.6133, 0),
    'Wisconsin': (43.0766, -89.4125, 1),
    'Wyoming': (41.3145, -105.5811, 2)
}

# Load players and combine results
players = pd.read_csv('data/players.csv')
combine = pd.read_csv('data/combine_results.csv')
track = pd.read_csv('data/player_track_backgrounds.csv')

df = pd.merge(players, combine, on=['nfl_id', 'draft_year'], how='left')
df = pd.merge(df, track[['nfl_id', 'has_track_background']], on='nfl_id', how='left')

# Calculate travel features
travel_data = []
for idx, row in df.iterrows():
    c = row['college_name']
    if c in COLLEGE_LOCS:
        lat, lon, tz = COLLEGE_LOCS[c]
        dist = haversine(lat, lon, INDY_LAT, INDY_LON)
    else:
        dist = np.nan
        tz = np.nan
    travel_data.append({'distance_to_indy': dist, 'timezones_crossed': tz})

travel_df = pd.DataFrame(travel_data)
df = pd.concat([df, travel_df], axis=1)

print(f"Total prospects analyzed: {len(df)}")
print("\n--- DISTRIBUTION BY TIME ZONES CROSSED TO INDY ---")
print(df['timezones_crossed'].value_counts().sort_index())

# Group comparisons: Local / Eastern (0 TZ) vs Central (1 TZ) vs Mountain (2 TZ) vs Pacific (3 TZ)
print("\n--- COMBINE METRICS BY TIME ZONES CROSSED ---")
agg_dict = {
    'display_name': 'count',
    'distance_to_indy': 'mean',
    'vertical': 'mean',
    'broad_jump': 'mean',
    'ten_yd_split': 'mean',
    'forty': 'mean',
    'combine_weight': 'mean'
}
summary = df.groupby('timezones_crossed').agg(agg_dict).rename(columns={'display_name': 'n_players'})
print(summary.round(3))

# Skill Positions specifically (controlling for weight difference)
skill_positions = ['WR', 'CB', 'SS', 'FS', 'RB']
skills = df[df['nfl_position'].isin(skill_positions)].copy()

print("\n--- SKILL POSITIONS ONLY (WR, DB, RB) BY TIME ZONE ---")
skill_summary = skills.groupby('timezones_crossed').agg(agg_dict).rename(columns={'display_name': 'n_players'})
print(skill_summary.round(3))

# Compare Big Ten (Local/Midwest) vs Pac-12 (Cross-Country/3 TZ)
b10 = df[df['college_conference'] == 'Big Ten Conference']
p12 = df[df['college_conference'] == 'Pacific Twelve Conference']

print("\n--- BIG TEN (LOCAL) vs PAC-12 (3 TIME ZONES) ---")
print(f"Big Ten: N={len(b10)}, Avg Dist={b10['distance_to_indy'].mean():.1f} mi, Vert={b10['vertical'].mean():.2f} in, 10-Yd Split={b10['ten_yd_split'].mean():.3f}s, 40={b10['forty'].mean():.3f}s, Wt={b10['combine_weight'].mean():.1f} lbs")
print(f"Pac-12:  N={len(p12)}, Avg Dist={p12['distance_to_indy'].mean():.1f} mi, Vert={p12['vertical'].mean():.2f} in, 10-Yd Split={p12['ten_yd_split'].mean():.3f}s, 40={p12['forty'].mean():.3f}s, Wt={p12['combine_weight'].mean():.1f} lbs")

# Regression Analysis: Testing the Travel Tax controlling for Weight
from scipy import stats

valid_vert = skills.dropna(subset=['vertical', 'combine_weight', 'timezones_crossed', 'distance_to_indy'])
slope_tz, intercept_tz, r_value_tz, p_value_tz, std_err_tz = stats.linregress(valid_vert['timezones_crossed'], valid_vert['vertical'])
print(f"\nLinear Regression: Vertical Jump vs Timezones Crossed (Skill Positions):")
print(f"  Slope (effect per TZ crossed): {slope_tz:.3f} inches | p-value: {p_value_tz:.4f} | R: {r_value_tz:.3f}")

valid_split = skills.dropna(subset=['ten_yd_split', 'combine_weight', 'timezones_crossed', 'distance_to_indy'])
slope_sp, intercept_sp, r_value_sp, p_value_sp, std_err_sp = stats.linregress(valid_split['timezones_crossed'], valid_split['ten_yd_split'])
print(f"\nLinear Regression: 10-Yard Split vs Timezones Crossed (Skill Positions):")
print(f"  Slope (effect per TZ crossed): {slope_sp:.4f}s | p-value: {p_value_sp:.4f} | R: {r_value_sp:.3f}")

# Save the enriched dataset
df.to_csv('data/players_with_travel.csv', index=False)
print("\nSaved enriched dataset to data/players_with_travel.csv")
