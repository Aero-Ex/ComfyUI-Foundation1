import os
import sys
import torch

# Help IDE/LSP find local and ComfyUI modules
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

_COMFY_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
if _COMFY_ROOT not in sys.path:
    sys.path.insert(0, _COMFY_ROOT)

try:
    import comfy.model_management
    import comfy.samplers
    import node_helpers
except ImportError:
    # Fallback or silent fail for IDEs without full path
    pass

try:
    import foundation1_utils
    bpm_to_seconds = foundation1_utils.bpm_to_seconds
    build_foundation1_prompt = foundation1_utils.build_foundation1_prompt
except ImportError:
    from .foundation1_utils import bpm_to_seconds, build_foundation1_prompt


class Foundation1Prompt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "instrument": ([
                    "None", "Synth Lead", "Synth Bass", "Digital Piano", "Pluck", "Grand Piano", "Bell",
                    "Pad", "Atmosphere", "Digital Strings", "FM Synth", "Violin", "Digital Organ",
                    "Supersaw", "Wavetable Bass", "Rhodes Piano", "Cello", "Texture", "Flute",
                    "Reese Bass", "Wavetable Synth", "Electric Bass", "Marimba", "Synthetic",
                    "Electric Guitar", "Sub Bass", "Trumpet", "Pan Flute", "Picked Bass",
                    "Digital Bass", "Brass", "Saxophone", "Choir", "Harp", "Woodwinds",
                    "Church Organ", "Pipe Organ", "Church Bell", "Koto", "Felt Piano",
                    "Harpsichord", "Steel Drums", "Tubular Bells", "Organ", "Analog Bass",
                    "Sitar", "Fiddle", "Piccolo", "World Winds", "Nylon Guitar", "Alto Sax",
                    "Acoustic Guitar", "Soprano Sax", "FM Bass", "Celesta", "Clavinet",
                    "Celtic Harp", "Concert Harp", "CP Piano", "Guitar", "Hammond Organ",
                    "Tack Piano", "Wurlitzer Piano", "Music Box", "Analog Synth", "Kalimba",
                    "Glockenspiel", "Vibraphone", "Ocarina", "Xylophone", "Viola",
                    "Bass Trombone", "Tenor Trombone", "Tenor Sax", "Bassoon", "Irish Flute",
                    "French Horn", "Synth", "Piano", "Clarinet", "Flugelhorn", "Baritone Sax",
                    "Tuba", "Oboe"
                ], {"default": "Synth Lead"}),
                "timbre_preset": ([
                    "None", "Warm", "Bright", "Gritty", "Clean", "Retro", "Snappy", "Crisp",
                    "Dark", "Shiny", "Analog", "Digital", "Ambient", "Soft", "Smooth", "Buzzy",
                    "Overdriven", "Woody", "Biting", "Fat", "Nasal", "Intimate", "Glassy",
                    "Breathy", "Metallic", "Spacey", "Cold", "Subdued", "Deep", "Round",
                    "Hollow", "Punchy", "Vintage", "Harsh", "Muddy", "Muffled", "Thin",
                    "Thick", "Airy", "Rich", "Tight", "Full", "Silky", "Sparkly", "Big",
                    "Small", "Distant", "Near", "Wide", "Mono", "Noisy"
                ], {"default": "None"}),
                "genre": ([
                    "None", "Cinematic", "Lo-fi", "Techno", "House", "Ambient", "Jazz",
                    "Rock", "Hip Hop", "Electronica", "Classical", "Pop", "Funk", "Soul",
                    "R&B", "Trap", "Drum and Bass", "Synthwave", "Cyberpunk", "Orchestral",
                    "World", "Folk", "Country", "Blues"
                ], {"default": "None"}),
                "mood": ([
                    "None", "Epic", "Chill", "Aggressive", "Sad", "Happy", "Mysterious",
                    "Dark", "Energetic", "Relaxed", "Tense", "Dreamy", "Nostalgic",
                    "Suspenseful", "Uplifting", "Melancholic", "Ethereal", "Grimy"
                ], {"default": "None"}),
                "recording_style": ([
                    "None", "Studio", "Live", "Raw", "Processed", "Analog", "Digital",
                    "Lo-fi", "High-fidelity", "Boutique", "Vintage", "Modern"
                ], {"default": "None"}),
                "timbre": ("STRING", {"multiline": True, "default": ""}),
                "notation": ("STRING", {"multiline": True, "default": "Melody"}),
                "fx": ("STRING", {"multiline": True, "default": "Medium Reverb"}),
                "key": ([
                    "None", "C major", "C# major", "D major", "D# major", "E major", 
                    "F major", "F# major", "G major", "G# major", "A major", "A# major", "B major",
                    "C minor", "C# minor", "D minor", "D# minor", "E minor", 
                    "F minor", "F# minor", "G minor", "G# minor", "A minor", "A# minor", "B minor"
                ], {"default": "C minor"}),
                "bpm": ("INT", {"default": 120, "min": 1, "max": 500}),
                "bars": ("INT", {"default": 8, "min": 1, "max": 128}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "build"
    CATEGORY = "Foundation1"

    def build(self, instrument, timbre_preset, genre, mood, recording_style, timbre, notation, fx, key, bpm, bars):
        prompt = build_foundation1_prompt(
            genre=genre,
            mood=mood,
            instrument=instrument,
            timbre=timbre,
            timbre_preset=timbre_preset,
            notation=notation,
            fx=fx,
            recording_style=recording_style,
            key=key,
            bars=bars,
            bpm=bpm
        )
        return (prompt,)

class Foundation1KSampler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 50, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "bpm": ("INT", {"default": 120, "min": 1, "max": 500}),
                "bars": ("INT", {"default": 8, "min": 1, "max": 128}),
            },
            "optional": {
                "latent_audio": ("LATENT",),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"
    CATEGORY = "Foundation1"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, denoise, bpm, bars, latent_audio=None):
        import nodes as comfy_nodes
        
        # Determine seconds for conditioning and empty latent generation
        if latent_audio is not None:
            # Calculate duration from existing latent
            # Based on nodes_audio.py: seconds = length * 2 / (44100 / 2048) * error correcting rounding
            # More direct: length = samples.shape[-1]
            samples = latent_audio["samples"]
            length = samples.shape[-1]
            # seconds = (length / 2) * 2 * 2048 / 44100  -> simplifies to:
            seconds = length * 2048 / 44100
        else:
            # Use manual BPM/Bars for generation
            seconds = bpm_to_seconds(bpm, bars)
            length = round((seconds * 44100 / 2048) / 2) * 2
            latent_tensor = torch.zeros([1, 64, length], device=comfy.model_management.intermediate_device())
            latent_audio = {"samples": latent_tensor, "type": "audio"}

        sampler = comfy_nodes.KSampler()
        
        # Set seconds_total in conditioning (critical for Foundation-1/Stable Audio)
        # Use our calculated 'seconds' which now matches the actual buffer length
        positive = node_helpers.conditioning_set_values(positive, {"seconds_start": 0.0, "seconds_total": seconds})
        negative = node_helpers.conditioning_set_values(negative, {"seconds_start": 0.0, "seconds_total": seconds})
        
        # Run standard sampling
        return sampler.sample(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_audio, denoise)

NODE_CLASS_MAPPINGS = {
    "Foundation1Prompt": Foundation1Prompt,
    "Foundation1KSampler": Foundation1KSampler,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Foundation1Prompt": "Foundation-1 Prompt Builder",
    "Foundation1KSampler": "Foundation-1 KSampler",
}
