# Оптимiзована турнiрна таблиця. Optimized standings.


The goal of this project is to apply graph-based techniques to create a perfect tournament ranking system. Every match is an edge connecting two teams, and each team is represented as a node in the graph. We use a modified PageRank algorithm to adjust for opponent strength rather than giving wins and losses a set score. Therefore, a team's ranking rises more when they defeat a strong team than when they defeat a weak one.

The goal of this project is to develop a more equitable ranking algorithm and package the answer in a portable Docker environment that is simple to run on any computer.


## How to start our program
Save the Dockerfile file on your computer
Open terminal
Run this command to create an image:
```bash
docker build -t optimized_standings .
```
To run our code input this into cmd:
```bash
docker run -it optimized_standings
```







# quick overview of realisation
input:
output:



----------------------------------
Work distribution:

Anna Kravchenko - docker
Karina Madiar - CLI
Ulyana Krushchyk - algorithm
Yura Melnyk - algorithm
Alina Derevyagina - visual part
