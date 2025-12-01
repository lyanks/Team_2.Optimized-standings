import random


def single_cycle():
    pass


def read_income(path: str) -> dict:
    matches = {}
    with open(path, 'r', encoding='utf-8') as table:
        for line in table:
            w, l = line.split(',')
            winner = w.strip()
            looser = l.strip()
            if looser not in matches:
                matches[looser] = set()
            matches[looser].add(winner)


def ranking_table(losers: dict) -> dict:
    average_point = 1 / len(losers)
    start_leaderboard = {}
    for name in losers:
        start_leaderboard[name] = average_point

    for i in range(100):
        loos_name = losers


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
