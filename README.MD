# **Optimized Tournament Standings(Web App)**

The goal of this project is to create a fair and accurate tournament ranking system using graph theory. Instead of a simple point system, we treat the tournament as a network where every match is an edge connecting two teams.

We utilize a modified PageRank algorithm to calculate "Authority Scores". The core assumption is simple: a win against a strong opponent should be worth more than a win against a weak one.

This project has evolved into a full Interactive Web Application packaged in a portable Docker environment, allowing for dynamic analysis of tournament data.

---

## Features

- Interactive Visualization: A force-directed graph (powered by Plotly) where you can zoom, pan, and hover to see team details.
- Time Travel (Replay Mode): A slider to step through the tournament match-by-match and watch how rankings evolve in real-time. 
- Fair Ranking Algorithm: Implementation of PageRank adapted for sports (Loser pays Winner).
- Zero-Config Deployment: Fully automated setup via Docker and a Python launcher script.

---
## Project Structure

```text
.
├── Dockerfile             # Docker configuration (Streamlit + Python env)
├── start.py               # Launcher script (Builds & Runs Docker)
├── web_app.py             # Main Application Logic (UI + Algorithm)
├── data/                  # Directory for input CSV files
└── requirements.txt       # Python dependencies
```

## How to Run the Program

Prerequisites:
You must have the following software installed on your system:

Python 3 (The project script start.py is written in Python).
Docker Desktop (or Docker Engine) installed and running.
You should also give it access to modify and read your files.


1. Clone this repository or download start.py, Dockerfile, web_app.py, and requirements.txt.
2. Open a terminal in the project directory.
3. Run the launcher.
python3 start.py
4. The script will ask for the path to your CSV file.
Введи повний шлях до CSV файлу:
> /path/to/your/matches.csv
5. Wait for the Docker build to finish. The script will automatically attempt to open the web app in your browser at: http://localhost:8501


## Input & Output

**Input:**  

The application expects a CSV file containing match history. Format: Winner,Loser (headers are optional but recommended).

Example (data/matches.csv):
Winner,Loser
Team A,Team B
Team B,Team C
Team C,Team A
Giant Killer,The Boss
```

**Output:**  

Instead of static files, the application provides an Interactive Dashboard:
Interaction Graph: Visualizes the network of wins/losses. Node size represents the team's strength; color indicates their rank tier.
Live Leaderboard: A sorted table showing "Dominance Points" for each team.
Metrics: Real-time stats on active teams and total matches played.

---

## Algorithm Overview

We adapted the **PageRank algorithm** (originally designed by Google for ranking web pages) to the context of sports tournaments.

1.  **Graph Construction:**
    * **Nodes:** Represent teams.
    * **Edges:** Represent match outcomes.
    * **Direction:** The edge goes from the **Loser** to the **Winner**. This signifies that the Loser "votes" for the Winner's strength.

2.  **Mathematics:**
    The rank of a team $PR(A)$ is calculated iteratively:
    $$PR(A) = \frac{1-d}{N} + d \sum_{v \in M(A)} \frac{PR(v)}{L(v)}$$

    * $d$ is the **damping factor** (set to 0.85), ensuring the algorithm converges.
    * $M(A)$ is the set of teams that lost to Team A.
    * $L(v)$ is the number of losses suffered by team $v$.

3.  **Logic:**
    * If a strong team (with high PR) loses to you, they transfer a significant portion of their rank to you.
    * If a weak team loses to you, your rank increases only slightly.
    * This solves the problem where defeating a champion is valued the same as defeating an outsider in standard league tables.
PageRank Sports Ranking Project: Quick SummaryThis project tackles the flaw in standard sports rankings—where beating the worst team gives the same points as beating the best—by applying the PageRank algorithm to calculate a true "authority" score for each team.
Project Idea: Rating AuthorityThe Graph: We turn the tournament into a graph. Teams are nodes. Edges are directed from Loser → Winner.
The Core: When a team loses, it passes a chunk of its current score (rating) to the team that beat it. Simply put, you earn more points if you beat someone who already has a high rating.

How The Algorithm Works
The ranking score update relies on two key ideas:Opponent Strength: The winner collects a portion of the loser's rating. If you beat a top team (high score), you gain a lot. If you beat a weak team, you gain little.

Exclusivity: The amount transferred is split among all the teams the loser lost to. If a loser only lost to you, you get all their available rating—that was a "costly" loss for them, and a big win for you. If they lose to everyone, their rating is spread thin, and you only get pennies.

The Stabilizer (Dampening)The $d$ factor (our coefficient, usually $0.85$) acts as a system stabilizer. In every round, $15\%$ of the total rating is reset and given back to all teams equally. This guarantees every team has a minimum score and prevents leaders from running away with an unstable, impossibly high rating. The total rating in the system always sums up to 1.

Code SnapshotData Setup (read_matches): Takes a CSV file and builds the graph as a dictionary: {Loser: {List of Winners}}. This structure makes it fast to calculate who pays whom.
The Calculation (ranking_table, calculate_pagerank): We start with equal scores and run an iterative loop. In each step, every team's rating is completely recalculated based on the scores from the previous round.The Finish: The loop runs until the scores barely change anymore. The final, stable scores represent the team's true authoritative ranking.

---
## Tech Stack

* **Language:** Python 3.13
* **Containerization:** Docker
* **Core Libraries:**
    * `numpy` (Vectorized matrix calculations)
    * `matplotlib` (Custom force-directed graph visualization)
---


## Work Distribution 

| Team Member       | Responsibility                                |
|-------------------|-----------------------------------------------|
| Anna Kravchenko   | Docker environment setup + Visualization      |
| Karina Madiar     | CLI                                           |
| Uliana Kryshchyk  | Algorithm implementation + Tests              |
| Yura Melnyk       | Algorithm implementation                      |
| Alina Derevyagina | Visualization and output                      |
