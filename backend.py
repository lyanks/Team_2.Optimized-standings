import random


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

aaa = read_income("test_matches.csv")
a = aaa[0]
aa = aaa[1]

print(ranking_table(a, aa))


def generate_random_table() -> str | None:
    try:
        table_length = int(input())
    except ValueError:
        return 'Invalid input, write a number'
    with open('new_table.csv', 'w', encoding='utf-8') as table:
        table.writelines('winner,looser')
        for _ in range(table_length):
            team1, team2 = get_teams()
            table.writelines(['\n', team1, ',', team2])


def get_teams() -> tuple[str, str]:
    txt = 'Команда '
    letters = list(chr(i) for i in range(ord('A'), ord('Z') + 1))
    t1, t2 = random.sample(letters, 2)
    return txt + t1, txt + t2
