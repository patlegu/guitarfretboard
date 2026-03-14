import argparse
import sys
from .core import Fretboard, TUNINGS_GUITAR
from .renderer_svg import render_svg
from .notes import parse_pitch
from .scales import get_scale_intervals, SCALES

def main():
    parser = argparse.ArgumentParser(description="Generate guitar fretboard diagrams from the command line.")
    
    parser.add_argument("--scale", type=str, help="Scale to display (e.g. 'M' for Major, 'm' for minor)")
    parser.add_argument("--root", type=str, default="C", help="Root note for the scale (e.g. 'C', 'G#')")
    parser.add_argument("--title", type=str, help="Custom title for the diagram")
    parser.add_argument("--output", type=str, default="fretboard.svg", help="Output SVG filename")
    parser.add_argument("--chord", action="store_true", help="Rotate to vertical chord mode")
    parser.add_argument("--frets", type=int, default=5, help="Number of frets to display")
    parser.add_argument("--left", action="store_true", help="Left-handed mode")
    parser.add_argument("--tuning", type=str, default="standard", help="Instrument tuning (standard, dadgad, drop d, bass, ukulele)")

    args = parser.parse_args()

    # Determine tuning
    tuning_list = TUNINGS_GUITAR.get(args.tuning, TUNINGS_GUITAR["standard"])
    
    fb = Fretboard(
        frets_max=args.frets,
        chord=args.chord,
        left_handed=args.left,
        title=args.title if args.title else f"{args.root} {args.scale if args.scale else ''}",
        fret_numbers=True,
        tuning=tuning_list
    )

    if args.scale:
        try:
            root_pitch = parse_pitch(args.root)
            intervals = get_scale_intervals(args.scale)
            
            # Simple Legend
            fb.legend = [f"Root: {args.root}", f"Scale: {args.scale}"]
            
            # Add notes
            # 1 should be the root
            from .notes import parse_interval
            for interval in intervals:
                semitones = parse_interval(interval)
                pitch = (root_pitch + semitones) % 12
                style = "5" if semitones == 0 else "2"
                fb.add_note(pitch, style=style)
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    render_svg(fb, args.output)
    print(f"Diagram saved to {args.output}")

if __name__ == "__main__":
    main()
