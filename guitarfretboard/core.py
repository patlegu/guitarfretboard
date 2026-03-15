"""
Core classes for the fretboard representations.
"""
from typing import List, Dict, Optional

# Predefined tunings mappings (Absolute semitones, C0=0)
TUNINGS_GUITAR = {
    "standard": [40, 45, 50, 55, 59, 64][::-1], # E2 A2 D3 G3 B3 E4 -> [64, 59, 55, 50, 45, 40]
    "dadgad": [38, 45, 50, 55, 57, 62][::-1],
    "drop d": [38, 45, 50, 55, 59, 64][::-1],
    "double drop d": [38, 45, 50, 55, 59, 62][::-1],
    "open g": [38, 43, 50, 55, 59, 62][::-1],
    "7 string": [35, 40, 45, 50, 55, 59, 64][::-1], # B1 ...
}

TUNINGS_UKULELE = {
    "standard": [67, 60, 64, 69][::-1], # G4 C4 E4 A4
}

TUNINGS_BASS = {
    "standard": [28, 33, 38, 43][::-1], # E1 A1 D2 G2
    "5 string": [23, 28, 33, 38, 43][::-1], # B0 ...
    "5 string tenor": [28, 33, 38, 43, 48][::-1],
    "6 string": [23, 28, 33, 38, 43, 48][::-1],
}


