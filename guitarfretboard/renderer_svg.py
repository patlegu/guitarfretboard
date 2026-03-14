"""
A pure Python SVG generation engine for guitarfretboard.
Replicates the visual style of guitar-fretboard.sty (TikZ).
Now with full parity: Chord mode, Left-handed, Split notes, Styles, and Legends.
"""

from typing import List
from .core import Fretboard
from .notes import get_pitch_name

from .themes import THEMES


def render_svg(fretboard: Fretboard, filename: str):
    """
    Renders the Fretboard object into an SVG file.
    Supports Chord mode, Left-handed mode, split notes, and legends.
    """
    # SVG Constants
    FRET_WIDTH = 50
    STRING_HEIGHT = 40 if fretboard.chord else 30
    MARGIN_TOP = 60
    MARGIN_BOTTOM = 40
    MARGIN_LEFT = 60
    MARGIN_RIGHT = 40
    
    # Calculate boundaries
    num_frets_drawn = fretboard.canvas_x_max - fretboard.canvas_x_min + 1
    
    total_fret_length = (num_frets_drawn - 1) * FRET_WIDTH
    total_string_height = (fretboard.num_strings - 1) * STRING_HEIGHT
    
    # Base dimensions (Horizontal)
    width = total_fret_length + MARGIN_LEFT + MARGIN_RIGHT
    height = total_string_height + MARGIN_TOP + MARGIN_BOTTOM
    
    # Add space for legend
    legend_height = len(fretboard.legend) * 20 + (20 if fretboard.legend else 0)
    
    # Final dimensions based on orientation
    final_width = height if fretboard.chord else width
    final_height = (width + legend_height) if fretboard.chord else (height + legend_height)

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{final_width}" height="{final_height}" viewBox="0 0 {final_width} {final_height}">')
    theme = THEMES.get(fretboard.theme, THEMES["default"])
    
    lines.append(f'  <style>')
    lines.append(f'    .background {{ fill: {theme["background"]}; }}')
    if theme["fretboard"] != "none":
        lines.append(f'    .fretboard-board {{ fill: {theme["fretboard"]}; }}')
    lines.append(f'    .fret {{ stroke: {theme["frets"]}; stroke-width: 2px; }}')
    lines.append(f'    .string {{ stroke: {theme["strings"]}; }}')
    lines.append(f'    .nut {{ stroke: {theme["nut"]}; stroke-width: 5px; }}')
    lines.append(f'    .fret-text {{ font-family: sans-serif; font-size: 14px; fill: {theme["text"]}; text-anchor: middle; font-weight: bold; }}')
    lines.append(f'    .tuning-text {{ font-family: sans-serif; font-weight: bold; fill: {theme["text"]}; font-size: 16px; text-anchor: middle; alignment-baseline: middle; }}')
    lines.append(f'    .note-circle {{ stroke: {theme.get("note_stroke", "black")}; stroke-width: 1px; }}')
    lines.append(f'    .note-text {{ font-family: sans-serif; font-weight: bold; font-size: 14px; text-anchor: middle; alignment-baseline: central; }}')
    lines.append(f'    .note-text-small {{ font-family: sans-serif; font-weight: bold; font-size: 10px; text-anchor: middle; alignment-baseline: central; }}')
    lines.append(f'    .title-text {{ font-family: sans-serif; font-size: 24px; fill: {theme["text"]}; text-anchor: middle; font-weight: bold; }}')
    lines.append(f'    .legend-text {{ font-family: sans-serif; font-size: 14px; fill: {theme["text"]}; text-anchor: start; }}')
    lines.append(f'    .split-line {{ stroke: {theme.get("note_stroke", "black")}; stroke-width: 1px; }}')
    lines.append(f'  </style>')
    
    lines.append(f'  <rect width="100%" height="100%" class="background"/>')
    if theme["fretboard"] != "none":
        # Draw wooden/colored background for the fretboard itself
        fx, fy = MARGIN_LEFT, MARGIN_TOP
        fw, fh = total_fret_length, total_string_height
        if fretboard.chord:
             lines.append(f'  <rect x="{fy}" y="{MARGIN_RIGHT}" width="{fh}" height="{fw}" class="fretboard-board"/>')
        else:
             lines.append(f'  <rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" class="fretboard-board"/>')
             
    # Tooltip Container (Hidden by default)
    lines.append('  <g id="tooltip" visibility="hidden">')
    lines.append('    <rect width="60" height="25" fill="black" opacity="0.8" rx="5" ry="5"/>')
    lines.append('    <text x="30" y="17" fill="white" font-family="sans-serif" font-size="12px" text-anchor="middle" font-weight="bold">Note</text>')
    lines.append('  </g>')


    # Coordinate transformation helper
    def get_coords(fret_pos, string_idx):
        # Convert relative fret to x
        rel_fret = fret_pos - fretboard.canvas_x_min
        
        # Left-handed flip
        if fretboard.left_handed:
            rel_fret = (num_frets_drawn - 1) - rel_fret
            
        x = MARGIN_LEFT + rel_fret * FRET_WIDTH
        y = MARGIN_TOP + (string_idx - 1) * STRING_HEIGHT
        
        if fretboard.chord:
            # Chord mode: Rotate 90 degrees
            # (x, y) -> (y, width - x)
            return y, width - x + (MARGIN_LEFT - MARGIN_RIGHT) # Correction for margins
        return x, y

    # Draw Title
    title_x = final_width / 2
    title_y = 30
    if fretboard.title:
        lines.append(f'  <text x="{title_x}" y="{title_y}" class="title-text">{fretboard.title}</text>')
        
    # Draw Frets
    for i in range(fretboard.canvas_x_min, fretboard.canvas_x_max + 1):
        x1, y1 = get_coords(i, 1)
        x2, y2 = get_coords(i, fretboard.num_strings)
        
        fret_class = "nut" if i == 0 else "fret"
        lines.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{fret_class}"/>')
        
        # Fret Numbers
        if fretboard.fret_numbers and i > fretboard.canvas_x_min:
            nx, ny = get_coords(i - 0.5, fretboard.num_strings)
            offset = 20 if not fretboard.chord else 25
            if fretboard.chord:
                lines.append(f'  <text x="{nx + offset}" y="{ny}" class="fret-text">{i}</text>')
            else:
                lines.append(f'  <text x="{nx}" y="{ny + offset}" class="fret-text">{i}</text>')

    # Draw Strings
    for s_idx in range(1, fretboard.num_strings + 1):
        x1, y1 = get_coords(fretboard.canvas_x_min, s_idx)
        x2, y2 = get_coords(fretboard.canvas_x_max, s_idx)
        
        thickness = 1.0 + (s_idx - 1) * 0.5
        lines.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="string" style="stroke-width: {thickness}px;"/>')
        
        # Draw Tuning
        if fretboard.show_tuning:
            # Position tuning at the "headstock" end
            tx, ty = get_coords(fretboard.canvas_x_min, s_idx)
            pitch_str = get_pitch_name(fretboard.get_string_base_pitch(s_idx))
            
            if fretboard.chord:
                lines.append(f'  <text x="{tx}" y="{ty + 25}" class="tuning-text">{pitch_str}</text>')
            else:
                lines.append(f'  <text x="{tx - 25}" y="{ty}" class="tuning-text">{pitch_str}</text>')

    # Draw Notes
    for note in fretboard.notes:
        fret = note["fret"]
        string = note["string"]
        label = note["label"]
        split_label = note["split_label"]
        highlight = note["highlight"]
        shade = note["shade"]
        style = note["style"]
        
        # Open notes (fret 0) are placed slightly before the nut
        pos_fret = fret if fret > 0 else -0.3
        if fret == 0:
            nx, ny = get_coords(-0.4, string)
        else:
            nx, ny = get_coords(fret - 0.5, string)
            
        color_def = theme["styles"].get(style, theme["styles"]["normal"])
        bg = color_def["fill"]
        fg = color_def["text"]
        stroke = color_def.get("stroke", "black")
        
        opacity = 0.3 if shade else 1.0
        stroke_width = 4 if highlight else 1
        
        # Interactive js calls
        tooltip_label = split_label if split_label else label
        js_events = f'onmousemove="showTooltip(event, \'{tooltip_label}\')" onmouseout="hideTooltip()"'
        
        # Draw the circle
        lines.append(f'  <circle cx="{nx}" cy="{ny}" r="14" fill="{bg}" opacity="{opacity}" stroke="{stroke}" stroke-width="{stroke_width}" {js_events} style="cursor: pointer;"/>')
        
        if split_label:
            # Draw split line
            lines.append(f'  <line x1="{nx-14}" y1="{ny}" x2="{nx+14}" y2="{ny}" stroke="{stroke}" stroke-width="1px" opacity="{opacity}" pointer-events="none"/>')
            # Top label
            lines.append(f'  <text x="{nx}" y="{ny-6}" fill="{fg}" opacity="{opacity}" class="note-text-small" pointer-events="none">{label}</text>')
            # Bottom label
            lines.append(f'  <text x="{nx}" y="{ny+8}" fill="{fg}" opacity="{opacity}" class="note-text-small" pointer-events="none">{split_label}</text>')
        else:
            lines.append(f'  <text x="{nx}" y="{ny}" fill="{fg}" opacity="{opacity}" class="note-text" pointer-events="none">{label}</text>')



    # Draw Legend
    if fretboard.legend:
        lx = 20
        ly = (width if fretboard.chord else height) + 10
        lines.append(f'  <text x="{lx}" y="{ly}" class="legend-text">Legend:</text>')
        for idx, item in enumerate(fretboard.legend):
            lines.append(f'  <text x="{lx + 10}" y="{ly + 20 + idx*20}" class="legend-text">• {item}</text>')

    # Javascript for interactivity
    lines.append('  <script type="text/javascript">')
    lines.append('    <![CDATA[')
    lines.append('      function showTooltip(evt, text) {')
    lines.append('        let tooltip = document.getElementById("tooltip");')
    lines.append('        tooltip.setAttribute("visibility", "visible");')
    lines.append('        let textElement = tooltip.getElementsByTagName("text")[0];')
    lines.append('        textElement.textContent = text;')
    lines.append('        let rectElement = tooltip.getElementsByTagName("rect")[0];')
    lines.append('        let bbox = textElement.getBBox();')
    lines.append('        rectElement.setAttribute("width", bbox.width + 16);')
    lines.append('        textElement.setAttribute("x", (bbox.width + 16) / 2);')
    lines.append('        // Position slightly above and to the right of cursor')
    lines.append('        let svgPt = evt.target.ownerSVGElement.createSVGPoint();')
    lines.append('        svgPt.x = evt.clientX; svgPt.y = evt.clientY;')
    lines.append('        let cursorPt = svgPt.matrixTransform(evt.target.ownerSVGElement.getScreenCTM().inverse());')
    lines.append('        tooltip.setAttribute("transform", "translate(" + (cursorPt.x + 10) + "," + (cursorPt.y - 30) + ")");')
    lines.append('      }')
    lines.append('      function hideTooltip() {')
    lines.append('        document.getElementById("tooltip").setAttribute("visibility", "hidden");')
    lines.append('      }')
    lines.append('    ]]>')
    lines.append('  </script>')
    lines.append('</svg>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
