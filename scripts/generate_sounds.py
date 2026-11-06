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
CLEAN = (
    "Close-miked, dry and punchy, loud and clear, starts immediately and ends in silence. "
    "Single isolated sound effect for a video game. No music, no voices unless described, no background ambience."
)

SOUNDS = {
    "bounce": (0.5, "A leather basketball bouncing once on hard outdoor concrete: a firm low rubbery thump with a short hollow ping."),
    "rim": (0.8, "A basketball slamming into a steel basketball rim: one hard metallic clang with a brief ringing vibration."),
    "board": (0.6, "A basketball banging against a wooden outdoor backboard: one solid resonant wooden thud with a slight metal rattle."),
    "swish": (0.8, "A basketball dropping cleanly through a nylon net: one crisp fast swish of rope, very airy, the classic nothing-but-net sound."),
    "score": (1.2, "A few friends at an outdoor court shouting one short excited yeah together, with two quick claps."),
    "whistle": (0.8, "A referee's metal pea whistle: one loud sharp piercing blast with a fast trill."),
    "steal": (0.5, "A hand swiping a basketball away: one sharp loud leather slap followed by a tiny whoosh."),
    "pass": (0.5, "A chest pass caught in two hands: one quick firm leather smack, no echo."),
    "block": (0.6, "A big volleyball-style spike swat on a basketball: one very hard explosive leather slap with a heavy whoosh."),
    "perfect": (0.7, "A bright arcade power-up chime: two quick rising square wave notes with a sparkle, chiptune style."),
    "select": (0.5, "A crisp retro game menu confirm blip: one short square wave beep, 8-bit, clean."),
    "blink": (0.7, "A sci-fi alien teleport: a fast rising electronic warble that ends with a bright zap and pop."),
    "fire": (0.8, "A fireball launched through the air: one fast roaring flame whoosh with crackling embers."),
    "clunk": (0.5, "A chunky mechanical button pressed on a 1980s portable cassette player: one short plastic clunk with a tiny spring click."),
    "win": (2.5, "A small excited street court crowd erupting in cheers, whistles and applause for two seconds, then fading out."),
}


def generate(name, duration, prompt, key):
    body = json.dumps({
        "text": f"{prompt} {CLEAN}",
        "duration_seconds": duration,
        "prompt_influence": 0.85,
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