class Fretboard:
    def __init__(self, 
                 frets_min: int = 0, 
                 frets_max: int = 12,
                 frets_before: int = 0,
                 frets_after: int = 0,
                 tuning: List[int] = None,
                 fret_numbers: bool = False,
                 show_tuning: bool = True,
                 left_handed: bool = False,
                 chord: bool = False,
                 transpose: int = 0,
                 title: str = "",
                 legend: List[str] = None,
                 theme: str = "default",
                 interactive: bool = False,
                 use_note_colors: bool = False):
        self.frets_min = frets_min
        self.frets_max = frets_max
        self.frets_before = frets_before
        self.frets_after = frets_after
        
        # Standard guitar tuning if not provided (E A D G B E)
        if tuning is None:
            self.tuning = TUNINGS_GUITAR["standard"]
        else:
            self.tuning = tuning
            
        self.fret_numbers = fret_numbers
        self.show_tuning = show_tuning
        self.left_handed = left_handed
        self.chord = chord
        self.transpose = transpose
        self.title = title
        self.legend = legend if legend else []
        self.theme = theme
        self.interactive = interactive
        self.use_note_colors = use_note_colors
        
        self.num_strings = len(self.tuning)
        
        # We compute canvas boundaries
        self.canvas_x_min = self.frets_min - self.frets_before
        self.canvas_x_max = self.frets_max + self.frets_after
        
        # Added notes (each note is a dict with properties: 'fret', 'string', 'label', 'style', 'split_label', 'highlight', 'shade')
        self.notes = []

    def get_string_base_pitch(self, string_index: int) -> int:
        """Get the base pitch (semitones from C) of a given string (1-indexed, 1=top string in visual)."""
        # Our tuning list is [string 1, string 2, ..., string N] 
        # (e.g. from High E to Low E)
        return self.tuning[string_index - 1]

    def add_note_at_fret(self, string: int, fret: int, label: str, style: str = "normal", 
                         split_label: str = None, highlight: bool = False, shade: bool = False):
        """Add a note given its exact string and fret"""
        if self.canvas_x_min <= fret <= self.canvas_x_max:
            self.notes.append({
                "string": string,
                "fret": fret,
                "label": label,
                "split_label": split_label,
                "highlight": highlight,
                "shade": shade,
                "style": style
            })

    def get_caged_base_fret(self, form: str, root_pitch: int) -> Optional[int]:
        """Calculates the base fret for a given CAGED form and root note (Standard tuning assumed)."""
        # The CAGED system revolves around these open chord shapes translated up the neck:
        # C shape: Root on A string (5th)
        # A shape: Root on A string (5th)
        # G shape: Root on E string (6th)
        # E shape: Root on E string (6th)
        # D shape: Root on D string (4th)
        
        # Standard tuning baselines
        e_string_pitch = self.tuning[5] # Low E
        a_string_pitch = self.tuning[4] # A
        d_string_pitch = self.tuning[3] # D
        
        def _get_fret(string_pitch):
            semitones = (root_pitch - string_pitch) % 12
            if semitones == 0: semitones = 12 # Prefer higher frets for CAGED boxes if open
            return semitones
            
        if form == 'C':
            # C shape has root on 5th string. Fret range is roughly [root_fret - 3, root_fret]
            root_fret = _get_fret(a_string_pitch)
            return max(0, root_fret - 3)
        elif form == 'A':
            # A shape has root on 5th string. Fret range is [root_fret, root_fret + 2]
            return _get_fret(a_string_pitch)
        elif form == 'G':
            # G shape has root on 6th string. Fret range is [root_fret - 3, root_fret]
            root_fret = _get_fret(e_string_pitch)
            return max(0, root_fret - 3)
        elif form == 'E':
            # E shape has root on 6th string. Fret range [root_fret, root_fret + 2]
            return _get_fret(e_string_pitch)
        elif form == 'D':
            # D shape has root on 4th string. Fret range [root_fret - 1, root_fret + 2]
            root_fret = _get_fret(d_string_pitch)
            return max(0, root_fret - 1)
        return None

    def _is_in_caged_box(self, fret: int, base_fret: int) -> bool:
        """Check if a fret is within a standard 4-5 fret span."""
        # A CAGED box usually spans 4 frets (e.g. frets 5,6,7,8).
        # We allow a stretch of 5 to accommodate modes.
        return base_fret <= fret <= base_fret + 4

    def add_note(self, pitch_semitones: int, label: str = None, string_limit: List[int] = None, 
                 style: str = "normal", split: bool = False, highlight: bool = False, shade: bool = False,
                 caged_form: str = None, highlight_caged_only: bool = False, root_pitch_caged: int = None):
        """
        Calculates fingering on all strings for a given pitch and adds them.
        Can filter or highlight notes based on a specific CAGED form box.
        """
        from .notes import get_pitch_name
        
        actual_label = label if label else get_pitch_name(pitch_semitones)
        
        split_label = None
        if split:
            split_label = actual_label
            
        base_pitch = pitch_semitones + self.transpose
        
        # Calculate CAGED box boundaries if requested
        caged_base = None
        if caged_form and caged_form != "None" and root_pitch_caged is not None:
            caged_base = self.get_caged_base_fret(caged_form.upper(), root_pitch_caged)
            
        strings = string_limit if string_limit else range(1, self.num_strings + 1)
        
        for string in strings:
            string_pitch = self.get_string_base_pitch(string)
            base_semitones_string = base_pitch - string_pitch
            
            for octave in range(-84, 85, 12):
                fret = base_semitones_string + octave
                if self.canvas_x_min <= fret <= self.canvas_x_max:
                    
                    final_style = style
                    final_shade = shade
                    final_highlight = highlight
                    
                    if caged_base is not None:
                        is_in_box = self._is_in_caged_box(fret, caged_base)
                        if highlight_caged_only:
                            # Draw everything, but grey out notes outside the box
                            if not is_in_box:
                                final_shade = True
                            else:
                                final_highlight = True
                        else:
                            # Strict filtering: don't draw if outside box
                            if not is_in_box:
                                continue
                                
                    self.add_note_at_fret(string, fret, actual_label, style=final_style, 
                                         split_label=split_label if split else None,
                                         highlight=final_highlight, shade=final_shade)

    def add_chord(self, fingering: Dict[int, int], base_fret: int = 0, style: str = "normal"):
        """
        Adds a set of notes defined by a fingering dictionary (string: fret).
        Example: {6: 3, 5: 2, 4: 0, 3: 0, 2: 0, 1: 3} for G Major.
        """
        from .notes import get_pitch_name
        for string, fret in fingering.items():
            if fret == 'x':
                continue
            
            # If it's a number (including 0), we apply the base_fret offset.
            # In barre shapes, 0 means the barre fret itself.
            abs_fret = fret + base_fret
            pitch = (self.get_string_base_pitch(string) + abs_fret) % 12
            label = get_pitch_name(pitch)
            self.add_note_at_fret(string, abs_fret, label, style=style)

    def identify_chord(self) -> str:
        """
        Attempts to identify the chord currently shown on the fretboard.
        """
        from .notes import identify_chord_type
        semitones = []
        for note in self.notes:
            string_pitch = self.get_string_base_pitch(note["string"])
            abs_pitch = string_pitch + note["fret"]
            semitones.append(abs_pitch)
        
        return identify_chord_type(semitones)
        
    def export(self, filename: str):
        """
        Exports the fretboard to the specified file format based on extension.
        Supports: .svg, .png, .pdf
        """
        import os
        from .renderer_svg import render_svg
        import tempfile

        ext = os.path.splitext(filename)[1].lower()
        
        if ext == ".svg":
            render_svg(self, filename)
        elif ext in [".png", ".pdf"]:
            try:
                import cairosvg
                with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
                    temp_svg = tmp.name
                
                # First generate SVG
                render_svg(self, temp_svg)
                
                # Then convert based on extension
                if ext == ".png":
                    cairosvg.svg2png(url=temp_svg, write_to=filename)
                elif ext == ".pdf":
                    cairosvg.svg2pdf(url=temp_svg, write_to=filename)
                    
                os.remove(temp_svg)
            except ImportError:
                print("Warning: cairosvg is required for PNG/PDF export. Please install it with 'pip install cairosvg'. Saving as SVG instead.")
                render_svg(self, filename.replace(ext, ".svg"))
        else:
            raise ValueError(f"Unsupported file format: {ext}. Use .svg, .png, or .pdf")
