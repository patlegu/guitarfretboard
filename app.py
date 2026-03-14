import streamlit as st
import os
import sys
import base64

# The package 'guitarfretboard' should be available in the same directory
from guitarfretboard import Fretboard, render_svg, parse_pitch, get_scale_intervals, CHORD_SHAPES
from guitarfretboard.core import TUNINGS_GUITAR, TUNINGS_BASS, TUNINGS_UKULELE

st.set_page_config(page_title="Guitar Fretboard Generator", layout="wide")

def render_svg_to_html(filename):
    with open(filename, "r") as f:
        svg = f.read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="100%"/>'

def main():
    st.title("🎸 Guitar Fretboard SVG Generator")
    st.markdown("Create beautiful chord and scale diagrams instantly.")

    with st.sidebar:
        st.header("Settings")
        
        mode = st.radio("Mode", ["Scale", "Chord"])
        
        instrument = st.selectbox("Instrument", ["Guitar", "Bass", "Ukulele"])
        if instrument == "Guitar":
            tuning_name = st.selectbox("Tuning", list(TUNINGS_GUITAR.keys()))
            tuning = TUNINGS_GUITAR[tuning_name]
        elif instrument == "Bass":
            tuning_name = st.selectbox("Tuning", list(TUNINGS_BASS.keys()))
            tuning = TUNINGS_BASS[tuning_name]
        else:
            tuning_name = st.selectbox("Tuning", list(TUNINGS_UKULELE.keys()))
            tuning = TUNINGS_UKULELE[tuning_name]
            
        frets = st.slider("Number of frets", 0, 24, 5)
        
        col1, col2 = st.columns(2)
        with col1:
            is_vertical = st.checkbox("Vertical (Chord mode)", value=(mode=="Chord"))
        with col2:
            is_left = st.checkbox("Left-handed")
            
        title = st.text_input("Diagram Title", value="")
        show_tuning = st.checkbox("Show Tuning Names", value=True)
        show_fret_numbers = st.checkbox("Show Fret Numbers", value=True)

    # Main area
    if mode == "Scale":
        c1, c2 = st.columns(2)
        with c1:
            root = st.selectbox("Root Note", ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"])
        with c2:
            from guitarfretboard.scales import SCALES
            scale_name = st.selectbox("Scale Type", list(SCALES.keys()))
            
        fb = Fretboard(
            frets_max=frets,
            chord=is_vertical,
            left_handed=is_left,
            title=title if title else f"{root} {scale_name}",
            tuning=tuning,
            show_tuning=show_tuning,
            fret_numbers=show_fret_numbers
        )
        
        root_pitch = parse_pitch(root)
        intervals = get_scale_intervals(scale_name)
        
        from guitarfretboard.notes import parse_interval
        for interval in intervals:
            semitones = parse_interval(interval)
            pitch = (root_pitch + semitones) % 12
            style = "5" if semitones == 0 else "2"
            fb.add_note(pitch, style=style)
            
    else:  # Chord mode
        st.info("Select a predefined chord shape or add notes manually.")
        chord_type = st.selectbox("Chord Category", list(CHORD_SHAPES.keys()))
        subtype = st.selectbox("Shape Type", list(CHORD_SHAPES[chord_type].keys()))
        
        if subtype == "open":
            specific = st.selectbox("Specific Open Chord", list(CHORD_SHAPES[chord_type]["open"].keys()))
            fingering = CHORD_SHAPES[chord_type]["open"][specific]
            base_fret = 0
        else:
            base_fret = st.number_input("Barre Fret (Base)", 0, 12, 0)
            fingering = CHORD_SHAPES[chord_type][subtype]

        fb = Fretboard(
            frets_max=max(frets, base_fret + 4),
            chord=is_vertical,
            left_handed=is_left,
            title=title if title else f"{chord_type} ({subtype})",
            tuning=tuning,
            show_tuning=show_tuning,
            fret_numbers=show_fret_numbers
        )
        fb.add_chord(fingering, base_fret=base_fret, style="5")
        
        # Display identified name
        identified = fb.identify_chord()
        st.success(f"Identified as: **{identified}**")

    # Final rendering
    output_file = "preview.svg"
    render_svg(fb, output_file)
    
    st.markdown("### Preview")
    st.write(render_svg_to_html(output_file), unsafe_allow_html=True)
    
    with open(output_file, "rb") as f:
        st.download_button("Download SVG", f, "fretboard.svg", "image/svg+xml")

if __name__ == "__main__":
    main()
