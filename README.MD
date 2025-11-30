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

1. Download the `Dockerfile` for this repository.  
2. Open a terminal in the project directory.  
3. Build the Docker image:

'''bash
docker build -t optimized_standings .
'''

## Input & Output

**Input:**  


**Output:**  


---

## Algorithm Overview


---

## Work Distribution 
(For now)

| Team Member         | Responsibility                 |
|---------------------|--------------------------------|
| Anna Kravchenko     | Docker environment setup       |
| Karina Madiar       | CLI + Tests                    |
| Ulyana Krushchyk    | Algorithm implementation       |
| Yura Melnyk         | Algorithm implementation       |
| Alina Derevyagina   | Visualization and output       |
