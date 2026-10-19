# 🏆 Case Study: A Recent Grand Prize Winner
### *"Uncovering Missed Tackle Opportunities"*
**Authors:** Matthew Chang, Katherine Dai, Daniel Jiang, and Harvey Cheng  
**Competition:** NFL Big Data Bowl 2024 (Metric Track Winner — Presented live at the NFL Combine)  
**Direct Kaggle Link:** [kaggle.com/code/matthewchang/uncovering-missed-tackle-opportunities](https://www.kaggle.com/code/matthewchang/uncovering-missed-tackle-opportunities)

---

## 🎯 Why This Notebook Won Grand Prize
This project is another masterclass in **"fixing a broken football statistic."** The authors realized that standard NFL box scores and broadcast stats for tackling are completely backwards, and they used 10 Hz player-tracking data to create a metric that NFL defensive coordinators now study.

---

## 📖 The 4 Sections of the Notebook

### 1. The Football Problem (Introduction)
* **The Scout's Dilemma:** In traditional box scores, "Missed Tackles" are totally misleading.
  * **The "Hero Miss":** A linebacker sprints 40 yards sideline-to-sideline, makes an acrobatic dive, and barely grazes the running back's shoelace. The box score punishes him with a "Missed Tackle," even though it was an unbelievable effort just to get there.
  * **The "Passive Bystander":** A cornerback takes a lazy pursuit angle, breaks down 5 yards away, hesitates, and lets the receiver sprint right past him without making contact. The box score says: **0 Missed Tackles** (because he never touched him!).
* **The Question:** Can we separate defenders who actually blow easy tackles from defenders who only miss because they are constantly putting themselves in difficult, high-effort situations?

---

### 2. The 10 Hz Tracking Metric (Expected Tackle Probability — $xTackle$)
At every single 100ms frame (10 times a second), their model looked at the physical physics between the ball-carrier and the defender:
* **Distance to runner**
* **Closing speed (relative velocity)**
* **Pursuit angle (are hips squared up or running parallel?)**
* **Blocker interference (is an offensive lineman in between them?)**

From this, they calculated **Expected Tackle Probability ($xTackle$)** in real time:
* At frame 10: Defender is 10 yards away $\rightarrow xTackle = 15\%$
* At frame 18: Defender closes within 2 yards with squared shoulders $\rightarrow xTackle = 82\%$
* At frame 22: Ball-carrier makes a cut, defender whiffs $\rightarrow xTackle = 0\%$

**The Big Finding (MTO):**  
They officially defined a **"Missed Tackle Opportunity (MTO)"**: Any play where a defender reached **$\ge 75\%$ tackle probability for at least 0.5 seconds**, but failed to bring the ball-carrier down.

---

### 3. The Visualizations (The "Aha!" Charts)

#### Chart 1: The Live Probability Meter Over the Player's Head
An animated play diagram where each defender had a live circle changing color from blue (low probability) to green to bright red (high probability). You could watch the red circle pop up over a defender's head right before he got juked.

#### Chart 2: The "Tackling Reality" Quadrant Plot
They plotted every NFL linebacker and safety on a 2x2 scatter plot:
* **X-Axis:** Tackle Opportunities Generated per Game (Range, Hustle, Motor)
* **Y-Axis:** Tackle Conversion Rate (% of high-probability opportunities finished)

```
                              HIGH CONVERSION RATE (%)
                                         |
            "The Conservative Finishers" |       "The Elite Erasers"
            (Low range / slow trigger,   |   (Insane range, creates tons of
             but rarely misses when in   |    chances, finishes at 90%+)
             easy position)              |   [Ex: Fred Warner, Roquan Smith]
            -----------------------------+-----------------------------
            "The Invisible Bystanders"   |       "The High-Motor Gamblers"
            (Low range, low hustle,      |   (Flies around the field, creates
             never gets close enough to  |    huge play volume, but over-pursues
             even register a miss)       |    or whiffs on open-field jukes)
                                         |
                               LOW CONVERSION RATE (%)
```

---

### 4. The Actionable Coaching / GM Takeaway
* **Don't Cut the "Gambler":** Players who lead the league in raw box-score missed tackles are often your best athletes—they generate 12 tackle opportunities a game and finish 10 of them. A lazy player might generate 2 opportunities and finish 2.
* **Tackling Technique vs. Range:** If a linebacker is in the bottom-right quadrant ("High-Motor Gambler"), coaches don't need to bench him—they just need to teach him to sink his hips and break down rather than lunging.

---

## 💡 How Matt Can Connect This to Combine & College
This tackling model directly mirrors the questions Matt is asking about **Big Game performers and Combine testing**:

1. **The Combine Link (The Short Shuttle & Broad Jump):**
   * Does a linebacker's lateral agility in the 20-yard shuttle predict his **Tackle Opportunity Generation** (his sideline-to-sideline range)?
   * Or does the short shuttle only test change of direction in underwear, while true closing burst requires the instincts you see on college tape?
2. **The College "Big Game" Dog:**
   * In college big games (against Georgia, Ohio State, Alabama), which linebackers maintained elite conversion rates when facing future NFL speed?
   * If a linebacker dominated All-Conference play, his tackling conversion rate on Sundays is often resilient, even if his 40-yard dash at the Combine was average.
