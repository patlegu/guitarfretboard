"""
Definitions of musical scales.
Ported from guitar-fretboard.scales.sty.
"""

# Map scale aliases to intervals list
SCALES = {
    # Basic Chords/Scales (Legacy aliases)
    "M": ["1", "3", "5"],
    "m": ["1", "b3", "5"],
    "7": ["1", "3", "5", "b7"],
    "M7": ["1", "3", "5", "7"],
    "m7": ["1", "b3", "5", "b7"],
    "sus2": ["1", "2", "5"],
    "sus4": ["1", "4", "5"],
    "aug": ["1", "3", "S5"],
    "dim": ["1", "3", "b5"],

    # Major Scale Modes (The 7 Church Modes)
    "Ionian": ["1", "2", "3", "4", "5", "6", "7"],
    "Major": ["1", "2", "3", "4", "5", "6", "7"],
    "Dorian": ["1", "2", "b3", "4", "5", "6", "b7"],
    "Phrygian": ["1", "b2", "b3", "4", "5", "b6", "b7"],
    "Lydian": ["1", "2", "3", "S4", "5", "6", "7"],
    "Mixolydian": ["1", "2", "3", "4", "5", "6", "b7"],
    "Aeolian": ["1", "2", "b3", "4", "5", "b6", "b7"],
    "Minor": ["1", "2", "b3", "4", "5", "b6", "b7"],
    "Locrian": ["1", "b2", "b3", "4", "b5", "b6", "b7"],

    # Pentatonic Scales
    "Pentatonic Major": ["1", "2", "3", "5", "6"],
    "MP": ["1", "2", "3", "5", "6"],
    "Pentatonic Minor": ["1", "b3", "4", "5", "b7"],
    "mP": ["1", "b3", "4", "5", "b7"],
    "Blues": ["1", "b3", "4", "b5", "5", "b7"],

    # Harmonic Minor & Modes
    "Harmonic Minor": ["1", "2", "b3", "4", "5", "b6", "7"],
    "Phrygian Dominant": ["1", "b2", "3", "4", "5", "b6", "b7"],
    "Lydian #2": ["1", "S2", "3", "S4", "5", "6", "7"],

    # Melodic Minor & Modes
    "Melodic Minor": ["1", "2", "b3", "4", "5", "6", "7"],
    "Lydian Augmented": ["1", "2", "3", "S4", "S5", "6", "7"],
    "Lydian Dominant": ["1", "2", "3", "S4", "5", "6", "b7"],
    "Altered": ["1", "b2", "b3", "b4", "b5", "b6", "b7"],

    # Symmetric Scales
    "Diminished (H-W)": ["1", "b2", "b3", "3", "S4", "5", "6", "b7"],
    "Diminished (W-H)": ["1", "2", "b3", "4", "b5", "b6", "bb7", "7"],
    "Whole Tone": ["1", "2", "3", "S4", "S5", "S6"],

    # Specialized Chords/Short Scales
    "5": ["1", "5"],
    "b5": ["1", "b5"],
    "S5": ["1", "S5"],
    "7sus4": ["1", "4", "5", "b7"],
    "minMaj7": ["1", "b3", "5", "7"],
    "dim7": ["1", "b3", "b5", "bb7"],
    "m7b5": ["1", "b3", "b5", "b7"],
    "6": ["1", "3", "5", "6"],
    "m6": ["1", "b3", "5", "6"],
    "add9": ["1", "3", "5", "9"],
    "maj9": ["1", "3", "5", "7", "9"],
}

# Aliases to hide from the web UI to keep it clean
HIDE_SCALES = ["M", "m", "MP", "mP", "5", "b5", "S5"]

def get_scale_intervals(scale_name: str) -> list[str]:
    """Return the list of intervals (strings) for a given scale."""
    if scale_name in SCALES:
        return SCALES[scale_name]
    raise ValueError(f"Unknown scale: {scale_name}")
