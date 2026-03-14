"""
guitarfretboard - A pure Python SVG guitar fretboard generator.
"""

from .core import Fretboard
from .renderer_svg import render_svg
from .notes import parse_pitch, parse_interval, identify_chord_type
from .scales import get_scale_intervals
from .chords import CHORD_SHAPES

__all__ = ["Fretboard", "render_svg", "parse_pitch", "parse_interval", "get_scale_intervals", "identify_chord_type", "CHORD_SHAPES"]
