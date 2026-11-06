#!/usr/bin/env python3
"""Gera os efeitos sonoros com a ElevenLabs e empacota tudo em sounds.js.

Uso: ELEVENLABS_API_KEY=... python3 scripts/generate_sounds.py

Só gera o que ainda não existe em sounds/. Para refazer um efeito, apague o
.mp3 dele e rode de novo. O jogo não usa a chave: ele lê apenas o sounds.js,
que embute os áudios para funcionar também abrindo o index.html direto.
"""
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "sounds"
API = "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128"
CLEAN = "Isolated single sound effect for a video game. No music, no voices, no background ambience."

SOUNDS = {
    "bounce": (0.5, "One basketball bounce on outdoor asphalt, a single short rubbery thud with a slight hollow ring."),
    "rim": (0.6, "A basketball hitting a metal hoop rim once, a short bright metallic clank with a little rattle."),
    "board": (0.5, "A basketball hitting a hard outdoor backboard once, a short dull wooden thump."),
    "swish": (0.7, "A basketball dropping cleanly through a chain and rope net, one quick airy swish with a light net rustle."),
    "score": (1.0, "A very small group of friends at a street court giving one short excited cheer and a clap."),
    "whistle": (0.7, "A referee pea whistle, one short sharp blast."),
    "steal": (0.5, "A quick hand slap on a basketball, one short sharp leather smack."),
    "pass": (0.5, "Two hands catching a basketball, one soft quick leather pop."),
    "block": (0.5, "A hard hand swat on a basketball in the air, one forceful leather slap with a whoosh."),
    "perfect": (0.5, "A short bright retro arcade success chime, two rising 8-bit notes."),
    "select": (0.5, "A tiny retro arcade menu blip, one soft 8-bit click."),
    "blink": (0.5, "A short sci-fi alien teleport sound, one quick rising shimmer with a soft pop."),
    "fire": (0.6, "A quick burst of fire whooshing past, one short flaming fireball swoosh."),
    "win": (1.8, "A small street court crowd cheering and clapping in celebration, then quickly fading out."),
}


def generate(name, duration, prompt, key):
    body = json.dumps({
        "text": f"{prompt} {CLEAN}",
        "duration_seconds": duration,
        "prompt_influence": 0.7,
        "model_id": "eleven_text_to_sound_v2",
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        "xi-api-key": key,
        "Content-Type": "application/json",
        "User-Agent": "quadra-sound-generator",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            return res.read()
    except urllib.error.HTTPError as err:
        sys.exit(f"{name}: ElevenLabs HTTP {err.code}: {err.read()[:300].decode(errors='replace')}")


def main():
    OUT.mkdir(exist_ok=True)
    missing = [n for n in SOUNDS if not (OUT / f"{n}.mp3").exists()]
    if missing:
        key = os.environ.get("ELEVENLABS_API_KEY")
        if not key:
            sys.exit("ELEVENLABS_API_KEY não definida")
        for name in missing:
            duration, prompt = SOUNDS[name]
            (OUT / f"{name}.mp3").write_bytes(generate(name, duration, prompt, key))
            print(f"gerado: sounds/{name}.mp3")

    bundle = {n: base64.b64encode((OUT / f"{n}.mp3").read_bytes()).decode() for n in SOUNDS}
    (ROOT / "sounds.js").write_text(
        "// Gerado por scripts/generate_sounds.py. Não edite à mão.\n"
        f"window.QUADRA_SOUNDS = {json.dumps(bundle)};\n"
    )
    print(f"empacotado: sounds.js ({(ROOT / 'sounds.js').stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
