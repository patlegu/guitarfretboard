"""
Definitions of musical scales.
Ported from guitar-fretboard.scales.sty.
"""

# Map scale aliases to intervals list
SCALES = {
    "5": ["1", "5"],
    "b5": ["1", "b5"],
    "S5": ["1", "S5"],
    "M": ["1", "3", "5"],
    "m": ["1", "b3", "5"],
    "sus2": ["1", "2", "5"],
    "sus4": ["1", "4", "5"],
    "aug": ["1", "3", "S5"],
    "dim": ["1", "3", "b5"],
    "7": ["1", "3", "5", "b7"],
    "M7": ["1", "3", "5", "7"],
    "m7": ["1", "b3", "5", "b7"],
    "7sus4": ["1", "4", "5", "b7"],
    "m7maj": ["1", "b3", "5", "7"],
    "7majS5": ["1", "3", "S5", "7"],
    "7S5": ["1", "3", "S5", "b7"],
    "7b5": ["1", "3", "b5", "b7"],
    "m7b5": ["1", "b3", "b5", "b7"],
    "dim7": ["1", "b3", "b5", "bb7"],
    "6": ["1", "3", "5", "6"],
    "m6": ["1", "b3", "5", "6"],
    "add9": ["1", "3", "5", "9"],
    "6add9": ["1", "3", "5", "6", "9"],
    "maj9": ["1", "3", "5", "7", "9"],
    "maj7S11": ["1", "3", "5", "7", "S11"],
    "maj13": ["1", "3", "5", "7", "9", "13"],
}

def get_scale_intervals(scale_name: str) -> list[str]:
    """Return the list of intervals (strings) for a given scale."""
    if scale_name in SCALES:
        return SCALES[scale_name]
    raise ValueError(f"Unknown scale: {scale_name}")
