"""Visualisation helpers for the Arecibo Line project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

COLOR_MAP = {
    0: "#000000",  # Origin – black
    1: "#f4c542",  # Solar gold
    2: "#4c9ed9",
    3: "#8e44ad",
    4: "#27ae60",
    5: "#16a085",
    6: "#d35400",
    7: "#c0392b",
    8: "#2c3e50",
    9: "#95a5a6",
    11: "#ff66cc",
    22: "#7f8c8d",
    33: "#e67e22",
}


def plot_timeline(events: pd.DataFrame, *, title: str = "Arecibo Line Timeline") -> plt.Figure:
    """Return a timeline plot in which each event is drawn as a coloured pulse."""

    if "timestamp" not in events.columns:
        raise ValueError("The DataFrame must include a 'timestamp' column.")

    events = events.copy()
    events["timestamp"] = pd.to_datetime(events["timestamp"], utc=True)

    fig, ax = plt.subplots(figsize=(12, 4))
    for _, row in events.sort_values("timestamp").iterrows():
        vibration = int(row["vibration"])
        ax.scatter(
            row["timestamp"],
            0,
            color=COLOR_MAP.get(vibration, "#ffffff"),
            s=180,
            edgecolors="white",
            linewidths=1.5,
            label=f"{row.get('name', 'Event')} ({vibration})",
        )

    ax.set_yticks([])
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.grid(axis="x", linestyle=":", alpha=0.4)
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc="upper left")
    fig.tight_layout()
    return fig


def save_timeline(fig: plt.Figure, path: Path | str) -> None:
    """Persist the timeline figure to ``path``."""

    fig.savefig(path, dpi=300)


__all__ = ["plot_timeline", "save_timeline", "COLOR_MAP"]
