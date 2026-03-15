"""
Visual themes and color palettes for guitarfretboard.
"""

# Default colors ported from guitar-fretboard.colors.sty
DEFAULT_COLORS = {
    "background": "none",
    "fretboard": "#F5D0A9",  # Wood-like color, used if background fill is desired
    "nut": "black",
    "frets": "black",
    "strings": "black",
    "text": "black",
    "note_text_dark": "white",
    "note_text_light": "black",
    
    # Note styles mapping
    "styles": {
        "normal": {"fill": "black", "text": "white"},
        "root": {"fill": "#cc0000", "text": "white"}, 
        # Match latex colors
        "1": {"fill": "black", "text": "white"},
        "2": {"fill": "#A020F0", "text": "white"}, # Purple
        "3": {"fill": "#0000FF", "text": "white"}, # Blue
        "4": {"fill": "#00FF00", "text": "black"}, # Green
        "5": {"fill": "#FFD700", "text": "black"}, # Yellow
        "6": {"fill": "#FFA500", "text": "black"}, # Orange
        "7": {"fill": "#FF0000", "text": "white"}, # Red
        "white": {"fill": "white", "text": "black"},
        "gray": {"fill": "gray", "text": "white"},
    }
}

DARK_MODE = {
    "background": "#1E1E1E",
    "fretboard": "#2D2D2D",
    "nut": "#FFFFFF",
    "frets": "#888888",
    "strings": "#AAAAAA",
    "text": "#E0E0E0",
    "note_text_dark": "white",
    "note_text_light": "black",
    
    "styles": {
        "normal": {"fill": "#444444", "text": "white"},
        "root": {"fill": "#FF5555", "text": "white"},
        "1": {"fill": "#444444", "text": "white"},
        "2": {"fill": "#BB86FC", "text": "white"}, # Lighter purple
        "3": {"fill": "#64B5F6", "text": "black"}, # Lighter blue
        "4": {"fill": "#81C784", "text": "black"}, # Lighter green
        "5": {"fill": "#FFF176", "text": "black"}, # Lighter yellow
        "6": {"fill": "#FFB74D", "text": "black"}, # Lighter orange
        "7": {"fill": "#E57373", "text": "black"}, # Lighter red
        "white": {"fill": "#E0E0E0", "text": "black"},
        "gray": {"fill": "#666666", "text": "white"},
    }
}

VINTAGE = {
    "background": "#FDF6E3", # Solarized light background
    "fretboard": "#D2B48C",  # Tan / Wood
    "nut": "#5C4033",        # Dark brown
    "frets": "#8B4513",      # Saddle brown
    "strings": "#A0522D",    # Sienna
    "text": "#3E2723",       # Very dark brown
    "note_text_dark": "#FDF6E3",
    "note_text_light": "#3E2723",
    
    "styles": {
        "normal": {"fill": "#5C4033", "text": "#FDF6E3"},
        "root": {"fill": "#8B0000", "text": "#FDF6E3"}, # Dark red
        "1": {"fill": "#5C4033", "text": "#FDF6E3"},
        "2": {"fill": "#4B0082", "text": "#FDF6E3"}, # Indigo
        "3": {"fill": "#000080", "text": "#FDF6E3"}, # Navy
        "4": {"fill": "#006400", "text": "#FDF6E3"}, # Dark green
        "5": {"fill": "#DAA520", "text": "#3E2723"}, # Goldenrod
        "6": {"fill": "#D2691E", "text": "#3E2723"}, # Chocolate
        "7": {"fill": "#A52A2A", "text": "#FDF6E3"}, # Brown
        "white": {"fill": "#FFF8DC", "text": "#3E2723"}, # Cornsilk
        "gray": {"fill": "#808080", "text": "#FDF6E3"},
    }
}

MINIMALIST = {
    "background": "white",
    "fretboard": "none",
    "nut": "black",
    "frets": "#DDDDDD",
    "strings": "black",
    "text": "black",
    "note_text_dark": "white",
    "note_text_light": "black",
    
    "styles": {
        "normal": {"fill": "white", "text": "black", "stroke": "black"},
        "root": {"fill": "black", "text": "white", "stroke": "black"},
        "1": {"fill": "white", "text": "black", "stroke": "black"},
        "2": {"fill": "white", "text": "black", "stroke": "black"},
        "3": {"fill": "white", "text": "black", "stroke": "black"},
        "4": {"fill": "white", "text": "black", "stroke": "black"},
        "5": {"fill": "white", "text": "black", "stroke": "black"},
        "6": {"fill": "white", "text": "black", "stroke": "black"},
        "7": {"fill": "white", "text": "black", "stroke": "black"},
        "white": {"fill": "white", "text": "black", "stroke": "black"},
        "gray": {"fill": "#EEEEEE", "text": "gray", "stroke": "gray"},
    }
}

THEMES = {
    "default": DEFAULT_COLORS,
    "dark": DARK_MODE,
    "vintage": VINTAGE,
    "minimalist": MINIMALIST
}

# Mapping for note-specific coloring
NOTE_COLORS = {
    "A": "#FF4136", # Rouge
    "B": "#FF851B", # Orange
    "C": "#FFDC00", # Jaune
    "D": "#2ECC40", # Vert
    "E": "#0074D9", # Bleu
    "F": "#B10DC9", # Violet
    "G": "#F012BE"  # Rose (Magenta-ish)
}
