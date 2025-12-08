import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np
import math
import random
import os
import csv
import sys # ДОДАНО: Для зчитування аргументів командного рядка

# Спроба імпорту вашої функції розрахунку
# Переконайтеся, що файли compare.py та backend.py доступні
try:
    from compare import ranking_table_while
except ImportError:
    # Заглушка, якщо файлів немає поруч
    def ranking_table_while(matches, teams):
        return {t: 1.0/len(teams) for t in teams}, 1

# ==========================================
# 1. НАЛАШТУВАННЯ СТИЛУ
# ==========================================
STYLE = {
    "bg": "#f9f9f9",
    "cmap": "viridis",
    "arrow_color_current": "#e74c3c", # Червоний для останнього матчу
    "arrow_color_history": "#7f8c8d", # Сірий для історії
    "text_color": "white",
    "outline_color": "#2c3e50",
    "font_size": 11,
    "shadow_alpha": 0.25,
    "team_colors": {
        "green_unique": "#138D75",     # 1. Смарагдовий (ТІЛЬКИ #1)
        "green_secondary": "#2ecc71",  # 2. Яскраво-зелений (Високий рейтинг)
        "orange": "#e67e22",           # 3. Помаранчевий (Середній)
        "violet": "#8e44ad",           # 4. Фіолетовий (Низький)
    },
}

BASE_POSITIONS = {}

# ==========================================
# 2. ФІЗИКА
# ==========================================

def get_base_positions(teams, radius=50, seed=42):
    """Визначає початкові позиції команд по спіралі."""
    global BASE_POSITIONS
    if BASE_POSITIONS and set(BASE_POSITIONS.keys()) >= set(teams):
        return

    random.seed(seed)
    phi = math.pi * (3 - math.sqrt(5))

    current_teams = list(teams)
    for i, t in enumerate(current_teams):
        if t not in BASE_POSITIONS:
            angle = i * phi
            r = radius * (0.6 + 0.6 * (i / (len(current_teams) + 1)))
            BASE_POSITIONS[t] = np.array([r * math.cos(angle), r * math.sin(angle)])

def compute_radii(scores, min_r=8, max_r=25):
    """Розраховує радіуси бульбашок відповідно до рейтингу."""
    vals = np.array(list(scores.values()))
    if len(vals) == 0: return {}

    s_min, s_max = vals.min(), vals.max()
    radii = {}

    for t, s in scores.items():
        if s_max == s_min:
            norm = 0.5
        else:
            norm = (s - s_min) / (s_max - s_min)
        radii[t] = min_r + norm * (max_r - min_r)
    return radii

def resolve_collisions(coords, radii, teams, iterations=30):
    """Алгоритм для уникнення перекриття бульбашок."""
    pos = coords.copy()
    keys = list(pos.keys())

    for _ in range(iterations):
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                t1, t2 = keys[i], keys[j]
                p1, p2 = pos[t1], pos[t2]
                r1, r2 = radii[t1], radii[t2]

                diff = p2 - p1
                dist = np.linalg.norm(diff)
                # ЗБІЛЬШЕНА МІНІМАЛЬНА ВІДСТАНЬ ДЛЯ РОЗРІДЖЕННЯ ГРАФА
                min_dist = r1 + r2 + 8.0

                if dist < min_dist:
                    if dist == 0:
                        diff = np.random.randn(2)
                        dist = 0.1

                    overlap = (min_dist - dist) * 0.5
                    correction = (diff / dist) * overlap
                    pos[t1] -= correction
                    pos[t2] += correction
    return pos

# ==========================================
# 3. МАЛЮВАННЯ
# ==========================================

def get_team_color(scores):
    """Призначає колір відповідно до рейтингу (Топ-1 та 3 групи)."""
    sorted_teams_by_score = sorted(scores.keys(), key=lambda t: scores[t])
    N = len(sorted_teams_by_score)

    color_map = {}
    if N == 0: return {}

    # 1. УНІКАЛЬНИЙ ТОП-1
    top_team = sorted_teams_by_score[-1]
    color_map[top_team] = STYLE["team_colors"]["green_unique"]

    if N > 1:
        num_remaining = N - 1
        T = num_remaining // 3

        for i in range(num_remaining):
            # Перебір решти команд від низу догори
            team_r = sorted_teams_by_score[i]

            if i < T:
                color_map[team_r] = STYLE["team_colors"]["violet"]      # Низький рейтинг
            elif i < 2 * T:
                color_map[team_r] = STYLE["team_colors"]["orange"]      # Середній
            else:
                color_map[team_r] = STYLE["team_colors"]["green_secondary"] # Високий

    return color_map


