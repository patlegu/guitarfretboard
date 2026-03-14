"""
Chord dictionary and fingering definitions for guitarfretboard.
"""
from typing import Dict, List, Optional

# Define chord shapes as (string, fret) pairs
# We use relative frets where 0 is the root or base fret of the shape.
# Strings are 1-indexed (1=high E, 6=low E for standard guitar).
CHORD_SHAPES = {
    "major": {
        "open": {
            "C": {6: 'x', 5: 3, 4: 2, 3: 0, 2: 1, 1: 0},
            "A": {6: 'x', 5: 0, 4: 2, 3: 2, 2: 2, 1: 0},
            "G": {6: 3, 5: 2, 4: 0, 3: 0, 2: 0, 1: 3},
            "E": {6: 0, 5: 2, 4: 2, 3: 1, 2: 0, 1: 0},
            "D": {6: 'x', 5: 'x', 4: 0, 3: 2, 2: 3, 1: 2},
        },
        "barre_e": {6: 0, 5: 2, 4: 2, 3: 1, 2: 0, 1: 0}, # Root on 6th string
        "barre_a": {6: 'x', 5: 0, 4: 2, 3: 2, 2: 2, 1: 0}, # Root on 5th string
    },
    "minor": {
        "open": {
            "Am": {6: 'x', 5: 0, 4: 2, 3: 2, 2: 1, 1: 0},
            "Em": {6: 0, 5: 2, 4: 2, 3: 0, 2: 0, 1: 0},
            "Dm": {6: 'x', 5: 'x', 4: 0, 3: 2, 2: 3, 1: 1},
        },
        "barre_e": {6: 0, 5: 2, 4: 2, 3: 0, 2: 0, 1: 0},
        "barre_a": {6: 'x', 5: 0, 4: 2, 3: 2, 2: 1, 1: 0},
    },
    "7": {
        "open": {
            "C7": {6: 'x', 5: 3, 4: 2, 3: 3, 2: 1, 1: 'x'},
            "A7": {6: 'x', 5: 0, 4: 2, 3: 0, 2: 2, 1: 0},
            "G7": {6: 3, 5: 2, 4: 0, 3: 0, 2: 0, 1: 1},
            "E7": {6: 0, 5: 2, 4: 0, 3: 1, 2: 0, 1: 0},
            "D7": {6: 'x', 5: 'x', 4: 0, 3: 2, 2: 1, 1: 2},
        },
        "barre_e": {6: 0, 5: 2, 4: 0, 3: 1, 2: 0, 1: 0},
        "barre_a": {6: 'x', 5: 0, 4: 2, 3: 0, 2: 2, 1: 0},
    }
}

class Chord:
    def __init__(self, name: str, fingering: Dict[int, Optional[int]]):
        self.name = name
        self.fingering = fingering # {string_idx: fret_num or 'x' or 0}

def get_chord(chord_type: str, root_pitch: int, shape_type: str = "barre_e") -> Optional[Chord]:
    """
    Returns a Chord object with absolute frets calculated for a given root.
    """
    # Simply mapping barre shapes for now
    if chord_type in CHORD_SHAPES:
        if shape_type in CHORD_SHAPES[chord_type]:
            shape = CHORD_SHAPES[chord_type][shape_type]
            
            # For barre_e, root is on string 6
            # For barre_a, root is on string 5
            root_string = 6 if shape_type == "barre_e" else 5
            
            # Example: G is 3 semitones from E on string 6.
            # We need to know the string tuning to find the base fret.
            # Since this depends on Fretboard instance tuning, we might just return the shape
            # and let Fretboard.add_chord handle the math.
            return Chord(f"{chord_type} shape", shape)
    return None
