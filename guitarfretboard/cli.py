import argparse
import sys
from .core import Fretboard, TUNINGS_GUITAR
from .renderer_svg import render_svg
from .notes import parse_pitch
from .scales import get_scale_intervals, SCALES

def main():
    parser = argparse.ArgumentParser(description="Generate guitar fretboard diagrams from the command line.")
    
    parser.add_argument("--scale", type=str, help="Scale to display (e.g. 'M' for Major, 'm' for minor)")
    parser.add_argument("--arpeggio", type=str, help="Arpeggio to display (e.g. 'Major 7', 'Minor')")
    parser.add_argument("--root", type=str, default="C", help="Root note (e.g. 'C', 'G#')")
    parser.add_argument("--caged", type=str, choices=["C", "A", "G", "E", "D"], help="Filter by CAGED form")
    parser.add_argument("--highlight-caged", action="store_true", help="Highlight CAGED form instead of filtering")
    parser.add_argument("--title", type=str, help="Custom title for the diagram")
    parser.add_argument("--output", type=str, default="fretboard.svg", help="Output SVG filename")
    parser.add_argument("--chord", action="store_true", help="Rotate to vertical chord mode")
    parser.add_argument("--frets", type=int, default=5, help="Number of frets to display")
    parser.add_argument("--left", action="store_true", help="Left-handed mode")
    parser.add_argument("--tuning", type=str, default="standard", help="Instrument tuning (standard, dadgad, drop d, bass, ukulele)")
    parser.add_argument("--theme", type=str, default="default", help="Visual theme (default, dark, vintage, minimalist)")

    args = parser.parse_args()

    # Determine tuning
    tuning_list = TUNINGS_GUITAR.get(args.tuning, TUNINGS_GUITAR["standard"])
    
    title = args.title
    if not title:
        if args.scale:
            title = f"{args.root} {args.scale}"
        elif args.arpeggio:
            title = f"{args.root} {args.arpeggio}"
        else:
            title = args.root

    fb = Fretboard(
        frets_max=args.frets,
        chord=args.chord,
        left_handed=args.left,
        title=title,
        fret_numbers=True,
        tuning=tuning_list,
        theme=args.theme
    )

    if args.scale or args.arpeggio:
        try:
            root_pitch = parse_pitch(args.root)
            
            if args.scale:
                intervals = get_scale_intervals(args.scale)
                fb.legend = [f"Root: {args.root}", f"Scale: {args.scale}"]
            else:
                from guitarfretboard.arpeggios import get_arpeggio_intervals
                intervals = get_arpeggio_intervals(args.arpeggio)
                fb.legend = [f"Root: {args.root}", f"Arpeggio: {args.arpeggio}"]
                
            if args.caged:
                fb.legend.append(f"CAGED Form: {args.caged}")
            
            # Add notes
            from guitarfretboard.notes import parse_interval
            for interval in intervals:
                semitones = parse_interval(interval)
                pitch = (root_pitch + semitones) % 12
                style = "5" if semitones == 0 else "2"
                fb.add_note(pitch, style=style,
                            caged_form=args.caged,
                            highlight_caged_only=args.highlight_caged,
                            root_pitch_caged=root_pitch)
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    render_svg(fb, args.output)
    print(f"Diagram saved to {args.output}")

if __name__ == "__main__":
    main()