def draw_frame(ax, scores, history_matches, coords, radii, total_matches, is_final_static=False):
    ax.clear()
    ax.set_facecolor(STYLE["bg"])
    ax.axis('off')
    ax.set_aspect('equal')

    # АВТО-МАСШТАБ З ДОДАТКОВИМ ПРОСТОРОМ (ДЛЯ ВІЛЬНОГО ПОЛЯ)
    all_x = [p[0] for p in coords.values()]
    all_y = [p[1] for p in coords.values()]

    if all_x and all_y:
        max_coord = max(max(np.abs(all_x)), max(np.abs(all_y)))
        max_radius = max(radii.values()) if radii else 20
        # ЗБІЛЬШЕНО ВІДСТУП: 40 замість 25
        limit = max(110, max_coord + max_radius + 40)
    else:
        limit = 110

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    color_map = get_team_color(scores)
    # Сортуємо команди за розміром, щоб менші не ховалися за великими
    sorted_teams = sorted(scores.keys(), key=lambda t: radii[t], reverse=True)

    # --- 1. СТРІЛКИ (МАТЧІ) ---
    for idx, (winner, loser) in enumerate(history_matches):
        if winner in coords and loser in coords:
            p1, p2 = coords[winner], coords[loser]
            is_last_in_list = (idx == len(history_matches) - 1)

            if is_last_in_list and not is_final_static:
                # АКТИВНИЙ МАТЧ (ЧЕРВОНИЙ, ТОВСТИЙ)
                c_color = STYLE["arrow_color_current"]
                c_alpha = 1.0
                c_lw = 4.0
                c_zorder = 2
            else:
                # ІСТОРІЯ (СІРИЙ, ТОНШИЙ)
                c_color = STYLE["arrow_color_history"]
                c_alpha = 0.7
                c_lw = 2.5
                c_zorder = 1

            # Розрахунок точки старту/кінця стрілки (щоб не починалася в центрі бульбашки)
            diff = p2 - p1
            dist = np.linalg.norm(diff)
            if dist > 0:
                dir_vec = diff / dist
                start_p = p1 + dir_vec * radii[winner]
                end_p = p2 - dir_vec * radii[loser]
            else:
                start_p, end_p = p1, p2

            arrow = FancyArrowPatch(
                posA=start_p, posB=end_p,
                arrowstyle=f'-|>,head_width=1.2,head_length=1.0',
                color=c_color, lw=c_lw, alpha=c_alpha, zorder=c_zorder
            )
            ax.add_patch(arrow)

    # --- 2. БУЛЬБАШКИ (ВУЗЛИ) ---
    for team in sorted_teams:
        p = coords[team]
        r = radii[team]
        score = scores[team]

        color = color_map.get(team, STYLE["team_colors"]["violet"])

        # 1. Світіння (задній план)
        glow = Circle(p, r*1.15, color=color, alpha=STYLE["shadow_alpha"], zorder=3)
        ax.add_patch(glow)

        # 2. Коло (основний вузол)
        circle = Circle(p, r, facecolor=color, edgecolor=STYLE["outline_color"], lw=2.5, zorder=4)
        ax.add_patch(circle)

        # 3. ТЕКСТ (назва та відсоток)
        label = f"{team}\n{score*100:.1f}%"

        txt = ax.text(p[0], p[1], label, ha='center', va='center',
                      fontsize=STYLE["font_size"], color=STYLE["text_color"],
                      fontweight='bold', zorder=5)
        # Додавання контуру до тексту для кращої читабельності
        txt.set_path_effects([pe.withStroke(linewidth=3.5, foreground=STYLE["outline_color"])])

    # --- 3. ТЕКСТОВІ ПІДПИСИ ---
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    text_y = -limit + 10

    if history_matches:
        if is_final_static:
             ax.text(0, text_y, "FINAL RANKING", ha='center', fontsize=14, fontweight='bold', color=STYLE["outline_color"])
        else:
            last_w, last_l = history_matches[-1]
            ax.text(0, text_y, f"MATCH: {last_w} vs {last_l}", ha='center', fontsize=12, fontweight='bold', color=STYLE["outline_color"])

    # Лічильник раундів
    if not is_final_static and history_matches:
        ax.text(xlims[1]*0.9, ylims[1]*0.9, f"Round {len(history_matches)}/{total_matches}",
                ha='right', va='top', fontsize=12, color=STYLE["outline_color"])

