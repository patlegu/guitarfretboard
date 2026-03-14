import os
from guitarfretboard import Fretboard, render_svg, CHORD_SHAPES

def demo_chord_detection_and_dictionary():
    print("Generating: chord_detection_demo.svg")
    
    # 1. Using the dictionary to add a chord
    fb = Fretboard(
        frets_min=0, frets_max=4, 
        chord=True, # Vertical
        fret_numbers=True,
    )
    
    # Add a C Major Open Chord from our dictionary
    c_major_fingering = CHORD_SHAPES["major"]["open"]["C"]
    fb.add_chord(c_major_fingering, base_fret=0, style="5")
    
    # 2. Automated identification
    chord_name = fb.identify_chord()
    fb.title = f"Detected: {chord_name}"
    
    render_svg(fb, "chord_detection_demo.svg")
    print(f"Chord identified: {chord_name}")

def demo_barre_chords():
    print("Generating: barre_chord_demo.svg")
    
    # B Minor Barre Chord (A minor shape at 2nd fret)
    fb = Fretboard(
        frets_min=0, frets_max=5, 
        chord=True,
        fret_numbers=True,
    )
    
    # A minor barre shape
    am_shape = CHORD_SHAPES["minor"]["barre_a"]
    fb.add_chord(am_shape, base_fret=2, style="2")
    
    # Automated identification
    chord_name = fb.identify_chord()
    fb.title = f"Identified Barre: {chord_name}"
    
    render_svg(fb, "barre_chord_demo.svg")
    print(f"Chord identified: {chord_name}")

if __name__ == "__main__":
    demo_chord_detection_and_dictionary()
    demo_barre_chords()
    print("Done! Musical intelligence demo files generated.")
