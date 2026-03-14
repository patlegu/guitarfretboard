from typing import List
"""
Notes, intervals and pitch definitions for guitarfretboard.
Ported from guitar-fretboard.notes.sty.
"""

NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]

# Mapping notes to their semitone value from C
# We include standard accidentals as well as some enharmonics.
PITCHES = {
    "C": 0, "C#": 1, "Db": 1, 
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "Fb": 4, "E#": 5,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11, "Cb": 11, "B#": 0
}

# Intervals mapping to their semitone distance from the root note
INTERVALS = {
    # Unison
    "1": 0, "d1": -1, "A1": 1,
    # Second
    "m2": 1, "2": 2, "d2": 0, "A2": 3,
    # Third
    "m3": 3, "3": 4, "d3": 2, "A3": 5,
    # Fourth
    "4": 5, "d4": 4, "A4": 6,
    # Fifth
    "5": 7, "d5": 6, "A5": 8,
    # Sixth
    "m6": 8, "6": 9, "d6": 7, "A6": 10,
    # Seventh
    "m7": 10, "7": 11, "d7": 9, "A7": 12,
    # Extended intervals
    "8": 12,
    "m9": 13, "9": 14,
    "11": 17,
    "m13": 20, "13": 21,
    
    # Aliases
    "b2": 1, "bb2": 0, "S2": 3,
    "b3": 3, "bb3": 2, "S3": 5,
    "b4": 4, "S4": 6,
    "b5": 6, "S5": 8,
    "b6": 8, "bb6": 7, "S6": 10,
    "b7": 10, "bb7": 9, "S7": 12,
}

def parse_pitch(pitch_str: str) -> int:
    """Returns the semitone value format of a pitch string, e.g. 'C' -> 0, 'F#' -> 6"""
    # Normalize some common typography for sharp/flat if necessary
    pitch_str = pitch_str.replace('♯', '#').replace('♭', 'b')
    if pitch_str in PITCHES:
        return PITCHES[pitch_str]
    raise ValueError(f"Unknown pitch: {pitch_str}")

def get_pitch_name(semitones: int) -> str:
    """Gets a standard note name for a semitone value (0-11)."""
    return NOTE_NAMES[semitones % 12]

def parse_interval(interval_str: str) -> int:
    """Returns the semitone value of an interval string."""
    if interval_str in INTERVALS:
        return INTERVALS[interval_str]
    raise ValueError(f"Unknown interval: {interval_str}")

# Common chord interval patterns (using semitone distances from root)
CHORD_PATTERNS = {
    (0, 4, 7): "Major",
    (0, 3, 7): "minor",
    (0, 4, 7, 10): "7",
    (0, 4, 7, 11): "Major 7",
    (0, 3, 7, 10): "minor 7",
    (0, 3, 7, 11): "minor Major 7",
    (0, 4, 8): "Augmented",
    (0, 3, 6): "Diminished",
    (0, 3, 6, 9): "Diminished 7",
    (0, 3, 6, 10): "m7b5",
    (0, 2, 7): "Sus2",
    (0, 5, 7): "Sus4",
    (0, 7): "5 (Power Chord)",
    (0, 4, 7, 9): "6",
    (0, 3, 7, 9): "m6",
}

def identify_chord_type(semitones: List[int]) -> str:
    """
    Given a list of absolute semitones, identifies the chord type.
    """
    if not semitones:
        return ""
    
    # Identify unique tones and the lowest physical note
    lowest_note = min(semitones)
    root_candidate = lowest_note % 12
    
    unique_tones = sorted(list(set([t % 12 for t in semitones])))
    
    # Try the lowest note as root first
    def check_pattern(root):
        pattern = tuple(sorted([(t - root) % 12 for t in unique_tones]))
        if pattern in CHORD_PATTERNS:
            return f"{get_pitch_name(root)} {CHORD_PATTERNS[pattern]}"
        return None

    # 1. Try lowest note
    result = check_pattern(root_candidate)
    if result:
        return result
        
    # 2. Try all other notes as roots (for inversions)
    for t in unique_tones:
        if t == root_candidate:
            continue
        result = check_pattern(t)
        if result:
            return f"{result} (Inversion)"

    return "Unknown Chord"

def transpose(pitch: int, interval_semitones: int) -> int:
    return (pitch + interval_semitones) % 12
