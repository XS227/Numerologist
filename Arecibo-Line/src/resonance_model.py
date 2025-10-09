"""Core routines for preparing data and exploring resonances along the line.

This module exposes a light-weight interface that wraps around machine learning
pipelines. While the exact model architecture is left to the practitioner, the
helpers defined here focus on deterministic preprocessing and interpretation so
that the numerological symbolism remains front-and-centre.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

import numpy as np
import pandas as pd

from .numerology import reduce_to_vibration


@dataclass
class EventPulse:
    """A single entry on the Arecibo line.

    Attributes
    ----------
    name:
        Human-readable label for the pulse (e.g., "Arecibo Message").
    timestamp:
        ISO 8601 timestamp associated with the event.
    vibration:
        Åse vibration derived from the event metadata.
    metadata:
        Additional contextual information, such as frequency or power.
    """

    name: str
    timestamp: pd.Timestamp
    vibration: int
    metadata: dict


def load_event_table(csv_path: Path | str) -> pd.DataFrame:
    """Load an event CSV and append a `vibration` column."""

    df = pd.read_csv(csv_path)
    if "identifier" in df.columns:
        vibration_source: Iterable = df["identifier"]
    elif "timestamp" in df.columns:
        vibration_source = df["timestamp"]
    else:
        # Fall back to the index position to ensure deterministic behaviour.
        vibration_source = df.index

    df["vibration"] = [reduce_to_vibration(value) for value in vibration_source]
    return df


def build_sequence(events: Sequence[EventPulse]) -> np.ndarray:
    """Convert a sequence of :class:`EventPulse` instances into an array."""

    return np.array([pulse.vibration for pulse in events], dtype=np.int16)


def interpret_sequence(sequence: Sequence[int]) -> List[str]:
    """Translate numeric vibrations into short symbolic phrases."""

    phrases = {
        0: "Origin silence",
        1: "Solar translation",
        2: "Dual resonance",
        3: "Creative emergence",
        4: "Stabilising structure",
        5: "Harmonic journey",
        6: "Resonant nurturing",
        7: "Inner reflection",
        8: "Transmutation",
        9: "Completion pulse",
        11: "Gateway alignment",
        22: "Architect frequency",
        33: "Avatar chorus",
    }
    return [phrases.get(value, f"Vibration {value}") for value in sequence]


__all__ = ["EventPulse", "load_event_table", "build_sequence", "interpret_sequence"]