# ==========================================
# 4. ЗАПУСК
# ==========================================

def run_visualization():
    # 1. Зчитування аргументу командного рядка через sys.argv
    if len(sys.argv) < 2:
        print("Помилка: Необхідно передати шлях до вхідного CSV файлу.")
        print("\nВикористання:")
        print("python visual.py <шлях_до_файлу.csv>")
        return

    csv_path = sys.argv[1] # Шлях до файлу - це перший аргумент

    if not os.path.exists(csv_path):
        print(f"Помилка: файл '{csv_path}' не знайдено!")
        print("\nПеревірте, чи правильно вказано шлях.")
        return

    # Налаштування вихідної папки
    output_dir = "frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Зчитування матчів з CSV
    raw_matches = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None) # Пропускаємо заголовок
            for row in reader:
                if len(row) >= 2:
                    w, l = row[0].strip(), row[1].strip()
                    raw_matches.append((w, l))
    except Exception as e:
        print(f"Помилка зчитування CSV: {e}")
        return

    print(f"Зчитано {len(raw_matches)} матчів з {csv_path}. Починаємо генерувати кадри...")

    matches_dict = {}
    all_teams = set()
    total_matches = len(raw_matches)

    fig, ax = plt.subplots(figsize=(10, 10))
    prev_coords = {}

    final_scores = {}
    final_coords = {}
    final_radii = {}

    # 2. Основний цикл генерації кадрів
    for i in range(total_matches):
        winner, loser = raw_matches[i]

        all_teams.add(winner)
        all_teams.add(loser)

        if loser not in matches_dict:
            matches_dict[loser] = set()
        matches_dict[loser].add(winner)

        # Розрахунок рейтингу на поточному кроці
        current_scores, _ = ranking_table_while(matches_dict, all_teams)

        # Фізика та позиціонування
        get_base_positions(all_teams)
        target_coords = {t: BASE_POSITIONS[t] * 0.9 for t in all_teams}

        # Інерція (плавність руху): 70% старої позиції, 30% нової
        coords = {}
        for t in all_teams:
            if t in prev_coords:
                coords[t] = prev_coords[t] * 0.7 + target_coords[t] * 0.3
            else:
                coords[t] = target_coords[t]

        radii = compute_radii(current_scores)
        coords = resolve_collisions(coords, radii, list(all_teams))
        prev_coords = coords.copy()

        # Зберігаємо фінальні дані
        final_scores = current_scores
        final_coords = coords
        final_radii = radii

        # Малюємо та зберігаємо поточний кадр
        history_so_far = raw_matches[:i+1]
        draw_frame(ax, current_scores, history_so_far, coords, radii, total_matches, is_final_static=False)

        fname = os.path.join(output_dir, f"step_{i+1:03d}.png")
        plt.savefig(fname, dpi=100, bbox_inches='tight')
        print(f"Збережено: {fname}")

    # === 3. ФІНАЛЬНИЙ СТАТИЧНИЙ КАДР ===
    print("\nЗберігаємо фінальний результат...")
    draw_frame(ax, final_scores, raw_matches, final_coords, final_radii, total_matches, is_final_static=True)

    final_name = os.path.join(output_dir, "final_result.png")
    plt.savefig(final_name, dpi=150, bbox_inches='tight')

    print(f"Готово! Фінальний файл: {final_name}")
    plt.close()

if __name__ == "__main__":
    run_visualization()
