import numpy as np


def read_matches(path: str) -> dict:
    matches = {}
    all_teams = set()
    with open(path, 'r', encoding='utf-8') as table:
        table.readline()
        for line in table:
            w, l = line.split(',')
            winner = w.strip()
            loser = l.strip()
            all_teams.add(winner)
            all_teams.add(loser)

            if loser not in matches:
                matches[loser] = set()
            matches[loser].add(winner)
    return matches, all_teams

def calculate_pagerank(matches_dict, teams, damping=0.85, epsilon=1e-8):
    """
    Розраховує PageRank для команд на основі перемог.
    matches_dict: {loser: {winners who beat them}}
    """
    n = len(teams)
    if n == 0:
        return {}

    teams_list = list(teams)
    team_idx = {t: i for i, t in enumerate(teams_list)}

    scores = np.ones(n) / n

    out_degree = {t: 0 for t in teams}

    for loser, winners in matches_dict.items():
        out_degree[loser] = len(winners)

    while True:
        new_scores = np.ones(n) * (1 - damping) / n

        for loser, winners in matches_dict.items():
            if out_degree[loser] > 0:
                loser_idx = team_idx[loser]
                contribution = damping * scores[loser_idx] / out_degree[loser]

                for winner in winners:
                    winner_idx = team_idx[winner]
                    new_scores[winner_idx] += contribution

        dangling_sum = 0
        for t in teams:
            if t not in matches_dict or len(matches_dict.get(t, set())) == 0:
                dangling_sum += scores[team_idx[t]]

        new_scores += damping * dangling_sum / n

        delta = np.sum(np.abs(new_scores - scores))
        scores = new_scores

        if delta < epsilon:
            break

    scores = scores / scores.sum()

    return {teams_list[i]: scores[i] for i in range(n)}

def ranking_table(matches: dict, all_teams: set, coef = 0.85) -> dict:

    num_of_command = len(all_teams)
    base_bonus = (1 - coef)/num_of_command

    start_leaderboard = {name: 1/num_of_command for name in all_teams}

    for _ in range(100):
        new_leaderboard = {name: base_bonus for name in all_teams}
        for name, winners in matches.items():
            loser_points = start_leaderboard[name]
            loser_loos = len(winners)
            share = (loser_points / loser_loos) * coef
            for w_nam in winners:
                new_leaderboard[w_nam] += share
        start_leaderboard = new_leaderboard
    return start_leaderboard

aaa = read_matches("/Users/yurleomel/Documents/ProgrammingUCU/discra_lab2/Team_2.Optimized-standings/app/data/test_matches.csv")
a = aaa[0]
aa = aaa[1]


print(calculate_pagerank(a, aa))
print(ranking_table(a, aa))
