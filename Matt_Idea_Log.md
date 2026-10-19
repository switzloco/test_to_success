# 🏈 Matt Davis Idea Log: "The Football Brain Depot"

> **Purpose:** A dedicated, unstructured repository for Matt Davis's football theories, player observations, and scouting instincts. These don't need to be formal math equations or statistical hypotheses yet—just football gut checks, film-room questions, and player archetypes we want to test against the 10 Hz sensor tracking data.

---

## 📋 Status & Next Step
- **Current Stage:** Phase 1 (Brainstorming & Unstructured Idea Capture)
- **The Core Assignment Distinction (Stopwatch vs. Telemetry):**
  * **What traditional scouts look at:** Static stopwatch times (e.g., "He ran a 4.52 forty, jumped 36 inches").
  * **What we have:** **10 Hz telemetry (10 sensor pings every second)**. We have their continuous throttle (acceleration), brake profile (deceleration), cornering grip (angular velocity/hip turn), and top-end speed curve.
  * **The Goal:** Show how the *telemetry* predicts who actually wins on Sundays, especially when the stopwatch is misleading.
- **Goal:** Collect Matt's raw thoughts on college careers, competition levels, and big-game performances, then match them to tracking metrics in `combine_tracking.csv` and NFL regular-season games.

---

## 💡 Active Idea Buckets (Matt's Focus Areas)

### 1. The "All-Conference & Competition Level" Anchor
* **Matt's Core Question:** Does a prospect's Combine testing translate differently depending on whether they dominated elite college competition?
* **The Football Logic:**
  * A 4.48 corner who earned 1st-Team All-SEC honors was locking down future NFL 1st-round wideouts every single Saturday.
  * A 4.38 corner from a smaller conference or FCS school may have elite straight-line testing, but rarely faced NFL-caliber route runners, release packages, or physical stem contact.
  * *The Trap:* NFL teams regularly get seduced by workout warriors from small schools and ignore the "dog" from the Big Ten/SEC who tested average in shorts.
* **How We Weave It In (The Combine + Tracking Link):**
  * **The "Pedigree Multiplier":** Does elite Combine movement (e.g., top 10% 3-cone deceleration or 10-yard burst) have a significantly higher conversion rate to NFL success when backed by All-Conference accolades?
  * **The "Under-Tester Steal":** Do All-Conference players with mediocre Combine stopwatch numbers actually display top-tier in-game speed and deceleration once they step onto an NFL field (proving the Combine testing environment was the outlier, not their tape)?

---

### 2. "Big Game Risers" vs. "Workout Warriors" (The Bright Lights Factor)
* **Matt's Core Question:** How do players perform when the pressure is suffocating vs. when running in underwear in a quiet indoor dome?
* **The Football Logic:**
  * Some athletes are "track stars" who excel in sterile, scripted environments (Lucas Oil Stadium with no pads, no crowd, no contact).
  * Other players have a distinct gear shift in rivalry games, conference championships, and CFP bowl games—they find another level of burst, violence, and effort when the stakes spike.
* **How We Weave It In (The Combine + Tracking Link):**
  * **Combine vs. In-Game Speed Ratio:** Compare a player's max speed in the Combine 40-yard dash to their max in-game speed on Sundays. Do "Big Game" college studs have a higher ratio of in-game speed to combine speed (i.e., they play *faster* than they test)?
  * **High-Leverage NFL Tracking:** In NFL regular season games, does their 10 Hz burst stay high on 3rd down, 4th quarter, and in the red zone, while Combine workout warriors see their speed drop off when fatigue and pressure mount?

---

### 3. College Career Arc & Mileage (The 3-Year Starter vs. 1-Year Wonder)
* **Matt's Core Question:** Does a full 3-4 year college career as a productive starter tell us more about movement repeatability than a single season of flash?
* **The Football Logic:**
  * Multi-year starters have hundreds of snaps of calibrated muscle memory against varied schemes and adjustments.
  * 1-year wonders might test through the roof at the Combine after 3 months of hyper-focused private combine training (e.g., EXOS, IMG Academy), masking raw football instincts.
* **How We Weave It In (The Combine + Tracking Link):**
  * Does the mechanical consistency of drill attempts (Attempt 1 vs. Attempt 2 variance in the 3-cone or 40-yard dash) correlate with college starting experience?

---

## 🗣️ Raw Quotes, Player Names & Notes from Matt
*(Use this section to dump quick text messages, player names, or passing thoughts from Matt before categorizing them.)*

* **Player Examples to Test:**
  * *The "Tape Over Testing" Guy:* (e.g., Amon-Ra St. Brown, Cooper Kupp, Puka Nacua) – What did their college accolades say, and why did the Combine miss them?
  * *The "Combine Freak Who Busted" Guy:* (e.g., John Ross, Vernon Gholston, Isaiah Simmons) – Did they have low production/lack of All-Conference consistency?
  * *The "Big Game Dog":* Who are Matt's favorite college playoff / rivalry game dominators whose game translated immediately to the pros?

---

## 🛠️ Data Assets Available to Test Matt's Ideas
1. `data/players.csv`: Contains `college_name`, `college_conference`, draft round, and pick.
2. `data/combine_tracking.csv`: 10 Hz coordinates, speed (`s`), acceleration (`a`), orientation (`o`), and direction (`dir`) across all Combine events.
3. `data/player_career_successes.csv`: NFL games started, offensive/defensive snaps, 1st/2nd-team All-Pro honors, and Pro Bowl selections.
4. `External College Accolades`: We can pull NCAA All-Conference (1st/2nd Team AP/Coaches), College Football Playoff appearances, and top-25 opponent schedules to cross-reference against every rookie class.
