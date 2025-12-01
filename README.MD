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
```bash
docker build -t optimized_standings .
```
4. Run the program interactively:
```bash
docker run -it optimized_standings
```



## Input & Output

**Input:**  

Програма отримує на вхід CSV-файл з історією матчів. 
Щоб уникнути дублів та помилок через різний стиль запису, алгоритм зчитує рядки у форматі Winner, Loser.

**Output:**  

Після завершення всіх ітерацій алгоритм повертає словник (dictionary) 
із фінальними рейтингами команд. Цей словник сортується за спаданням 
значень і передається в окрему функцію візуалізації, яка формує красиву таблицю і виводить її результат у консоль

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
