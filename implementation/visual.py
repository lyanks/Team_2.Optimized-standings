import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
import numpy as np
import math
import os
import csv

# ==========================================
# PAGERANK АЛГОРИТМ
# ==========================================

def calculate_pagerank(matches_dict, teams, damping=0.85, iterations=100):
    """
    Розраховує PageRank для команд на основі перемог.
    matches_dict: {loser: {winners who beat them}}
    """
    n = len(teams)
    if n == 0:
        return {}

    teams_list = list(teams)
    team_idx = {t: i for i, t in enumerate(teams_list)}

    # Ініціалізація рівномірно
    scores = np.ones(n) / n

    # Будуємо матрицю переходів
    # Якщо A переміг B, то B "передає" свій рейтинг A
    out_degree = {t: 0 for t in teams}

    for loser, winners in matches_dict.items():
        out_degree[loser] = len(winners)

    # PageRank ітерації
    for _ in range(iterations):
        new_scores = np.ones(n) * (1 - damping) / n

        for loser, winners in matches_dict.items():
            if out_degree[loser] > 0:
                loser_idx = team_idx[loser]
                contribution = damping * scores[loser_idx] / out_degree[loser]

                for winner in winners:
                    winner_idx = team_idx[winner]
                    new_scores[winner_idx] += contribution

        # Для команд без поразок - розподіляємо рівномірно
        dangling_sum = 0
        for t in teams:
            if t not in matches_dict or len(matches_dict.get(t, set())) == 0:
                dangling_sum += scores[team_idx[t]]

        new_scores += damping * dangling_sum / n
        scores = new_scores

    # Нормалізуємо
    scores = scores / scores.sum()

    return {teams_list[i]: scores[i] for i in range(n)}

# ==========================================
# СТИЛЬ
# ==========================================
STYLE = {
    "bg": "#FADEC9",
    "arrow_color": "#1a1a1a",
    "text_color": "#1a1a1a",
    "portal_color": "#1a1a1a",
    "font_size": 11,
}

def get_team_color(rank_ratio):
    """Колір на основі рангу (0 = топ, 1 = низ)"""

    if rank_ratio < 0.33:
        # Топ-команди: зелений (раніше був жовтий)
        return {"inner": "#7DFF7A", "outer": "#1F8A0A"}  # зелений

    elif rank_ratio < 0.66:
        # Середні команди: тепер ЖОВТИЙ замість оранжевого
        return {"inner": "#FFE66D", "outer": "#E1B800"}  # жовтий

    else:
        # Нижні команди: червоний (замінено замість фіолетового)
        return {"inner": "#FF4C4C", "outer": "#8A0000"}  # червоний

def draw_sphere(ax, center, radius, colors, zorder=5):
    """Малює сферу з градієнтом"""
    cx, cy = center
    n_rings = 35

    for i in range(n_rings, 0, -1):
        ratio = i / n_rings
        r = radius * ratio

        c_inner = np.array(plt.cm.colors.to_rgb(colors["inner"]))
        c_outer = np.array(plt.cm.colors.to_rgb(colors["outer"]))

        t = ratio ** 0.7
        color = c_outer * (1 - t) + c_inner * t

        circle = Circle((cx, cy), r, facecolor=color, edgecolor='none', zorder=zorder)
        ax.add_patch(circle)

def get_circular_positions(scores, radii):
    """Розташування по колу"""
    sorted_teams = sorted(scores.keys(), key=lambda t: scores[t], reverse=True)
    n = len(sorted_teams)

    if n == 0:
        return {}
    if n == 1:
        return {sorted_teams[0]: np.array([0.0, 0.0])}

    max_r = max(radii.values()) if radii else 30
    circle_radius = max(90, n * max_r * 0.6)

    positions = {}
    for i, team in enumerate(sorted_teams):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = circle_radius * math.cos(angle)
        y = circle_radius * math.sin(angle)
        positions[team] = np.array([x, y])

    return positions

def resolve_collisions(coords, radii, iterations=60):
    """Розсування кіл"""
    pos = {k: v.copy() for k, v in coords.items()}
    keys = list(pos.keys())

    for _ in range(iterations):
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                t1, t2 = keys[i], keys[j]
                p1, p2 = pos[t1], pos[t2]
                r1, r2 = radii[t1], radii[t2]

                diff = p2 - p1
                dist = np.linalg.norm(diff)
                min_dist = r1 + r2 + 8

                if dist < min_dist and dist > 0:
                    overlap = (min_dist - dist) * 0.5
                    correction = (diff / dist) * overlap
                    pos[t1] = pos[t1] - correction
                    pos[t2] = pos[t2] + correction

    return pos

