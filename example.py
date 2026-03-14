import os
from guitarfretboard import Fretboard, render_svg, parse_pitch

def demo_horizontal_scale():
    print("Generating: horizontal_scale.svg")
    fb = Fretboard(
        frets_min=0, frets_max=5, frets_before=0, frets_after=0,
        fret_numbers=True, title="C Major Scale (Horizontal)",
        legend=["Red: Root (C)", "Blue: Other (D, E)"]
    )
    
    # Add C (Root - style 5)
    fb.add_note(parse_pitch("C"), style="5", label="C")
    # Add D, E (Other - style 2)
    fb.add_note(parse_pitch("D"), style="2", label="D")
    fb.add_note(parse_pitch("E"), style="2", label="E")
    
    render_svg(fb, "horizontal_scale.svg")

def demo_vertical_chord():
    print("Generating: vertical_chord.svg")
    # G Major Chord - Vertical orientation
    fb = Fretboard(
        frets_min=0, frets_max=3, 
        chord=True, # VERTICAL MODE
        fret_numbers=True, 
        title="G Major Chord (Vertical)"
    )
    
    # G Major: G(3,3), B(2,0), D(4,0), G(5,0), B(6,0), G(1,3)
    # Using add_note_at_fret(string, fret, label, style)
    # Standard tuning: 6=E, 5=A, 4=D, 3=G, 2=B, 1=E (high)
    fb.add_note_at_fret(6, 3, "G", style="5") # Low G
    fb.add_note_at_fret(5, 2, "B", style="2")
    fb.add_note_at_fret(4, 0, "D", style="2")
    fb.add_note_at_fret(3, 0, "G", style="2")
    fb.add_note_at_fret(2, 0, "B", style="2")
    fb.add_note_at_fret(1, 3, "G", style="2") # High G
    
    render_svg(fb, "vertical_chord.svg")

def demo_left_handed():
    print("Generating: left_handed_scale.svg")
    fb = Fretboard(
        frets_min=0, frets_max=5,
        left_handed=True, # LEFT HANDED MODE
        fret_numbers=True,
        title="A minor (Left-Handed)"
    )
    fb.add_note(parse_pitch("A"), style="5", label="A")
    fb.add_note(parse_pitch("C"), style="2", label="C")
    fb.add_note(parse_pitch("E"), style="2", label="E")
    
    render_svg(fb, "left_handed_scale.svg")

def demo_advanced_styles():
    print("Generating: advanced_styles.svg")
    fb = Fretboard(
        frets_min=0, frets_max=4,
        fret_numbers=True,
        title="Split Notes & Highlights"
    )
    
    # Split note (Note + Interval)
    fb.add_note_at_fret(6, 0, label="E", split_label="1", style="5")
    
    # Highlighted note
    fb.add_note_at_fret(6, 3, label="G", style="2", highlight=True)
    
    # Shaded note
    fb.add_note_at_fret(5, 2, label="B", style="2", shade=True)
    
    render_svg(fb, "advanced_styles.svg")

if __name__ == "__main__":
    demo_horizontal_scale()
    demo_vertical_chord()
    demo_left_handed()
    demo_advanced_styles()
    print("Done! All examples generated in current directory.")
