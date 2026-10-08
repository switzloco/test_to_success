import pandas as pd
import urllib.request
import urllib.parse
import json
import time
import re
import os
import sys

# Ensure stdout flushes immediately
sys.stdout.reconfigure(line_buffering=True)

players = pd.read_csv('data/players.csv')
output_file = 'data/player_track_backgrounds.csv'

print(f"Starting Track Background extraction for {len(players)} players...")

headers = {
    'User-Agent': 'NFLTrackResearchBot/1.0 (academic research; contact@example.edu)'
}

track_patterns = [
    r'\btrack and field\b', r'\btrack & field\b', r'\btrack team\b',
    r'\b100[- ]meter\b', r'\b100m\b', r'\b200[- ]meter\b', r'\b200m\b',
    r'\b400[- ]meter\b', r'\b400m\b', r'\b4x100\b', r'\b4x200\b', r'\b4x400\b',
    r'\bsprinter\b', r'\bsprints\b', r'\bhurdles\b', r'\bhurdler\b',
    r'\bshot put\b', r'\bdiscus\b', r'\blong jump\b', r'\bhigh jump\b',
    r'\btriple jump\b'
]
regex = re.compile('|'.join(track_patterns), re.IGNORECASE)

# Load existing progress if available
if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file)
    processed_ids = set(existing_df['nfl_id'])
    results = existing_df.to_dict('records')
    print(f"Resuming from {len(processed_ids)} already processed players.")
else:
    processed_ids = set()
    results = []

def lookup_track(name, college):
    query = f"{name} {college} football"
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
    req = urllib.request.Request(search_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('query', {}).get('search', [])
            if not hits:
                return False, "", "", "No wiki page found"
            
            # Select top hit
            title = hits[0]['title']
            
        time.sleep(0.2)
        page_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
        req2 = urllib.request.Request(page_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=8) as resp2:
            page_data = json.loads(resp2.read().decode('utf-8'))
            pages = page_data.get('query', {}).get('pages', {})
            for pid, pinfo in pages.items():
                extract = pinfo.get('extract', '')
                
                # Search for track keywords
                matches = regex.findall(extract)
                if matches:
                    first_match = regex.search(extract)
                    start = max(0, first_match.start() - 60)
                    end = min(len(extract), first_match.end() + 100)
                    snippet = extract[start:end].replace('\n', ' ').strip()
                    unique_matches = list(set([m.lower() for m in matches]))
                    return True, ", ".join(unique_matches), snippet, title
                else:
                    return False, "", "", title
    except Exception as e:
        return False, "", f"Error: {e}", ""

count = len(results)
total = len(players)

for idx, row in players.iterrows():
    nfl_id = row['nfl_id']
    if nfl_id in processed_ids:
        continue
        
    name = row['display_name']
    college = row['college_name']
    pos = row['nfl_position']
    year = row['draft_year']
    
    has_track, keywords, snippet, wiki_title = lookup_track(name, college)
    
    record = {
        'nfl_id': nfl_id,
        'display_name': name,
        'draft_year': year,
        'nfl_position': pos,
        'college_name': college,
        'has_track_background': has_track,
        'track_keywords': keywords,
        'track_evidence_snippet': snippet,
        'wiki_page_title': wiki_title
    }
    results.append(record)
    processed_ids.add(nfl_id)
    count += 1
    
    track_status = "TRACK" if has_track else "No"
    print(f"[{count}/{total}] {name} ({pos}, {college}): {track_status} {f'({keywords})' if has_track else ''}")
    
    # Save checkpoint every 25 players
    if count % 25 == 0 or count == total:
        pd.DataFrame(results).to_csv(output_file, index=False)
        print(f"--> Saved checkpoint ({count}/{total}) to {output_file}")
        
    time.sleep(0.3)

final_df = pd.DataFrame(results)
final_df.to_csv(output_file, index=False)
print("\nExtraction complete!")
print(f"Total track athletes identified: {final_df['has_track_background'].sum()} / {len(final_df)} ({final_df['has_track_background'].mean()*100:.1f}%)")
