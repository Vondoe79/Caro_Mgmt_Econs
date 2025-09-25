import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "plot"


def save_all_figures(output_dir: Path, prefix: str = "HW1") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, num in enumerate(plt.get_fignums(), 1):
        fig = plt.figure(num)
        ax = fig.axes[0] if fig.axes else None
        title = ax.get_title() if ax else ""
        name = f"{prefix}_{i}_{_slugify(title)}.png" if title else f"{prefix}_{i}.png"
        fig.savefig(output_dir / name, dpi=300, bbox_inches="tight")
    plt.close("all")

# -----------------
# Graph 1: Cafes vs Employees (Problem 2)
# -----------------
n_values = np.array([0, 14])  # cafes
N_values = 10 * n_values + 120  # employees

plt.figure(figsize=(6, 6))
plt.plot(n_values, N_values, color="blue")
plt.scatter([14, 7], [260, 190], color="red", zorder=5)
plt.text(14, 260, "(14, 260)", ha="right", va="bottom")
plt.text(7, 190, "(7, 190)", ha="right", va="top")
plt.title("Graph of Cafes (n) vs Employees (N)")
plt.xlabel("Number of Cafes (n)")
plt.ylabel("Number of Employees (N)")
plt.grid(True, linestyle="--", alpha=0.6)


# -----------------
# Graph 2: Distance vs Cost (Problem 1)
# -----------------
x_values = np.array([2000, 4000])  # distances
y_values = 2 * x_values - 1000  # costs

plt.figure(figsize=(6, 6))
plt.plot(x_values, y_values, color="green")
plt.scatter([2000, 4000, 3200, 2500], [3000, 7000, 5400, 4000], color="red", zorder=5)
plt.text(2000, 3000, "(2000, 3000)", ha="left", va="bottom")
plt.text(4000, 7000, "(4000, 7000)", ha="right", va="bottom")
plt.text(3200, 5400, "(3200, 5400)", ha="left", va="top")
plt.text(2500, 4000, "(2500, 4000)", ha="left", va="top")
plt.title("Graph of Distance vs Cost of Flight")
plt.xlabel("Distance (km)")
plt.ylabel("Cost (cedis)")
plt.grid(True, linestyle="--", alpha=0.6)


# -----------------
# Graph 3: Paper vs Electronic Copies (Problem 4)
# -----------------
x_vals = np.linspace(0, 40000, 200)

# Equation 1: y = 35000 - x
y1 = 35000 - x_vals

# Equation 2: y = (9750000 - 300x)/250  (i.e., 300x + 250y = 9,750,000)
y2 = (9750000 - 300 * x_vals) / 250

plt.figure(figsize=(6, 6))
plt.plot(x_vals, y1, label="x + y = 35000", color="blue")
plt.plot(x_vals, y2, label="300x + 250y = 9,750,000", color="orange")

# Compute the exact intersection point of the two lines
import numpy as _np
_A = _np.array([[1, 1], [300, 250]], dtype=float)
_b = _np.array([35000, 9750000], dtype=float)
_x_int, _y_int = _np.linalg.solve(_A, _b)

# Annotate the intersection point
plt.scatter([_x_int], [_y_int], color="red", zorder=5)
plt.text(_x_int, _y_int, f"({_x_int:.0f}, {_y_int:.0f})", ha="left", va="bottom")
plt.title("Graph of Paper vs Electronic Copies")
plt.xlabel("Paper Copies (x)")
plt.ylabel("Electronic Copies (y)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

# Save all generated figures to data/output/HW1
save_all_figures(Path("data") / "output" / "HW1", prefix="HW1")
