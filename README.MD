# **Optimized Tournament Standings**

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

Prerequisites:
You must have the following software installed on your system:

Python 3 (The project script start.py is written in Python).
Docker Desktop (or Docker Engine) installed and running.
You should also give it access to modify and read your files.


1. Download the `start.py` and  `Dockerfile` from this repository.
2. Ensure 'start.py' and the 'Dockerfile' are in the same local directory.
3. Place your input data file (e.g., input_data.txt) in a seperate folder on your local system.
4. Open a terminal in the directory where 'start.py' and Dockrfile are.
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


---

## Work Distribution 

| Team Member       | Responsibility                                |
|-------------------|-----------------------------------------------|
| Anna Kravchenko   | Docker environment setup + Visualization      |
| Karina Madiar     | CLI                                           |
| Uliana Kryshchyk  | Algorithm implementation + Tests              |
| Yura Melnyk       | Algorithm implementation                      |
| Alina Derevyagina | Visualization and output                      |
