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