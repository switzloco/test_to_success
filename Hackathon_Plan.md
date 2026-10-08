# NFL Big Data Bowl 2027: Hackathon Project Plan

## Overview
The NFL Big Data Bowl 2027 challenges us to uncover hidden links between how a player moves in a Scouting Combine drill and how they actually perform on the field. Instead of traditional combine testing times, we have high-frequency **10 Hz optical sensor tracking data** (recording speed, acceleration, and orientation 10 times a second) for both Combine drills and actual regular-season NFL games from 2023–2025.

## 🎯 The "Fun Bucket" (Alternative / Bonus Angles)
*   **Combine vs. Madden (The Ultimate Showdown):** Which is a better predictor of on-field NFL success? Actual 10Hz Combine sensor data, or the subjective Madden ratings assigned by EA Sports? 
*   **The "Sandbagger / Track Star" Database:** The Combine is essentially a track meet. Players who ran high school track have a massive mechanical advantage in drills like the 40-yard dash, while pure "football players" might look slow or sandbag the drills because they don't know the starting block techniques. We will build an external database flagging which of our rookies had High School Track experience to see if "Track Guys" overperform at the Combine but underperform on the field compared to their sensor data.

## Hackathon Phases

**Phase 1: Brainstorming & Hypotheses (Weeks 1-2)**
*   **The SMEs:** Leverage our "football guys" (Dad, Brother, Matt) to provide the "eye test" theories. We need to formulate specific hypotheses (e.g., "I don't care about a defensive end's 40-yard dash, I only care how fast he changes direction in the 3-cone.")
*   **The Data Team:** Note these theories and prepare the environment (combining `players.csv`, `combine_tracking.csv`, and `game_tracking.csv`). Build out external datasets (e.g., Madden Ratings, High School Track Database).

**Phase 2: Data Exploration & Prototyping (Weeks 3-5)**
*   Translate theories into queries. If the hypothesis is that "deceleration into breaks" is what makes a great slot receiver, extract deceleration metrics from the Combine positional drills tracking data and correlate it with the `separation_at_pass_forward` metric in the game data.

**Phase 3: Modeling & Narrowing the Scope (Weeks 6-9)**
*   The Kaggle prompt specifically recommends focusing on **one position group or one specific trait**. Pick the strongest correlation found (e.g., O-Line lateral acceleration vs. pass protection pressure allowed) and build out the statistical models to prove it.
*   *Control Variables:* Use our external databases to control for variables like "Did they run track?" to isolate true football speed.

**Phase 4: Write-up & Submission (Weeks 10-12)**
*   Draft the final Kaggle notebook. Requirements are strict: max 2,000 words, fewer than 10 charts/tables, and it must explicitly link Combine sensor data to NFL game performance.
*   Deadline: **January 6, 2027**.

## Combine Test Descriptions (For Reference)
*   **40-Yard Dash (and 10-Yard Split):** The marquee event testing straight-line speed. The 10-yard split is arguably more important for linemen and edge rushers as it measures pure initial burst and explosiveness off the line.
*   **3-Cone Drill (L-Drill):** The ultimate test of agility, change of direction, and body control. Players run around three cones in an L-shape. Famous for evaluating if edge rushers can "bend" around offensive tackles, and if receivers have fluid hips.
*   **20-Yard Short Shuttle (5-10-5):** Measures lateral quickness, start-and-stop ability, and explosion. Essential for linebackers reacting to the run and offensive linemen mirroring pass rushers.
*   **Vertical Jump:** Measures lower-body power and explosiveness vertically from a standstill. Crucial for receivers high-pointing the ball and DBs contesting catches.
*   **Broad Jump:** Tests lower-body explosiveness horizontally. A great indicator of a player's ability to explode out of their stance.
*   **Bench Press (225 lbs):** Tests upper-body strength and endurance. Highly valued for linemen who need to sustain or shed blocks.
*   **Position-Specific Drills:** Tracked specific football movements (e.g., WR route trees, DB backpedals, O-line pass-pro mirrors). Allows analysis of exact deceleration out of cuts or turning speed, rather than just pass/fail eye tests.
