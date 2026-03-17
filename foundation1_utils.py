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

def build_foundation1_prompt(family, sub_family, timbre, fx, notation, key, bars, bpm):
    """
    Constructs a layered prompt according to Foundation-1 guidelines.
    [Instrument Family / Sub-Family], [Timbre], [Musical Behavior / Notation], [FX], [Key], [Bars], [BPM]
    """
    parts = []
    
    # Instrument Identity
    if sub_family and sub_family != "None":
        parts.append(sub_family)
    elif family and family != "None":
        parts.append(family)
        
    # Timbre
    if timbre and timbre.strip():
        parts.append(timbre.strip())
        
    # Musical Behavior / Notation
    if notation and notation.strip():
        parts.append(notation.strip())
        
    # FX
    if fx and fx.strip():
        parts.append(fx.strip())
        
    # Key
    if key and key != "None":
        parts.append(key)
        
    # Bars & BPM
    if bars > 0:
        parts = parts + [str(bars) + " Bars"]
    if bpm > 0:
        parts = parts + [str(bpm) + " BPM"]
        
    return ", ".join(parts)
