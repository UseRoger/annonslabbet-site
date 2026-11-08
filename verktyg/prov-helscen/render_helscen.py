#!/usr/bin/env python3
"""Rita kodad text ovanpå en hel scen. Bara prov.

Fotografiet behåller sina proportioner. Texten läggs sist, i butikens
typsnitt. Produktens png klistras inte ovanpå scenen, och bilden
beskärs inte till F1–F12.

    python3 render_helscen.py --data annons.json --ut ut/annons.png

Betald leverans (10 motiv, 9:16 och 4:5) ritas fortfarande med
render_format.py i Drive outbox/text-i-kod. Den filen ändras inte.
"""

import argparse
import json
import sys
from pathlib import Path

from gemensamt import Fel, rendera


def main():
    parser = argparse.ArgumentParser(description="Rita provtext i kod ovanpå en hel scen.")
    parser.add_argument("--data", required=True)
    parser.add_argument("--ut", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    if data.get("workflow") == "leverans":
        sys.stderr.write(
            "Det här verktyget ritar bara prov. Betald leverans körs med render_format.py.\n"
        )
        return 2
    data["workflow"] = "prov"
    bas = str(Path(args.data).resolve().parent)
    try:
        resultat = rendera(data, bas)
    except Fel as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    ut = Path(args.ut)
    ut.parent.mkdir(parents=True, exist_ok=True)
    bild = resultat["bild"].convert("RGB")
    bild.save(ut, "PNG")
    placering = []
    for block in resultat["block"]:
        placering.append({k: v for k, v in block.items() if k not in ("mask", "font")})
    sido = ut.with_suffix(".placering.json")
    sido.write_text(json.dumps({
        "bild_px": list(bild.size),
        "scen": data.get("bild"),
        "produkt_png": "hoppades_over" if data.get("produkt_png") else None,
        "block": placering,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if data.get("produkt_png"):
        sys.stderr.write("OBS: produkt_png ignoreras. Scenens produkt ligger kvar som den är.\n")
    sys.stderr.write(f"skrev {ut} ({bild.size[0]}×{bild.size[1]})\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
