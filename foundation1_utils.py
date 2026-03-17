def bpm_to_seconds(bpm, bars, beats_per_bar=4):
    """
    Calculate duration in seconds based on BPM and total bars.
    Default assumes 4/4 time.
    """
    if bpm <= 0:
        return 0
    # One bar in 4/4 with BPM b is (60/b) * 4 seconds
    seconds_per_beat = 60.0 / bpm
    seconds_per_bar = seconds_per_beat * beats_per_bar
    return seconds_per_bar * bars

def build_foundation1_prompt(genre, mood, instrument, timbre, timbre_preset, notation, fx, recording_style, key, bars, bpm):
    """
    Constructs a layered prompt according to Foundation-1 guidelines.
    [Genre] [Mood] [Instrument], [Timbre + Timbre Preset], [Notation], [FX], [Recording Style], [Key], [Bars], [BPM]
    """
    parts = []
    
    # 1. Style & Identity
    identity_parts = []
    if genre and genre != "None":
        identity_parts.append(genre)
    if mood and mood != "None":
        identity_parts.append(mood)
    if instrument and instrument != "None":
        identity_parts.append(instrument)
    
    if identity_parts:
        parts.append(" ".join(identity_parts))
        
    # 2. Timbre
    timbre_parts = []
    if timbre and timbre.strip():
        timbre_parts.append(timbre.strip())
    if timbre_preset and timbre_preset != "None":
        timbre_parts.append(timbre_preset)
        
    if timbre_parts:
        parts.append(", ".join(timbre_parts))
        
    # 3. Musical Behavior / Notation
    if notation and notation.strip():
        parts.append(notation.strip())
        
    # 4. FX
    if fx and fx.strip():
        parts.append(fx.strip())
        
    # 5. Production / Recording Context
    if recording_style and recording_style != "None":
        parts.append(recording_style)
        
    # 6. Technical / Harmonic parameters
    if key and key != "None":
        parts.append(key)
        
    # 7. Structure
    if bars > 0:
        parts.append(f"{bars} Bars")
    if bpm > 0:
        parts.append(f"{bpm} BPM")
        
    return ", ".join(parts)
