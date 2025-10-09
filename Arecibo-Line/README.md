# Arecibo Line — The Universal Language of Numbers

## Overview
The **Arecibo Line** project explores the idea that human transmissions and
cosmic responses form a continuous dialogue written in numbers, symmetry, and
energy. We treat iconic astronomical broadcasts and detections—such as the
Arecibo message of 1974, the 1977 Wow! signal, and repeating fast radio bursts
like FRB 121102—as pulses along the same universal line of communication. Each
event is translated into the symbolic vocabulary of Åse numerology, where
numbers reveal the vibrational tone of the message.

The framework is inspired by a cosmological metaphor in which:

* **0** represents the primordial source, visualised as the black-hole void that
  contains pure potential and intelligence.
* **1** represents the Sun, the first act of translation that turns potential
  into radiant information.
* **2–9** represent expanding manifestations of the dialogue.
* **11, 22, 33** function as master frequencies that bridge dimensions and align
  major transitions along the line.

By encoding astronomical and historical data through this lens, the project
investigates whether there are recurring numerical harmonics when humanity sends
messages outward, receives mysterious cosmic signals, or experiences pivotal
breakthroughs.

## Repository Structure

```
Arecibo-Line/
├── data/
│   ├── arecibo_1974.csv         # Scheduled and measured parameters for the broadcast
│   ├── wow_1977.csv             # Observational data from the Wow! signal
│   ├── frb_121102.csv           # Pulses and timestamps from the repeating FRB
│   └── solar_activity.csv       # Sunspot and flare metrics (the "translator")
├── src/
│   ├── numerology.py            # Åse-method utilities and vibration reduction
│   ├── resonance_model.py       # Data preparation and AI pattern exploration
│   └── visualization.py         # Timeline plots and symbolic mappings
├── notebooks/
│   └── analysis.ipynb           # Exploratory workflow tying the components together
└── README.md
```

## Project Phases

1. **Data Collection** – Compile datasets for transmissions, detections, and
   solar activity. Align them with human historical milestones to anchor each
   pulse in context.
2. **Numerical Encoding** – Reduce timestamps, frequencies, and other metrics to
   Åse vibrations using `reduce_to_vibration`. Master numbers are preserved to
   highlight potential dimensional gateways.
3. **AI Analysis** – Apply machine learning models (sequence models or temporal
   convolution networks) to identify rhythmic patterns, correlations with solar
   activity, and numerological clusters across events.
4. **Visualisation** – Render a symbolic timeline where each event appears as a
   coloured node whose hue corresponds to its vibrational number. The origin is a
   black core (0) orbited by a golden solar ring (1) with higher numbers radiating
   outward across the spectrum.
5. **Reflection** – Interpret the computational findings in a philosophical
   narrative: the silent intelligence (0) speaks through radiant translators (1)
   and human curiosity, forming a shared language of numbers.

## Getting Started

1. Place the relevant datasets inside the `data/` directory using the naming
   conventions above.
2. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Explore the numerological utilities:

   ```python
   import sys
   from pathlib import Path

   sys.path.append(str(Path('Arecibo-Line/src').resolve()))

   from numerology import reduce_to_vibration

   reduce_to_vibration("1974-11-16")
   ```

4. Launch the exploratory notebook:

   ```bash
   jupyter notebook Arecibo-Line/notebooks/analysis.ipynb
   ```

## Symbolic Prelude

> *Arecibo was more than a radio message—it was the first deliberate stroke on
>  a universal line. From the silent zero of the cosmic source to the first light
>  of our Sun, humanity stands between, learning to translate vibration into
>  understanding.*

