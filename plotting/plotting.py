"""Make all figures for ES 404 Assignment 3 (PDFs in figures/)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx

from style import (apply_style, DEEP_PURPLE, MID_LAVENDER, LIGHT_LAVENDER,
                   VERY_LIGHT, GOLD, CREAM_BG, TEXT_COLOR, DARK_PURPLE,
                   ZONE_COLORS, SCEN_A_COLOR, SCEN_B_COLOR, INTERV_COLOR)
from network import NODES, IDX, POPULATIONS, G_CAMPUS, EDGES

apply_style()

BASE  = os.path.join(os.path.dirname(__file__), "..")
DATA  = os.path.join(BASE, "data")
FIGS  = os.path.join(BASE, "figures")
os.makedirs(FIGS, exist_ok=True)


def fig_path(name):
    return os.path.join(FIGS, name)


def load(name):
    return np.load(os.path.join(DATA, name + ".npz"))


# Layout roughly follows the campus diagram: hostels left, dining centre-left,
# academic centre, labs/gate right, sports top-right
POS = {
    "H1":  (-2.5,  0.8),
    "H2":  (-2.5,  0.0),
    "H3":  (-2.5, -0.8),
    "D":   (-0.8,  0.0),
    "L":   ( 0.2, -1.2),
    "A":   ( 0.8,  0.0),
    "Lab": ( 2.0, -0.5),
    "S":   (-0.2,  1.2),
    "G":   ( 2.5,  0.5),
}


# Snapshot colormap
SNAP_CMAP = LinearSegmentedColormap.from_list(
    "infection",
    [CREAM_BG, LIGHT_LAVENDER, MID_LAVENDER, DEEP_PURPLE, DARK_PURPLE],
    N=256,
)


# Figure (a): Campus network graph
def plot_network():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_facecolor(CREAM_BG)

    node_sizes  = [POPULATIONS[IDX[n]] * 0.55 for n in NODES]
    edge_widths = [G_CAMPUS[u][v]["weight"] * 4.5 for u, v in G_CAMPUS.edges()]
    node_colors = [DEEP_PURPLE] * len(NODES)

    nx.draw_networkx_edges(G_CAMPUS, POS, ax=ax,
                           width=edge_widths,
                           edge_color=MID_LAVENDER,
                           alpha=0.7)
    nx.draw_networkx_nodes(G_CAMPUS, POS, ax=ax,
                           node_size=node_sizes,
                           node_color=node_colors,
                           alpha=0.92)
    nx.draw_networkx_labels(G_CAMPUS, POS, ax=ax,
                            font_size=8.5,
                            font_color=CREAM_BG,
                            font_weight="bold")

    # Edge weight labels
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G_CAMPUS.edges(data=True)}
    nx.draw_networkx_edge_labels(G_CAMPUS, POS, edge_labels=edge_labels,
                                  font_size=6.5, font_color=TEXT_COLOR, ax=ax,
                                  bbox=dict(boxstyle="round,pad=0.1",
                                            fc=CREAM_BG, ec="none", alpha=0.7))

    ax.set_title("Campus Contact Network", fontsize=12, color=TEXT_COLOR, pad=10)
    ax.axis("off")

    # Legend: node size, edge width
    for pop, label in [(160, "160"), (320, "320"), (520, "520")]:
        ax.scatter([], [], s=pop * 0.55, c=DEEP_PURPLE, alpha=0.92,
                   label=f"Pop. {label}")
    ax.legend(title="Node size ~ population", loc="lower left",
              frameon=False, fontsize=8, title_fontsize=8)

    fig.tight_layout()
    fig.savefig(fig_path("fig_a_network.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("  fig_a_network.pdf")


# Figure (d): Total infected vs time, both scenarios
def plot_total_infected():
    dA = load("scen_A")
    dB = load("scen_B")
    n  = 9

    tA = dA["t"]; yA = dA["y"]
    tB = dB["t"]; yB = dB["y"]

    total_I_A = yA[n:2*n, :].sum(axis=0)
    total_I_B = yB[n:2*n, :].sum(axis=0)

    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    ax.plot(tA, total_I_A, color=SCEN_A_COLOR, lw=2.0,
            label="Scenario A: H2 seed")
    ax.plot(tB, total_I_B, color=SCEN_B_COLOR, lw=2.0, ls="--",
            label="Scenario B: academic core seed")

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Total infected (persons)")
    ax.set_title("Total infected on campus", fontsize=11)
    ax.legend()
    ax.set_xlim(0, 30)

    fig.tight_layout()
    fig.savefig(fig_path("fig_d_total_infected.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("  fig_d_total_infected.pdf")


# Figure (e): Per-zone infected curves (4 key zones, both scenarios)
def plot_per_zone():
    dA = load("scen_A"); dB = load("scen_B")
    n = 9

    # H2 (seed A), A (seed B, hub), D (bridge), G (peripheral)
    highlight = ["H2", "A", "D", "G"]
    styles    = ["-", "--", "-.", ":"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=False)

    for ax, (d, title, scen_col) in zip(axes, [
            (dA, "Scenario A: H2 seed", SCEN_A_COLOR),
            (dB, "Scenario B: academic core seed", SCEN_B_COLOR),
    ]):
        t = d["t"]; y = d["y"]
        for zone, ls in zip(highlight, styles):
            i = IDX[zone]
            I_zone = y[n + i, :]
            ax.plot(t, I_zone, color=ZONE_COLORS[zone], lw=1.8, ls=ls, label=zone)

        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Infected (persons)")
        ax.set_title(title, fontsize=10)
        ax.set_xlim(0, 30)
        ax.legend(fontsize=8.5)

    fig.suptitle("Infected per zone", fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig(fig_path("fig_e_per_zone.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("  fig_e_per_zone.pdf")


# Figure (f): Network snapshots (days 0, 5, 10, 20)
def _snapshot_infected_fractions(y, t_arr, day):
    """Infected fraction per zone at the time point closest to `day`."""
    n = 9
    t_idx = np.argmin(np.abs(t_arr - day))
    I = y[n:2*n, t_idx]
    return I / POPULATIONS


def plot_snapshots():
    snap_days = [0, 5, 10, 20]

    for tag, data_name in [("A", "scen_A"), ("B", "scen_B")]:
        d = load(data_name)
        t = d["t"]; y = d["y"]

        # shared color scale across snapshots
        all_fracs = np.array([
            _snapshot_infected_fractions(y, t, day) for day in snap_days
        ])
        vmax = all_fracs.max()
        vmax = max(vmax, 1e-4)   # avoid zero range

        fig, axes = plt.subplots(1, 4, figsize=(14, 3.8))
        fig.patch.set_facecolor(CREAM_BG)

        for ax, day in zip(axes, snap_days):
            fracs = _snapshot_infected_fractions(y, t, day)
            colors = [SNAP_CMAP(f / vmax) for f in fracs]

            node_sizes = [POPULATIONS[IDX[n_]] * 0.55 for n_ in NODES]
            edge_widths = [G_CAMPUS[u][v]["weight"] * 3.5 for u, v in G_CAMPUS.edges()]

            nx.draw_networkx_edges(G_CAMPUS, POS, ax=ax,
                                   width=edge_widths,
                                   edge_color="#CCBBDD",
                                   alpha=0.6)
            nx.draw_networkx_nodes(G_CAMPUS, POS, ax=ax,
                                   node_size=node_sizes,
                                   node_color=colors)
            nx.draw_networkx_labels(G_CAMPUS, POS, ax=ax,
                                    font_size=7,
                                    font_color="white",
                                    font_weight="bold")

            ax.set_title(f"Day {day}", fontsize=10, color=TEXT_COLOR)
            ax.axis("off")
            ax.set_facecolor(CREAM_BG)

        # Shared colorbar
        sm = plt.cm.ScalarMappable(cmap=SNAP_CMAP,
                                   norm=mcolors.Normalize(vmin=0, vmax=vmax))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=axes, orientation="vertical",
                            fraction=0.018, pad=0.02)
        cbar.set_label("Infected fraction", fontsize=9, color=TEXT_COLOR)
        cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_COLOR)

        seed_label = "H2" if tag == "A" else "Academic core (A)"
        fig.suptitle(f"Scenario {tag} (seed: {seed_label})",
                     fontsize=11, y=1.03, color=TEXT_COLOR)
        fig.tight_layout()
        fig.savefig(fig_path(f"fig_f_snapshots_{tag}.pdf"),
                    format="pdf", bbox_inches="tight")
        plt.close(fig)
        print(f"  fig_f_snapshots_{tag}.pdf")


# Figure (h): Network (Scenario B) vs well-mixed baseline
def plot_wellmixed():
    dB  = load("scen_B")
    dWM = load("wellmixed_B")
    n   = 9

    total_I_B  = dB["y"][n:2*n, :].sum(axis=0)
    I_WM       = dWM["y"][1, :]    # row 1 = I(t) in [S, I, R]

    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    ax.plot(dB["t"],  total_I_B, color=DEEP_PURPLE, lw=2.0,
            label="Network model, scenario B")
    ax.plot(dWM["t"], I_WM,      color=GOLD,        lw=2.0, ls="--",
            label="Well-mixed SIR")

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Total infected (persons)")
    ax.set_title("Network model vs well-mixed SIR", fontsize=11)
    ax.legend()
    ax.set_xlim(0, 30)

    fig.tight_layout()
    fig.savefig(fig_path("fig_h_wellmixed.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("  fig_h_wellmixed.pdf")


# Figure (i): Intervention: H2 isolation at day 7
def plot_intervention():
    dA   = load("scen_A")
    dInt = load("intervention_A")
    n    = 9

    total_I_base = dA["y"][n:2*n, :].sum(axis=0)
    total_I_int  = dInt["y"][n:2*n, :].sum(axis=0)

    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    ax.plot(dA["t"],   total_I_base, color=SCEN_A_COLOR, lw=2.0,
            label="Scenario A, no intervention")
    ax.plot(dInt["t"], total_I_int,  color=INTERV_COLOR, lw=2.0, ls="--",
            label="H2 isolation at day 7 (80% edge reduction)")

    ax.axvline(7, color=TEXT_COLOR, lw=0.9, ls=":", alpha=0.7,
               label="Intervention day")

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Total infected (persons)")
    ax.set_title("H2 isolation from day 7", fontsize=11)
    ax.legend()
    ax.set_xlim(0, 30)

    fig.tight_layout()
    fig.savefig(fig_path("fig_i_intervention.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("  fig_i_intervention.pdf")


if __name__ == "__main__":
    print("Generating figures...")
    plot_network()
    plot_total_infected()
    plot_per_zone()
    plot_snapshots()
    plot_wellmixed()
    plot_intervention()
    print("All figures saved to figures/")
