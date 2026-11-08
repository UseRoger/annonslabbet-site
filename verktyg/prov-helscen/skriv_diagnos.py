"""Skriv de diagnostiska proven. Bilderna är syntetiska, inte kundannonser."""

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

import mat_helscen
from gemensamt import rita_block

FONT_NAMN = "ProvSans-Bold.ttf"
FONT_SRC = Path(__file__).resolve().parent / "testdata" / "fonts" / FONT_NAMN


def _scen(path, farg, ellips):
    bild = Image.new("RGBA", (1080, 1920), farg)
    ImageDraw.Draw(bild).ellipse(ellips, fill=(232, 214, 180, 255))
    bild.save(path)


def _grund(bild):
    return {
        "vag": "prov-helscen",
        "workflow": "prov",
        "bild": bild,
        "format": "9x16",
        "uppdrag": {
            "fakta": ["Badrock med namnbrodyr", "449 kr"],
            "kopskal": "Första julen med eget namn",
            "vinkel": "Present, inte en produkt på vitt",
            "vinnare": "Presentvinkel som redan säljer hos andra butiker, bara som referens",
            "fotoide": "Barn i badrock på trägolv, lugn yta för rubriken",
        },
        "forhand": {
            "kalla": "BG",
            "produkt_stammer": True,
            "pris_stammer": True,
            "pastaenden_stammer": True,
            "anatomi_ok": True,
            "montering_ok": True,
            "ai_person_vid_omdome": False,
        },
        "syntetisk": True,
        "font_filer": {"ProvSans": FONT_NAMN},
        "font": {"rubrik": "ProvSans", "pris": "ProvSans", "text": "ProvSans"},
    }


def _fixture_lasbar():
    return {
        "bedomd": True,
        "lasbar": True,
        "av": "syntetisk fixture",
        "syntetisk": True,
        "kommentar": "Fixture för att visa bläck mot em-ruta. Inget påstående om en riktig annons.",
    }


def skriv(ut: Path):
    ut.mkdir(parents=True, exist_ok=True)
    shutil.copy(FONT_SRC, ut / FONT_NAMN)
    _scen(ut / "scen-01.png", (26, 42, 34, 255), (360, 780, 760, 1360))
    _scen(ut / "scen-02.png", (18, 32, 58, 255), (640, 780, 980, 1460))
    _scen(ut / "scen-03.png", (62, 36, 28, 255), (400, 900, 720, 1400))

    matt = rita_block(
        {"text": "HALLO", "px": 80, "roll": "rubrik", "font": "ProvSans"},
        {"font_filer": {"ProvSans": str(ut / FONT_NAMN)}},
        str(ut),
    )
    grans = 1580
    y = grans - (matt["black_lokal"][3] + matt["linebox_lokal"][3]) / 2

    jobb = [
        ("01-meter-ren-ej-faktagranskad", "scen-01.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72, "font": "ProvSans", "farg": "#ffffff"},
            {"roll": "pris", "text": "449 kr", "x": 180, "y": 780, "px": 64, "font": "ProvSans", "farg": "#ffffff", "bricka_farg": "#1d3a2a"},
        ], None),
        ("02-linebox", "scen-02.png", [
            {"roll": "rubrik", "text": "HALLO", "x": 200, "y": y, "px": 80, "font": "ProvSans", "farg": "#ffffff"},
        ], _fixture_lasbar()),
        ("03-ui-krock", "scen-03.png", [
            {"roll": "rubrik", "text": "Eget namn", "x": 200, "y": 1600, "px": 72, "font": "ProvSans", "farg": "#ffffff"},
        ], _fixture_lasbar()),
    ]
    for namn, scen, texter, lasbarhet in jobb:
        data = _grund(scen)
        data["texter"] = texter
        if lasbarhet is not None:
            data["lasbarhet"] = lasbarhet
        (ut / f"{namn}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rapport, render = mat_helscen.rapport(data, str(ut), None, "prov")
        for block in rapport.get("matt", {}).get("block") or []:
            if Path(str(block.get("font_fil") or "")).name == FONT_NAMN:
                block["font_fil"] = FONT_NAMN
        render["bild"].convert("RGB").save(ut / f"{namn}.png")
        (ut / f"{namn}.mat.json").write_text(
            json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    trio = mat_helscen.mat_trio([
        ut / "01-meter-ren-ej-faktagranskad.png",
        ut / "02-linebox.png",
        ut / "03-ui-krock.png",
    ])
    (ut / "trio.mat.json").write_text(json.dumps(trio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    skriv(Path(__file__).resolve().parent / "diagnos")
