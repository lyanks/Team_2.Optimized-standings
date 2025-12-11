# **Optimized Tournament Standings**

The goal of this project is to apply graph-based techniques to create a fair and accurate tournament ranking system. Every match is represented as an edge connecting two teams, and each team is represented as a node in the graph. We use a **modified PageRank algorithm** to adjust for opponent strength, so a team's ranking rises more when they defeat a strong team than when they defeat a weak one.

This approach aims to develop a more equitable ranking system and package it in a portable **Docker environment**, making it easy to run on any computer.

---

## Features

- Compute tournament standings based on match results.  
- Adjust team rankings using a PageRank algorithm.  
- Docker setup for easy deployment.  
- Command-line interface (CLI) for interaction.  
- Step-by-step visualization of standings.

---

## How to Run the Program

Prerequisites:
You must have the following software installed on your system:

Python 3 (The project script start.py is written in Python).
Docker Desktop (or Docker Engine) installed and running.
You should also give it access to modify and read your files.


1. Download the `start.py` and `Dockerfile` from this repository.
2. Ensure `start.py` and the `Dockerfile` are in the same local directory.
3. Place your input data file (e.g., input_data.txt) in a seperate folder on your local system.
4. Open a terminal in the directory where `start.py` and `Dockerfile` are.
5. Run the program interactively:
```bash
python3 start.py
```
6. The script will ask you to enter the full path to your input file:
```bash
Введи повний шлях до файлу:
Шлях до файлу: [ENTER THE ABSOLUTE PATH TO YOUR INPUT FILE HERE]
```
7. When completed Docker running, the script will indicate where the results are saved:
```bash
Результати будуть збережені у локальній теці: [PATH_TO_OUTPUT_DIRECTORY]
✅ Завершено. Результати (frames) у теці: [PATH_TO_OUTPUT_DIRECTORY]
```



## Input & Output

**Input:**  

The program expects a CSV file containing match history.
To avoid duplicates or formatting conflicts, each row must follow the format:
```csv
Winner Loser
Teem A Teem B
Teem B Teem C
Teem C Teem A
```

**Output:**  

After completing the PageRank iterations, the algorithm returns a dictionary containing the final team ratings.
This dictionary is sorted in descending order and passed to a visualization function, which generates a clean, readable table and prints it to the console.

User will receive on his local directory photos of progress itteration as well as the final visual respresentation of final team ratings.

---

## Algorithm Overview

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

## Work Distribution 

| Team Member       | Responsibility                                |
|-------------------|-----------------------------------------------|
| Anna Kravchenko   | Docker environment setup + Visualization      |
| Karina Madiar     | CLI                                           |
| Uliana Kryshchyk  | Algorithm implementation + Tests              |
| Yura Melnyk       | Algorithm implementation                      |
| Alina Derevyagina | Visualization and output                      |
