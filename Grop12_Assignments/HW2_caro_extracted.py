import re
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import matplotlib.pyplot as plt


def intersection(D_intercept=10, S_intercept=2, slope=1):
    Q = (D_intercept - S_intercept) / (2 * slope)
    P = D_intercept - slope * Q
    return Q, P


def market_diagram_with_arrows(
    shift: str = "demand_left",
    title: str = "",
    filename: str = "diagram.png",
    output_dir: Path = Path("data") / "output" / "HW2" / "Caro_version",
):
    Q = np.linspace(0, 10, 200)
    D0, S0 = 10 - Q, 2 + Q
    D1, S1 = D0, S0

    # Parallel shifts
    if shift == "demand_left":
        D1 = 8 - Q
    elif shift == "demand_right":
        D1 = 12 - Q
    elif shift == "supply_left":
        S1 = 4 + Q
    elif shift == "supply_right":
        S1 = 0 + Q
    elif shift == "movement_along":
        S1 = 4 + Q

    # Equilibria
    Q0, P0 = intersection(10, 2, 1)
    if shift.startswith("demand"):
        D_int = 8 if shift == "demand_left" else 12
        Q1, P1 = intersection(D_int, 2, 1)
    else:
        S_int = 4 if shift in ("supply_left", "movement_along") else 0
        Q1, P1 = intersection(10, S_int, 1)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(Q, D0, label="D0")
    ax.plot(Q, S0, label="S0")
    if shift.startswith("demand"):
        ax.plot(Q, D1, "--", label="D1")
        q_mid = 4.5
        ax.annotate(
            "",
            xy=(q_mid, 10 - q_mid),
            xytext=(q_mid, (8 if shift == "demand_left" else 12) - q_mid),
            arrowprops=dict(arrowstyle="->", lw=2),
        )
    else:
        ax.plot(Q, S1, "--", label="S1")
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

    # Movement along demand (only for 'movement_along')
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

    # Save to Caro_version folder
    output_dir.mkdir(parents=True, exist_ok=True)
    name = Path(filename).name
    safe_name = re.sub(r"[^A-Za-z0-9_.\-]", "_", name)
    out_path = output_dir / safe_name
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out_path


# Generate all required diagrams
outputs = {
    "Q1a_malta_substitutes.png": ("demand_left", "Q1(a) Malta Guinness: Cheaper substitutes → Demand left"),
    "Q1b_malta_more_producers.png": ("supply_right", "Q1(b) Malta Guinness: Ten new producers → Supply right"),
    "Q1c_malta_income_up.png": ("demand_right", "Q1(c) Malta Guinness: Incomes rise → Demand right"),

    "Q2a_tilapia_income_down.png": ("demand_left", "Q2(a) Tilapia (normal good): Income down → Demand left"),
    "Q2b_tilapia_input_cost_up.png": ("supply_left", "Q2(b) Tilapia: Input costs up → Supply left"),

    "Q3i_air_travel_move_along.png": ("movement_along", "Q3(i) Air travel: Higher fares → Move along D"),
    "Q3ii_hotels_complement.png": ("demand_left", "Q3(ii) Hotels: Complement to flights → Demand left"),
    "Q3iii_rentals_complement.png": ("demand_left", "Q3(iii) Rental cars: Complement to flights → Demand left"),

    "Q4_soursop_health_positive.png": ("demand_right", "Q4 Soursop: Positive health info → Demand right"),

    "Q5a_maize_fertilizers.png": ("supply_right", "Q5(a) Maize: Free fertilizers → Supply right"),
    "Q5b_maize_army_worms.png": ("supply_left", "Q5(b) Maize: Army worms destroy fields → Supply left"),
}

out_dir = Path("data") / "output" / "HW2" / "Caro_version"
saved_paths = [market_diagram_with_arrows(shift, title, fname, output_dir=out_dir)
               for fname, (shift, title) in outputs.items()]

# Zip them too for convenience
zip_path = out_dir / "clean_diagrams_bundle.zip"
with ZipFile(zip_path, "w") as zf:
    for p in saved_paths:
        zf.write(p, arcname=Path(p).name)

zip_path
