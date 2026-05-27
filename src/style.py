"""Colours and matplotlib rcParams."""
import matplotlib as mpl
import matplotlib.pyplot as plt

# Palette
DEEP_PURPLE    = "#4B2E83"
MID_LAVENDER   = "#7B5EA7"
LIGHT_LAVENDER = "#B19CD9"
VERY_LIGHT     = "#DDD0F0"
GOLD           = "#C9A961"   # well-mixed / accent
CREAM_BG       = "#FAFAF7"
TEXT_COLOR     = "#2D2D2D"
DARK_PURPLE    = "#1A0A3B"

# Zone-specific colours for per-zone time-series plots
ZONE_COLORS = {
    "H1":  "#7B5EA7",
    "H2":  "#4B2E83",
    "H3":  "#9C78C8",
    "D":   "#C9A961",
    "L":   "#6B8E9F",
    "A":   "#C15F3C",
    "Lab": "#5E9E6E",
    "S":   "#B19CD9",
    "G":   "#A0A0A0",
}

# Scenario line styles
SCEN_A_COLOR = DEEP_PURPLE
SCEN_B_COLOR = GOLD
INTERV_COLOR = MID_LAVENDER


def apply_style():
    """Set global rcParams."""
    mpl.rcParams.update({
        # Font
        "font.family":       "serif",
        "font.serif":        ["Palatino", "Georgia", "DejaVu Serif"],
        "mathtext.fontset":  "dejavuserif",
        "font.size":         10,
        "axes.titlesize":    11,
        "axes.labelsize":    10,
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "legend.fontsize":   9,
        "figure.titlesize":  12,
        # Axes
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.linewidth":    0.8,
        "axes.edgecolor":    TEXT_COLOR,
        "axes.labelcolor":   TEXT_COLOR,
        "axes.facecolor":    CREAM_BG,
        "figure.facecolor":  CREAM_BG,
        # Ticks
        "xtick.color":       TEXT_COLOR,
        "ytick.color":       TEXT_COLOR,
        "xtick.direction":   "out",
        "ytick.direction":   "out",
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        # Grid
        "axes.grid":         False,
        # Lines
        "lines.linewidth":   1.6,
        # Legend
        "legend.frameon":    False,
        # Save
        "savefig.facecolor": CREAM_BG,
        "savefig.dpi":       300,
    })
