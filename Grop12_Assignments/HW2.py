import re
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "plot"


def intersection(D_intercept=10, S_intercept=2, slope=1):
    """
    Solve for intersection of:
      Demand:  P = D_intercept - slope*Q
      Supply:  P = S_intercept + slope*Q
    Returns (Q*, P*)
    """
    Q = (D_intercept - S_intercept) / (2 * slope)
    P = D_intercept - slope * Q
    return Q, P


def market_diagram_with_arrows(
    shift: str = "demand_left",
    title: str = "",
    output_dir: Path = Path("data") / "output" / "HW2" / "hw2_output",
    prefix: str = "HW2",
):
    """
    Draws supply-demand with initial curves (D0, S0), shifted curve (D1 or S1),
    marks equilibria E0 and E1, and adds arrows indicating the direction of change.

    shift in {"demand_left","demand_right","supply_left","supply_right","movement_along"}
    """
    Q = np.linspace(0, 10, 200)
    # Base curves
    D0 = 10 - Q  # Demand: P = 10 - Q
    S0 = 2 + Q  # Supply: P = 2 + Q

    # Default shifted curves
    D1 = D0
    S1 = S0

    # Shift logic (parallel shifts)
    if shift == "demand_left":
        D1 = 8 - Q  # leftward / inward
    elif shift == "demand_right":
        D1 = 12 - Q  # rightward / outward
    elif shift == "supply_left":
        S1 = 4 + Q  # leftward / inward
    elif shift == "supply_right":
        S1 = 0 + Q  # rightward / outward
    elif shift == "movement_along":
        # model: supply shifts left; demand unchanged (movement along demand)
        S1 = 4 + Q

    # Compute equilibria
    Q0, P0 = intersection(10, 2, 1)
    if shift.startswith("demand"):
        # changed demand vs same supply
        D_int = 8 if shift == "demand_left" else 12
        Q1, P1 = intersection(D_int, 2, 1)
    elif shift.startswith("supply") or shift == "movement_along":
        S_int = 4 if shift in ("supply_left", "movement_along") else 0
        Q1, P1 = intersection(10, S_int, 1)
    else:
        Q1, P1 = Q0, P0

    # Plot
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(Q, D0, label="D0")
    ax.plot(Q, S0, label="S0")
    if shift in ("demand_left", "demand_right"):
        ax.plot(Q, D1, linestyle="--", label="D1")
        # arrow showing demand shift at mid-Q
        q_mid = 4.5
        ax.annotate(
            "",
            xy=(q_mid, 10 - q_mid),
            xytext=(q_mid, (8 if shift == "demand_left" else 12) - q_mid),
            arrowprops=dict(arrowstyle="->", lw=2),
        )
    elif shift in ("supply_left", "supply_right", "movement_along"):
        ax.plot(Q, S1, linestyle="--", label="S1")
        # arrow showing supply shift at mid-Q
        q_mid = 4.5
        ax.annotate(
            "",
            xy=(q_mid, 2 + q_mid),
            xytext=(q_mid, (4 if shift != "supply_right" else 0) + q_mid),
            arrowprops=dict(arrowstyle="->", lw=2),
        )

    # Mark equilibria
    ax.scatter([Q0], [P0], zorder=5)
    ax.text(Q0, P0, " E0", va="bottom", ha="left")
    ax.scatter([Q1], [P1], zorder=5)
    ax.text(Q1, P1, " E1", va="bottom", ha="left")

    # Arrow indicating movement along demand (only for 'movement_along')
    if shift == "movement_along":
        ax.annotate("", xy=(Q1, P1), xytext=(Q0, P0), arrowprops=dict(arrowstyle="->", lw=2))

    ax.set_title(title)
    ax.set_xlabel("Quantity (Q)")
    ax.set_ylabel("Price (P)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    fig.tight_layout()

    # Build output path and save
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = _slugify(title) if title else f"{shift}"
    filename = f"{prefix}_{stem}.png"
    out_path = output_dir / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out_path


# Regenerate all diagrams to the specified output folder
out_dir = Path("data") / "output" / "HW2" / "hw2_output"

saved_paths = [
    market_diagram_with_arrows("demand_left", "Malta Guinness: Cheaper substitutes → Demand left", out_dir),
    market_diagram_with_arrows("supply_right", "Malta Guinness: More producers → Supply right", out_dir),
    market_diagram_with_arrows("demand_right", "Malta Guinness: Income rises → Demand right", out_dir),

    market_diagram_with_arrows("demand_left", "Tilapia: Income falls → Demand left", out_dir),
    market_diagram_with_arrows("supply_left", "Tilapia: Input costs rise → Supply left", out_dir),

    market_diagram_with_arrows("movement_along", "Airfares: Higher prices (cost shock) → Move along D", out_dir),
    market_diagram_with_arrows("demand_left", "Hotels: Complement to flights → Demand left", out_dir),
    market_diagram_with_arrows("demand_left", "Rental cars: Complement to flights → Demand left", out_dir),

    market_diagram_with_arrows("demand_right", "Soursop: Positive health info → Demand right", out_dir),

    market_diagram_with_arrows("supply_right", "Maize: Free fertilizers → Supply right", out_dir),
    market_diagram_with_arrows("supply_left", "Maize: Army worms destroy fields → Supply left", out_dir),
]

saved_paths

