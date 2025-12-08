# Optimized Tournament Standings

The goal of this project is to apply graph-based techniques to create a fair and accurate tournament ranking system. Every match is represented as an edge connecting two teams, and each team is represented as a node in the graph. We use a **modified PageRank algorithm** to adjust for opponent strength, so a team's ranking rises more when they defeat a strong team than when they defeat a weak one.

This approach aims to develop a more equitable ranking system and package it in a portable **Docker environment**, making it easy to run on any computer.

---

## Features

- Compute tournament standings based on match results.  
- Adjust team rankings using a PageRank algorithm.  
- Docker setup for easy deployment.  
- Command-line interface (CLI) for interaction.  
- Optional visualization of standings.

---

## How to Run the Program


1. Download the `start.py` from this repository.  
2. Open a terminal in the project directory.
3. Run the program interactively:
```bash
python start.py
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

---

## Algorithm Overview


---

## Work Distribution 

| Team Member       | Responsibility                   |
|-------------------|----------------------------------|
| Anna Kravchenko   | Docker environment setup         |
| Karina Madiar     | CLI + Tests                      |
| Uliana Kryshchyk  | Algorithm implementation + Tests |
| Yura Melnyk       | Algorithm implementation         |
| Alina Derevyagina | Visualization and output         |
