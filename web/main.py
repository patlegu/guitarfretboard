from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import os
import sys

# Add parent directory to path so we can import guitarfretboard
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from guitarfretboard.core import TUNINGS_GUITAR, TUNINGS_BASS, TUNINGS_UKULELE
from guitarfretboard.scales import SCALES
from guitarfretboard.arpeggios import ARPEGGIOS
from guitarfretboard.notes import identify_chord_type, parse_pitch, parse_interval
from guitarfretboard import parse_pitch, Fretboard
import tempfile

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

class IdentifyRequest(BaseModel):
    pitches: List[int]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/metadata")
async def get_metadata():
    from guitarfretboard.scales import HIDE_SCALES
    visible_scales = [s for s in SCALES.keys() if s not in HIDE_SCALES]
    return {
        "tunings": {
            "Guitar": list(TUNINGS_GUITAR.keys()),
            "Bass": list(TUNINGS_BASS.keys()),
            "Ukulele": list(TUNINGS_UKULELE.keys()),
        },
        "scales": visible_scales,
        "arpeggios": list(ARPEGGIOS.keys()),
        "themes": ["default", "dark", "vintage", "minimalist"]
    }

@app.get("/api/fretboard")
async def get_fretboard(
    mode: str = "Scale",
    instrument: str = "Guitar",
    tuning: str = "standard",
    frets: int = 12,
    root: str = "C",
    pattern: str = "M",
    caged_form: str = "None",
    theme: str = "default",
    use_note_colors: bool = True
):
    # Determine tuning
    if instrument == "Guitar":
        t = TUNINGS_GUITAR.get(tuning, TUNINGS_GUITAR["standard"])
    elif instrument == "Bass":
        t = TUNINGS_BASS.get(tuning, TUNINGS_BASS["standard"])
    else:
        t = TUNINGS_UKULELE.get(tuning, TUNINGS_UKULELE["standard"])
        
    fb = Fretboard(frets_max=frets, tuning=t, theme=theme, interactive=True, use_note_colors=use_note_colors)
    
    if mode in ["Scale", "Arpeggio"]:
        root_pitch = parse_pitch(root)
        if mode == "Scale":
            from guitarfretboard.scales import get_scale_intervals
            intervals = get_scale_intervals(pattern)
        else:
            from guitarfretboard.arpeggios import get_arpeggio_intervals
            intervals = get_arpeggio_intervals(pattern)
            
        caged = None if caged_form == "None" else caged_form
        
        for interval in intervals:
            semitones = parse_interval(interval)
            pitch = (root_pitch + semitones) % 12
            style = "5" if semitones == 0 else "2"
            fb.add_note(pitch, style=style, caged_form=caged, root_pitch_caged=root_pitch)
            
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
        tmp_path = tmp.name
        
    fb.export(tmp_path)
    
    with open(tmp_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        
    os.remove(tmp_path)
    
    return {"svg": svg_content}

@app.post("/api/identify")
async def identify_chord(request: IdentifyRequest):
    name = identify_chord_type(request.pitches)
    return {"chord": name}
