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
    average_point = 1/len(losers)
    start_leaderboard = {}
    for name in losers:
            start_leaderboard[name] = average_point


    for i in range(100):
        loos_name = losers