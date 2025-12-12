import argparse
import os
from algorithm import compute_rankings



def validate_file(path: str) -> str:
    """
    Перевіряє, чи правильно введено шлях до файлу.
    Викликається автоматично всередині argparse.
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Файлу '{path}' не існує. Перевірте шлях.")

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"'{path}' не є файлом. Вкажіть коректний файл.")

    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"Файл '{path}' не можна прочитати. Немає дозволу.")

    return path

def read_matches(filepath: str) -> list[tuple[str, str]]:
    """
    Зчитує файл вручну без CSV-модуля.
    Формат кожного рядка: Winner Loser
    """
    matches = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Неправильний формат рядка: '{line}'. ""Очікується: Winner Loser")

            winner, loser = parts
            matches.append((winner, loser))

    return matches


def print_standings(ratings: dict[str, float]):
    """Красивий вивід результатів."""
    sorted_items = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    print("\n=== FINAL TOURNAMENT STANDINGS ===")
    print(f"{'Team':20} | Rating")

    for team, rating in sorted_items:
        print(f"{team:20} | {rating:.4f}")


def main():
    parser = argparse.ArgumentParser(description="Compute optimized tournament standings.")
    parser.add_argument("file", type=str,help="Шлях до файлу з результатами матчів")
    args = parser.parse_args()
    matches = read_matches(args.file)
    ratings = compute_rankings(matches)
    print_standings(ratings)

if __name__ == "__main__":
    main()
import argparse
import os
from algorithm import compute_rankings


def validate_file(path: str) -> str:
    """
    Перевіряє, чи правильно введено шлях до файлу.
    Викликається автоматично всередині argparse.
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Файлу '{path}' не існує. Перевірте шлях.")

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"'{path}' не є файлом. Вкажіть коректний файл.")

    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"Файл '{path}' не можна прочитати. Немає дозволу.")

    return path

def read_matches(filepath: str) -> list[tuple[str, str]]:
    """
    Зчитує файл вручну без CSV-модуля.
    Формат кожного рядка: Winner Loser
    """
    matches = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Неправильний формат рядка: '{line}'. ""Очікується: Winner Loser")

            winner, loser = parts
            matches.append((winner, loser))

    return matches


def print_standings(ratings: dict[str, float]):
    """Красивий вивід результатів."""
    sorted_items = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    print("\n=== FINAL TOURNAMENT STANDINGS ===")
    print(f"{'Team':20} | Rating")

    for team, rating in sorted_items:
        print(f"{team:20} | {rating:.4f}")


def main():
    parser = argparse.ArgumentParser(description="Compute optimized tournament standings.")
    parser.add_argument("file", type=str,help="Шлях до файлу з результатами матчів")
    args = parser.parse_args()
    matches = read_matches(args.file)
    ratings = compute_rankings(matches)
    print_standings(ratings)
if __name__ == "__main__":
    main()
