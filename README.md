# Guitar Fretboard (Python)

This project is a **pure Python library** for generating high-quality guitar fretboard diagrams. It produces standalone SVG diagrams with zero external dependencies.

## ✨ Features
*   **Zero Dependencies**: Generates pure SVG diagrams with pure Python.
*   **Music Theory Logic**: Parses chords, intervals, modes, generates full scales **and Arpeggios**.
*   **CAGED System Support**: Filter or visually highlight scales using the 5 classic CAGED positions.
*   **Chord Logic**: 
    *   **Chord Detection**: Automatically identifies chord names and inversions from notes on the fretboard.
    *   **Chord Dictionary**: Easy placement of common shapes (Major, Minor, 7ths, Barre chords).
*   **Modern Interfaces**:
    *   **CLI Tool**: Create diagrams directly from your terminal.
    *   **Web App**: Interactive Streamlit application for real-time preview (see `app.py`).
*   **Full Parity**: Supports Chord mode (vertical), Left-handed mode, Split notes, Highlights, and Shaded notes.

## 🚀 Installation

It is recommended to install the package inside a Python virtual environment.

```bash
# Clone the repository and navigate to it
git clone <repository_url>
cd guitarfretboard-standalone

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package and its dependencies (including Streamlit)
pip install -e .
```

---

## 💻 1. Web Application (Interactive)

The easiest way to generate diagrams is through the included interactive Web App. It allows you to select scales, chords, tunings, and visual styles through a graphical interface.

```bash
streamlit run app.py
```
This will open a new tab in your browser where you can instantly preview and download your SVG diagrams.

---

## 🖥️ 2. Command Line Interface (CLI)

You can generate diagrams directly from your terminal using the `guitarfretboard` command.

**Basic Scale Generation:**
```bash
# Generate a G Major scale diagram
guitarfretboard --root "G" --scale "M" --output g_major.svg
```

**Available Options:**
* `--scale`: Scale type (e.g., 'M', 'm', 'p', 'M7')
* `--root`: Root note (e.g., 'C', 'G#')
* `--output`: Output file name (default: `fretboard.svg`)
* `--chord`: Render the diagram vertically (for chord boxes)
* `--left`: Render for left-handed players
* `--frets`: Number of frets to display (default: 5)
* `--tuning`: Instrument tuning (`standard`, `dadgad`, `drop d`, `bass standard`, `ukulele standard`, etc.)

**Example for a Bass:**
```bash
guitarfretboard --root "E" --scale "m" --tuning "standard bass" --output e_minor_bass.svg
```

---

## 🐍 3. Python API Usage

You can use the library directly inside your own Python scripts for maximum control.

### Example A: Drawing a Custom Scale
```python
from guitarfretboard import Fretboard, render_svg
from guitarfretboard.core import TUNINGS_GUITAR
from guitarfretboard.notes import parse_pitch, parse_interval
from guitarfretboard.scales import get_scale_intervals

# 1. Initialize the fretboard
fb = Fretboard(
    frets_min=0, frets_max=5, 
    tuning=TUNINGS_GUITAR["standard"],
    title="A Minor Pentatonic"
)

# 2. Add notes
root_pitch = parse_pitch("A")
intervals = get_scale_intervals("mP") # Minor Pentatonic

for interval in intervals:
    semitones = parse_interval(interval)
    pitch = (root_pitch + semitones) % 12
    # Highlight the root note
    style = "5" if semitones == 0 else "2" 
    fb.add_note(pitch, style=style)

# 3. Render
render_svg(fb, "a_minor_penta.svg")
```

### Example B: Using the Chord Dictionary & Musical Intelligence
```python
from guitarfretboard import Fretboard, render_svg, CHORD_SHAPES

fb = Fretboard(chord=True, frets_max=5) # 'chord=True' makes it vertical

# Use a predefined 'A minor' barre shape, placed at the 2nd fret (making it B minor)
minor_barre_shape = CHORD_SHAPES["minor"]["barre_a"]
fb.add_chord(minor_barre_shape, base_fret=2, style="5")

# The library can automatically identify the chord you just drew!
identified_name = fb.identify_chord()
fb.title = f"Detected: {identified_name}" # Will show "Detected: B minor"

render_svg(fb, "b_minor_barre.svg")
```

---

## 📸 Feature Showcase

| Chord Mode (Vertical) | Left-Handed Mode |
| :---: | :---: |
| ![vertical_chord](vertical_chord.svg) | ![left_handed_scale](left_handed_scale.svg) |

| Split Notes & Styles | Automated Legend |
| :---: | :---: |
| ![advanced_styles](advanced_styles.svg) | ![horizontal_scale](horizontal_scale.svg) |

## 📜 License

Copyright 2024 patlegu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
