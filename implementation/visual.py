# import matplotlib.pyplot as plt
# import numpy as np
# import networkx as nx
# from backend import read_matches
# from compare import ranking_table_while

# def page_rank_visualization(matches, rank_dict):

#     teams = list(rank_dict.keys())
#     scores = np.array(list(rank_dict.values()))
#     perc = scores / scores.sum() * 100

#     # sort by score
#     idx = np.argsort(scores)[::-1]
#     teams = [teams[i] for i in idx]
#     scores = scores[idx]
#     perc = perc[idx]

#     # node sizes
#     min_size = 300
#     max_size = 6000
#     bubble_sizes = min_size + (scores - scores.min())/(scores.max() - scores.min())*(max_size - min_size)

#     # ====== BUILD GRAPH JUST LIKE THE EXAMPLE ======
#     G = nx.DiGraph()

#     for t in teams:
#         G.add_node(t)

#     # build loose linking so layout is nice
#     for i in range(len(teams) - 1):
#         G.add_edge(teams[i], teams[i+1])

#     # spring layout = EXACT visual look from example picture
#     pos = nx.spring_layout(
#         G,
#         k=1.7,             # spacing factor (bigger => more spread)
#         iterations=250     # stabilizes
#     )

#     # ====== COLOR MAP LIKE EXAMPLE ======
#     # continuous gradient: yellow -> orange -> red
#     from matplotlib.colors import Normalize
#     from matplotlib import cm

#     norm = Normalize(vmin=scores.min(), vmax=scores.max())
#     cmap = cm.get_cmap('autumn')   # exactly like picture
#     node_colors = [cmap(norm(v)) for v in scores]

#     # ====== DRAW BIG FIGURE ======
#     fig, ax = plt.subplots(figsize=(18, 10))
#     fig.set_size_inches(24, 14, forward=True)
#     ax.set_facecolor("white")   # white like example

#     # draw edges with arrows
#     nx.draw_networkx_edges(
#         G, pos,
#         edge_color="#BBBBBB",
#         arrows=True,
#         arrowsize=18,
#         width=1.5,
#         alpha=0.9
#     )

#     # draw nodes
#     nx.draw_networkx_nodes(
#         G, pos,
#         node_size=bubble_sizes,
#         node_color=node_colors,
#         alpha=0.95,
#         linewidths=1.5,
#         edgecolors="white"
#     )

#     # labels
#     nx.draw_networkx_labels(
#         G, pos,
#         labels={teams[i]: f"{teams[i]} {perc[i]:.1f}%" for i in range(len(teams))},
#         font_size=9,
#         font_weight="bold",
#         font_color="black"
#     )

#     ax.set_xticks([])
#     ax.set_yticks([])

#     ax.set_title(
#         "PageRank Graph Visualization",
#         fontsize=18,
#         fontweight="bold",
#         color="black",
#         pad=15
#     )

#     plt.tight_layout()
#     plt.show()


# if __name__ == "__main__":
#     matches, teams = read_matches("data/new_table.csv")
#     rankings, its = ranking_table_while(matches, teams)
#     page_rank_visualization(matches, rankings)








import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

from backend import read_matches
from compare import ranking_table_while


BASE_POSITIONS = {}


def bubble_map(rank_dict, edge_list, ax, grow_factor=1.0):
    ax.clear()

    teams = np.array(list(rank_dict.keys()))
    scores = np.array(list(rank_dict.values()))
    perc = scores / scores.sum() * 100

    idx = np.argsort(scores)[::-1]
    teams = teams[idx]
    scores = scores[idx]
    perc = perc[idx]

    # bigger bubbles
    min_size = 3500
    max_size = 140000
    bubble_sizes = min_size + (scores - scores.min())/(scores.max() - scores.min())*(max_size - min_size)
    target_radii = np.sqrt(bubble_sizes / np.pi)

    min_radius = 1.0
    radii = min_radius + grow_factor * (target_radii - min_radius)


    colors = []
    for i in range(len(teams)):
        if i < 3:
            colors.append("#00CC00")
        elif scores[i] > np.percentile(scores, 40):
            colors.append("#FF7A00")
        else:
            colors.append("#E10000")

    ax.set_facecolor("white")

    ax.set_xlim(-55, 55)
    ax.set_ylim(-55, 55)
    ax.set_aspect("equal")

    global BASE_POSITIONS
    for t in teams:
        if t not in BASE_POSITIONS:
            BASE_POSITIONS[t] = np.random.uniform(-45, 45, size=2)

    gravity = (scores - scores.min()) / (scores.max() - scores.min())

    coords = {}
    center = np.array([0.0, 0.0])

    for i, t in enumerate(teams):
        base = BASE_POSITIONS[t]
        g = gravity[i]
        final_pos = base * (1 - g) + center * g
        coords[t] = center * (1 - grow_factor) + final_pos * grow_factor

    for i, t in enumerate(teams):
        x, y = coords[t]

        circle = Circle(
            (x, y),
            (radii[i] / 80) * 2.0,
            color=colors[i],
            alpha=0.95
        )
        ax.add_patch(circle)

        ax.text(
            x, y,
            f"{t}\n{perc[i]:.1f}%",
            ha="center", va="center",
            fontsize=9,
            fontweight="bold",
            color="black"
        )

    for (src, dst) in edge_list:
        if src in coords and dst in coords:
            x1, y1 = coords[src]
            x2, y2 = coords[dst]

            i_src = teams.tolist().index(src)
            i_dst = teams.tolist().index(dst)

            r1 = (radii[i_src] / 80) * 2.0
            r2 = (radii[i_dst] / 80) * 2.0

            v = np.array([x2 - x1, y2 - y1])
            d = np.linalg.norm(v)
            if d == 0:
                continue
            direction = v / d

            start = np.array([x1, y1]) + direction * r1
            end = np.array([x2, y2]) - direction * r2

            ax.annotate(
                "",
                xy=end,
                xytext=start,
                arrowprops=dict(
                    arrowstyle="->",
                    lw=1.5,
                    color="black",
                    alpha=0.65
                )
            )

    ax.set_xticks([])
    ax.set_yticks([])


def animate_matches(matches, teams):
    match_keys = list(matches.keys())
    fig, ax = plt.subplots(figsize=(14, 9))

    history = []

    for i in range(1, len(match_keys) + 1):
        partial = {k: matches[k] for k in match_keys[:i]}
        rankings, _ = ranking_table_while(partial, teams)
        history.append(rankings.copy())

    def frame(step):
        grow_factor = (step + 1) / len(history)


        row = matches[match_keys[step]]

        if isinstance(row, (list, tuple)):
            if len(row) == 2:
                edge_now = [(row[0], row[1])]
                match_text = f"{row[0]} vs {row[1]}"
            else:
                edge_now = [(row[i], row[i + 1]) for i in range(0, len(row), 2)]
                match_text = " | ".join([f"{a} vs {b}" for a, b in edge_now])
        else:
            edge_now = []
            match_text = ""

        bubble_map(history[step], edge_now, ax, grow_factor=grow_factor)

        ax.set_title(
            f"THIS ROUND: {match_text}",
            fontsize=14,
            fontweight="bold",
            pad=20
        )

    _ = FuncAnimation(fig, frame, frames=len(history), interval=1600, repeat=True)
    plt.show()


if __name__ == "__main__":
    # matches, teams = read_matches("data/new_table.csv")
    matches, teams = read_matches("data/test_matches.csv")
    animate_matches(matches, teams)
