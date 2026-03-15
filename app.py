import streamlit as st
import os
import sys
import base64

# The package 'guitarfretboard' should be available in the same directory
from guitarfretboard import Fretboard, render_svg, parse_pitch, get_scale_intervals, CHORD_SHAPES
from guitarfretboard.core import TUNINGS_GUITAR, TUNINGS_BASS, TUNINGS_UKULELE

st.set_page_config(page_title="Guitar Fretboard Generator", layout="wide")

# The package 'guitarfretboard' should be available in the same directory
import streamlit.components.v1 as components

def main():
    st.title("🎸 Guitar Fretboard SVG Generator")
    st.markdown("Create beautiful chord and scale diagrams instantly.")

    with st.sidebar:
        st.header("Settings")
        
        mode = st.radio("Mode", ["Scale", "Arpeggio", "Chord"])
        
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
            
        from guitarfretboard.themes import THEMES
        theme = st.selectbox("Visual Theme", list(THEMES.keys()))
            
        title = st.text_input("Diagram Title", value="")
        show_tuning = st.checkbox("Show Tuning Names", value=True)
        show_fret_numbers = st.checkbox("Show Fret Numbers", value=True)

    # Main area
    if mode in ["Scale", "Arpeggio"]:
        c1, c2, c3 = st.columns(3)
        with c1:
            root = st.selectbox("Root Note", ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"])
        with c2:
            if mode == "Scale":
                from guitarfretboard.scales import SCALES
                pattern_name = st.selectbox("Scale Type", list(SCALES.keys()))
            else:
                from guitarfretboard.arpeggios import ARPEGGIOS
                pattern_name = st.selectbox("Arpeggio Type", list(ARPEGGIOS.keys()))
                
        with c3:
            caged_form = st.selectbox("CAGED Form (filter)", ["None", "C", "A", "G", "E", "D"])
            highlight_caged = False
            if caged_form != "None":
                highlight_caged = st.checkbox("Highlight box only (don't crop)", value=False)
            else:
                caged_form = None # Pass None to backend
            
        fb = Fretboard(
            frets_max=frets,
            chord=is_vertical,
            left_handed=is_left,
            title=title if title else f"{root} {pattern_name}",
            tuning=tuning,
            show_tuning=show_tuning,
            fret_numbers=show_fret_numbers,
            theme=theme
        )
        
        root_pitch = parse_pitch(root)
        if mode == "Scale":
            from guitarfretboard.scales import get_scale_intervals
            intervals = get_scale_intervals(pattern_name)
        else:
            from guitarfretboard.arpeggios import get_arpeggio_intervals
            intervals = get_arpeggio_intervals(pattern_name)
        
        from guitarfretboard.notes import parse_interval
        for interval in intervals:
            semitones = parse_interval(interval)
            pitch = (root_pitch + semitones) % 12
            style = "5" if semitones == 0 else "2"
            fb.add_note(pitch, style=style, 
                        caged_form=caged_form, 
                        highlight_caged_only=highlight_caged, 
                        root_pitch_caged=root_pitch)
            
    else:  # Chord mode
        st.info("Select a predefined chord shape or add notes manually.")
        chord_cats = list(CHORD_SHAPES.keys()) + ["Custom"]
        chord_type = st.selectbox("Chord Category", chord_cats)
        
        if chord_type == "Custom":
            st.write("Define frets for each string (use -1 for muted/unplayed string):")
            cols = st.columns(len(tuning))
            fingering = {}
            # Strings are 1-indexed, with 1 being the highest pitch (bottom visually in horizontal, right in vertical)
            # We want to display them in a logical order, usually low to high (e.g., 6 to 1) for standard tuning
            for i in range(len(tuning)):
                string_num = len(tuning) - i
                with cols[i]:
                    fret_val = st.number_input(f"Str {string_num}", min_value=-1, max_value=frets, value=-1, step=1)
                    if fret_val != -1:
                        fingering[string_num] = fret_val
            
            base_fret = 0
            subtype = "custom"
        else:
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
            fret_numbers=show_fret_numbers,
            theme=theme
        )
        fb.add_chord(fingering, base_fret=base_fret, style="normal")
        
        # Display identified name
        identified = fb.identify_chord()
        st.success(f"Identified as: **{identified}**")

    # Final rendering
    output_file = "preview.svg"
    render_svg(fb, output_file)
    
    st.markdown("### Preview")
    with open(output_file, "r") as f:
        svg_content = f.read()
    
    # Tooltips need an iframe (components.html) to execute JS securely in Streamlit
    preview_height = 500 if is_vertical else 350
    # Wrap in a div to ensure center alignment, no cutoffs, and a white background so transparent SVGs are visible
    html_str = f"""
    <div style="display: flex; justify-content: center; padding: 20px; background-color: white; border-radius: 8px;">
        {svg_content}
    </div>
    """
    components.html(html_str, height=preview_height, scrolling=True)
    
    import tempfile
    
    st.markdown("### Export")
    export_fmt = st.radio("Download Format", ["svg", "png", "pdf"], horizontal=True)
    
    with tempfile.NamedTemporaryFile(suffix=f".{export_fmt}", delete=False) as tmp:
        tmp_path = tmp.name
        
    fb.export(tmp_path)
    
    with open(tmp_path, "rb") as f:
        file_bytes = f.read()
        
    mime_type = "image/svg+xml" if export_fmt == "svg" else f"image/{export_fmt}"
    if export_fmt == "pdf":
        mime_type = "application/pdf"
        
    st.download_button(
        label=f"Download {export_fmt.upper()}",
        data=file_bytes,
        file_name=f"fretboard.{export_fmt}",
        mime=mime_type
    )
        
    os.remove(tmp_path)

if __name__ == "__main__":
    main()
