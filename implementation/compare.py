import time
from backend import *

def ranking_table_while(matches: dict, all_teams: set, coef = 0.85, epsilon = 1e-8) -> dict:
    num_of_command = len(all_teams)
    base_bonus = (1 - coef)/num_of_command

    start_leaderboard = {name: 1/num_of_command for name in all_teams}
    iterations = 0

    while True:
        new_leaderboard = {name: base_bonus for name in all_teams}
        for name, winners in matches.items():
            loser_points = start_leaderboard[name]
            loser_loos = len(winners)
            share = (loser_points / loser_loos) * coef 
            for w_nam in winners:
                new_leaderboard[w_nam] += share
        delta = sum(abs(new_leaderboard[n] - start_leaderboard[n]) for n in all_teams)
        start_leaderboard = new_leaderboard
        iterations += 1 

        if delta < epsilon:
            break
        
    return start_leaderboard, iterations


if __name__ == "__main__":
    generate_random_table()
    matches_data, teams_data = read_matches("new_table.csv")
    if matches_data:
        print(f"\nЗавантажено команд: {len(teams_data)}")
        print("-" * 30)

        start_time = time.time()
        res_for = ranking_table(matches_data, teams_data)
        time_for = time.time() - start_time
        print(f"FOR (100 ітерацій): {time_for:.5f} сек")
        print(f"Кількість ітерацій FOR: 100") 

        start_time = time.time()
        res_while, iterations_while = ranking_table_while(matches_data, teams_data)
        time_while = time.time() - start_time
        print(f"WHILE (авто-стоп):  {time_while:.5f} сек")
        print(f"Кількість ітерацій WHILE: {iterations_while}")

        print("-" * 30)

