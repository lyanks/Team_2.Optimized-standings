def single_cycle():
    pass


def read_income(path: str) -> dict:
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


def ranking_table(matches: dict, all_teams: set) -> dict:
    COEF = 0.85
    num_of_command = len(all_teams)
    average_point = 1/num_of_command
    base_bonus = (1 - COEF)/num_of_command
    start_leaderboard = {}

    for name in all_teams:
        start_leaderboard[name] = average_point


    for i in range(100):
        new_leaderboard = {name: base_bonus for name in all_teams}
        for name, winners in matches.items():
            loser_points = start_leaderboard[name]
            loser_loos = len(winners)
            for w_nam in winners:
                new_leaderboard[w_nam] += COEF * (loser_points/loser_loos)
        start_leaderboard = new_leaderboard
    return start_leaderboard

aaa = read_income("table_1.csv")
a = aaa[0]
aa = aaa[1]

print(ranking_table(a, aa))