def compute_radii(scores, min_r=18, max_r=55):
    """Радіуси на основі score"""
    vals = np.array(list(scores.values()))
    if len(vals) == 0:
        return {}

    s_min, s_max = vals.min(), vals.max()
    radii = {}

    for t, s in scores.items():
        if s_max == s_min:
            norm = 0.5
        else:
            norm = (s - s_min) / (s_max - s_min)
        radii[t] = min_r + (norm ** 0.5) * (max_r - min_r)

    return radii

def draw_portal(ax, x_pos, y_range):
    """Крива портала"""
    y = np.linspace(y_range[0], y_range[1], 100)
    x = x_pos + 10 * np.sin(y * 0.03)
    ax.plot(x, y, color=STYLE["portal_color"], lw=2.5, alpha=0.7, zorder=1)

def draw_new_node_box(ax, center, radius):
    """Новий вузол у рамці"""
    x, y = center
    box_size = radius * 3

    rect = FancyBboxPatch(
        (x - box_size/2, y - box_size/2),
        box_size, box_size,
        boxstyle="square,pad=0.02",
        facecolor='none',
        edgecolor=STYLE["portal_color"],
        lw=1.5, zorder=3
    )
    ax.add_patch(rect)

    colors = {"inner": "#FF8C42", "outer": "#D64A00"}
    draw_sphere(ax, center, radius, colors, zorder=4)

    ax.text(x, y - box_size/2 - 8, "new node",
            ha='center', va='top', fontsize=9,
            color=STYLE["text_color"], style='italic')

def draw_frame(ax, scores, history_matches, coords, radii, total_matches,
               new_teams=None, is_final_static=False, match_num=0):
    """Малює кадр"""
    ax.clear()
    ax.set_facecolor(STYLE["bg"])
    ax.axis('off')
    ax.set_aspect('equal')

    # Межі
    all_x = [p[0] for p in coords.values()]
    all_y = [p[1] for p in coords.values()]

    if all_x and all_y:
        max_r = max(radii.values()) if radii else 25
        x_min = min(all_x) - max_r - 40
        x_max = max(all_x) + max_r + 100
        y_min = min(all_y) - max_r - 50
        y_max = max(all_y) + max_r + 50
    else:
        x_min, x_max = -150, 200
        y_min, y_max = -120, 120

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Заголовок
    ax.text((x_min + x_max) / 2, y_max - 5, "Tournament PageRank",
            ha='center', va='top', fontsize=20, fontweight='bold',
            color=STYLE["text_color"])

    # Ранги
    sorted_teams = sorted(scores.keys(), key=lambda t: scores[t], reverse=True)
    n = len(sorted_teams)
    rank_map = {t: i / max(n - 1, 1) for i, t in enumerate(sorted_teams)}

    # Портал і нові вузли
    portal_x = x_max - 60

    if new_teams and len(new_teams) > 0:
        draw_portal(ax, portal_x, (y_min + 30, y_max - 40))

        display_new = new_teams[-3:]
        y_positions = [50, 0, -50]

        for i, team in enumerate(display_new):
            if i < len(y_positions):
                node_center = np.array([portal_x + 35, y_positions[i]])
                draw_new_node_box(ax, node_center, 12)

                if team in coords:
                    target = coords[team]
                    target_r = radii.get(team, 15)

                    diff = node_center - target
                    dist = np.linalg.norm(diff)
                    if dist > 0:
                        dir_vec = diff / dist
                        line_start = target + dir_vec * target_r
                        line_end = np.array([node_center[0] - 18, node_center[1]])

                        ax.plot([line_start[0], line_end[0]],
                               [line_start[1], line_end[1]],
                               '--', color=STYLE["portal_color"], lw=1.5, alpha=0.5, zorder=16)

    # Стрілки
    for idx, (winner, loser) in enumerate(history_matches):
        if winner in coords and loser in coords:
            p1, p2 = coords[winner], coords[loser]
            r1, r2 = radii.get(winner, 15), radii.get(loser, 15)

            diff = p2 - p1
            dist = np.linalg.norm(diff)

            if dist > 0:
                dir_vec = diff / dist
                start_p = p1 + dir_vec * r1
                end_p = p2 - dir_vec * r2
            else:
                continue

            is_current = (idx == len(history_matches) - 1) and not is_final_static

            arrow = FancyArrowPatch(
                posA=start_p, posB=end_p,
                arrowstyle='-|>,head_width=1.0,head_length=0.6',
                color='#e74c3c' if is_current else STYLE["arrow_color"],
                lw=2.5 if is_current else 2.0,
                alpha=1.0 if is_current else 0.75,
                zorder=15
            )
            ax.add_patch(arrow)

    # Сфери
    for team in sorted(scores.keys(), key=lambda t: radii[t]):
        p = coords[team]
        r = radii[team]
        score = scores[team]

        colors = get_team_color(rank_map[team])
        draw_sphere(ax, p, r, colors)

        label = f"{team}\n{score*100:.1f}%"
        ax.text(p[0], p[1], label, ha='center', va='center',
               fontsize=STYLE["font_size"], fontweight='bold',
               color=STYLE["text_color"], zorder=20)

    # Підпис
    if is_final_static:
        ax.text((x_min + x_max) / 2, y_min + 20, "🏆 FINAL RANKING 🏆",
                ha='center', fontsize=16, fontweight='bold', color='#2c3e50')
    elif history_matches:
        last_w, last_l = history_matches[-1]
        ax.text((x_min + x_max) / 2, y_min + 20,
                f"⚔️ Match {match_num}/{total_matches}: {last_w} defeats {last_l}",
                ha='center', fontsize=13, fontweight='bold', color='#c0392b')

