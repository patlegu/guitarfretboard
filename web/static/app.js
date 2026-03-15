document.addEventListener("DOMContentLoaded", async () => {
    const fretboardWrapper = document.getElementById("fretboard-wrapper");
    const chordNameSpan = document.getElementById("chord-name");
    const scaleHeader = document.getElementById("scale-header");
    const chordHeader = document.getElementById("chord-header");
    const patternDisplay = document.getElementById("pattern-display");
    const chordDetectionWrapper = document.getElementById("chord-detection-wrapper");
    const clearBtn = document.getElementById("clear-btn");
    const loader = document.querySelector(".loader");
    
    // UI Elements
    const instrumentSelect = document.getElementById("instrument-select");
    const tuningSelect = document.getElementById("tuning-select");
    const rootSelect = document.getElementById("root-select");
    const patternSelect = document.getElementById("pattern-select");
    const cagedSelect = document.getElementById("caged-select");
    const fretsInput = document.getElementById("frets-input");
    const themeSelect = document.getElementById("theme-select");
    const noteColorsToggle = document.getElementById("note-colors-toggle");
    const patternControls = document.getElementById("pattern-controls");
    const modeRadios = document.getElementsByName("mode");

    let metadata = null;
    let activeNotes = new Map(); // "string-fret" -> pitch

    // --- Initialization ---
    async function init() {
        try {
            const resp = await fetch("/api/metadata");
            metadata = await resp.json();
            
            // Populate Themes
            metadata.themes.forEach(t => {
                const opt = new Option(t.charAt(0).toUpperCase() + t.slice(1), t);
                themeSelect.add(opt);
            });

            updateTuningList();
            updatePatternList();
            loadFretboard();
        } catch (e) {
            console.error("Metadata fetch failed", e);
        }
    }

    function updateTuningList() {
        tuningSelect.innerHTML = "";
        const inst = instrumentSelect.value;
        metadata.tunings[inst].forEach(t => {
            const opt = new Option(t, t);
            tuningSelect.add(opt);
        });
    }

    function updatePatternList() {
        patternSelect.innerHTML = "";
        const mode = getActiveMode();
        if (mode === "Scale") {
            metadata.scales.forEach(s => patternSelect.add(new Option(s, s)));
            patternControls.classList.remove("hidden");
        } else if (mode === "Arpeggio") {
            metadata.arpeggios.forEach(a => patternSelect.add(new Option(a, a)));
            patternControls.classList.remove("hidden");
        } else {
            patternControls.classList.add("hidden");
        }
    }

    function getActiveMode() {
        for (const r of modeRadios) {
            if (r.checked) return r.value;
        }
        return "Chord";
    }

    // --- Core Logic ---
    async function loadFretboard() {
        const mode = getActiveMode();
        
        // Update UI Headers based on mode
        if (mode === "Chord") {
            scaleHeader.classList.add("hidden");
            chordHeader.classList.remove("hidden");
        } else {
            scaleHeader.classList.remove("hidden");
            chordHeader.classList.add("hidden");
            // Set header text to "Scale: " or "Arpeggio: "
            scaleHeader.childNodes[0].textContent = mode + ": ";
            patternDisplay.textContent = rootSelect.value + " " + patternSelect.value;
        }

        const params = new URLSearchParams({
            mode: mode,
            instrument: instrumentSelect.value,
            tuning: tuningSelect.value,
            frets: fretsInput.value,
            root: rootSelect.value,
            pattern: patternSelect.value,
            caged_form: cagedSelect.value,
            theme: themeSelect.value,
            use_note_colors: noteColorsToggle.checked
        });

        loader.style.display = "block";
        try {
            const response = await fetch(`/api/fretboard?${params.toString()}`);
            const data = await response.json();
            
            fretboardWrapper.innerHTML = data.svg;
            
            activeNotes.clear();
            attachInteraction();
            updateChordIdentification();
            
        } catch (error) {
            console.error("Error loading fretboard:", error);
        } finally {
            loader.style.display = "none";
        }
    }

    function attachInteraction() {
        const zones = document.querySelectorAll(".interactive-click-zone");
        zones.forEach(zone => {
            zone.addEventListener("click", () => {
                const string = zone.getAttribute("data-string");
                const fret = zone.getAttribute("data-fret");
                const pitch = parseInt(zone.getAttribute("data-pitch"));
                
                const noteId = `note-${string}-${fret}`;
                const noteGroup = document.getElementById(noteId);
                if (!noteGroup) return;

                const key = `${string}-${fret}`;
                const isCurrentlyVisible = noteGroup.getAttribute("visibility") === "visible";
                
                if (isCurrentlyVisible) {
                    activeNotes.delete(key);
                    noteGroup.setAttribute("visibility", "hidden");
                } else {
                    activeNotes.set(key, pitch);
                    noteGroup.setAttribute("visibility", "visible");
                }
                updateChordIdentification();
            });
        });

        // Initialize activeNotes map with already visible notes (from scales/arps)
        const visibleNotes = document.querySelectorAll('.note-group[visibility="visible"]');
        visibleNotes.forEach(group => {
            const id = group.id; // note-string-fret
            const parts = id.split("-");
            const string = parts[1];
            const fret = parts[2];
            // Find corresponding click zone to get pitch
            const zone = document.querySelector(`.interactive-click-zone[data-string="${string}"][data-fret="${fret}"]`);
            if (zone) {
                activeNotes.set(`${string}-${fret}`, parseInt(zone.getAttribute("data-pitch")));
            }
        });
        updateChordIdentification();
    }

    async function updateChordIdentification() {
        if (activeNotes.size === 0) {
            chordNameSpan.textContent = "None";
            return;
        }
        const pitches = Array.from(activeNotes.values());
        try {
            const response = await fetch("/api/identify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ pitches: pitches })
            });
            const data = await response.json();
            chordNameSpan.textContent = data.chord || "Unknown";
        } catch (e) {}
    }

    // --- Event Listeners ---
    instrumentSelect.addEventListener("change", () => {
        updateTuningList();
        loadFretboard();
    });

    modeRadios.forEach(r => r.addEventListener("change", () => {
        updatePatternList();
        loadFretboard();
    }));

    [tuningSelect, rootSelect, patternSelect, cagedSelect, fretsInput, themeSelect, noteColorsToggle].forEach(el => {
        el.addEventListener("change", loadFretboard);
    });

    clearBtn.addEventListener("click", () => {
        activeNotes.clear();
        updateChordIdentification();
        document.querySelectorAll(".note-group").forEach(g => g.setAttribute("visibility", "hidden"));
    });

    init();
});
