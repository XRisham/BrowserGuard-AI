"""Dataset loader for explicitly synthetic development fixtures."""
import csv
from pathlib import Path


def load_rows() -> tuple[list[str], list[str]]:
    path = Path(__file__).resolve().parents[1] / "datasets" / "synthetic_demo.csv"
    with path.open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    return [row["text"] for row in rows], [row["label"] for row in rows]