def run_visualization(csv_path="data/test_matches.csv"):
    if not os.path.exists(csv_path):
        print(f"Помилка: файл {csv_path} не знайдено!")
        return

    output_dir = "frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    raw_matches = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2:
                w, l = row[0].strip(), row[1].strip()
                raw_matches.append((w, l))

    print(f"Зчитано {len(raw_matches)} матчів. Починаємо візуалізацію...\n")

    matches_dict = {}
    all_teams = set()
    total_matches = len(raw_matches)

    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor(STYLE["bg"])

    final_scores = {}
    final_coords = {}
    final_radii = {}

    recently_added = []

    for i in range(total_matches):
        winner, loser = raw_matches[i]

        new_this_round = []
        for t in [winner, loser]:
            if t not in all_teams:
                all_teams.add(t)
                new_this_round.append(t)
                recently_added.append(t)

        recently_added = recently_added[-5:]

        if loser not in matches_dict:
            matches_dict[loser] = set()
        matches_dict[loser].add(winner)

        # Реальний PageRank
        current_scores = calculate_pagerank(matches_dict, all_teams)

        radii = compute_radii(current_scores)
        coords = get_circular_positions(current_scores, radii)
        coords = resolve_collisions(coords, radii)

        final_scores = current_scores
        final_coords = coords
        final_radii = radii

        history_so_far = raw_matches[:i+1]
        draw_frame(ax, current_scores, history_so_far, coords, radii, total_matches,
                  new_teams=recently_added if recently_added else None,
                  is_final_static=False, match_num=i+1)

        fname = os.path.join(output_dir, f"step_{i+1:03d}.png")
        plt.savefig(fname, dpi=120, bbox_inches='tight', facecolor=STYLE["bg"])

        # Виводимо рейтинг
        print(f"Match {i+1}: {winner} → {loser}")
        sorted_scores = sorted(current_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (team, score) in enumerate(sorted_scores, 1):
            print(f"  {rank}. {team}: {score*100:.2f}%")
        print()

    # Фінальний кадр
    print("=" * 50)
    print("FINAL RANKING:")
    print("=" * 50)
    sorted_final = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    for rank, (team, score) in enumerate(sorted_final, 1):
        print(f"{rank}. {team}: {score*100:.2f}%")


    draw_frame(ax, final_scores, raw_matches, final_coords, final_radii,
               total_matches, is_final_static=True)

    final_name = os.path.join(output_dir, "final_result.png")
    plt.savefig(final_name, dpi=150, bbox_inches='tight', facecolor=STYLE["bg"])

    print(f"\nГотово! Фінальний файл: {final_name}")
    plt.close()

    return final_name

if __name__ == "__main__":
    run_visualization()
