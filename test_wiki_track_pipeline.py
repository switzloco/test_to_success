import pandas as pd
import urllib.request
import urllib.parse
import json
import time
import re

players = pd.read_csv('data/players.csv')
print(f"Loaded {len(players)} players.")

headers = {
    'User-Agent': 'NFLTrackResearch/1.0 (academic research; contact@example.edu)'
}

track_keywords = [
    r'\btrack and field\b', r'\btrack & field\b', r'\btrack team\b',
    r'\b100[- ]meter\b', r'\b100m\b', r'\b200[- ]meter\b', r'\b200m\b',
    r'\b400[- ]meter\b', r'\b400m\b', r'\b4x100\b', r'\b4x200\b',
    r'\bsprinter\b', r'\bsprints\b', r'\bhurdles\b', r'\bhurdler\b',
    r'\bshot put\b', r'\bdiscus\b', r'\blong jump\b', r'\bhigh jump\b',
    r'\btriple jump\b'
]
pattern = re.compile('|'.join(track_keywords), re.IGNORECASE)

def search_wikipedia_track(name, college):
    # Try searching Wikipedia
    search_query = f"{name} {college} football"
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_query)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            results = data.get('query', {}).get('search', [])
            if not results:
                return False, "", "No Wiki Page"
            
            title = results[0]['title']
            
        time.sleep(0.3)
        page_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
        req2 = urllib.request.Request(page_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=5) as resp2:
            page_data = json.loads(resp2.read())
            pages = page_data.get('query', {}).get('pages', {})
            for pid, pinfo in pages.items():
                extract = pinfo.get('extract', '')
                
                # Search specifically in High school / Early life sections if possible, or anywhere
                matches = pattern.findall(extract)
                if matches:
                    # Find snippet around the match
                    first_match = pattern.search(extract)
                    start = max(0, first_match.start() - 60)
                    end = min(len(extract), first_match.end() + 100)
                    snippet = extract[start:end].replace('\n', ' ').strip()
                    unique_matches = list(set([m.lower() for m in matches]))
                    return True, ", ".join(unique_matches), snippet
                else:
                    return False, "", f"Wiki: {title} (no track mentions)"
    except Exception as e:
        return False, "", f"Error: {e}"

results = []
sample_size = 25
print(f"Testing on first {sample_size} players...")

for idx, row in players.head(sample_size).iterrows():
    name = row['display_name']
    college = row['college_name']
    pos = row['nfl_position']
    has_track, events, snippet = search_wikipedia_track(name, college)
    results.append({
        'nfl_id': row['nfl_id'],
        'name': name,
        'pos': pos,
        'college': college,
        'has_track': has_track,
        'events': events,
        'snippet': snippet[:80]
    })
    print(f"[{idx+1}/{sample_size}] {name} ({pos}, {college}): Track={has_track} | {events}")
    time.sleep(0.3)

res_df = pd.DataFrame(results)
print("\n--- RESULTS SUMMARY ---")
print(f"Track Athletes Found: {res_df['has_track'].sum()} / {sample_size} ({res_df['has_track'].mean()*100:.1f}%)")
