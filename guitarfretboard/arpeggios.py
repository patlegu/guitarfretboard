"""
Predefined arpeggio intervals for guitarfretboard.
"""

ARPEGGIOS = {
    # Triads
    "Major": ["1", "3", "5"],
    "Minor": ["1", "m3", "5"],
    "Diminished": ["1", "m3", "d5"],
    "Augmented": ["1", "3", "A5"],
    
    # 7ths
    "Major 7": ["1", "3", "5", "7"],
    "Minor 7": ["1", "m3", "5", "m7"],
    "Dominant 7": ["1", "3", "5", "m7"],
    "Half-Diminished 7 (m7b5)": ["1", "m3", "d5", "m7"],
    "Diminished 7": ["1", "m3", "d5", "d7"],
    "Minor Major 7": ["1", "m3", "5", "7"],
    "Augmented Major 7": ["1", "3", "A5", "7"],
    
    # 6ths
    "Major 6": ["1", "3", "5", "6"],
    "Minor 6": ["1", "m3", "5", "6"],
    
    # Extended (9ths, 11ths, 13ths - simplified representations for fretboard plotting)
    "Major 9": ["1", "3", "5", "7", "9"],
    "Minor 9": ["1", "m3", "5", "m7", "9"],
    "Dominant 9": ["1", "3", "5", "m7", "9"],
    "Dominant 7b9": ["1", "3", "5", "m7", "m9"],
    "Dominant 7#9": ["1", "3", "5", "m7", "A9"],
}

def get_arpeggio_intervals(arpeggio_name: str) -> list:
    """Returns the list of intervals for a given arpeggio name."""
    if arpeggio_name in ARPEGGIOS:
        return ARPEGGIOS[arpeggio_name]
    raise ValueError(f"Unknown arpeggio: {arpeggio_name}")
