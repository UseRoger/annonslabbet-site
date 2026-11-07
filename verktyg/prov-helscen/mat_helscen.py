#!/usr/bin/env python3
"""Mät ett prov som är en hel scen.

Råträffar behåller specens nivå. Provets allvar nedklassar bara gamla
mallregler. Synligt bläck, inte em-rutans underkant, avgör om text
korsar Reels- eller profil-UI.

    python3 mat_helscen.py --data annons.json --bild ut.png --json ut.mat.json
    python3 mat_helscen.py --trio a.png b.png c.png --json trio.mat.json
    python3 mat_helscen.py --data annons.json --bild ut.png --workflow leverans

--workflow leverans är bara en jämförelse av samma råträffar. Den ritar
ingen leveransbild och anropar inte render_format.py.
"""

import argparse
import json
import sys
from pathlib import Path

from gemensamt import (
    BLACK_TROSKEL,
    KONTRAST_MIN,
    KNAPP_FRAS,
    SPARR,
    Fel,
    exact_crop,
    hitta_priser,
    ink_pixlar_i,
    kontrast_kvot,
    korsar_linebox,
    luminanser_under,
    ord_antal,
    inom,
    relativ_luminans,
    rendera,
    skiljda_pixlar,
    zoner_for,
)
from policy import klassificera

HERE = Path(__file__).resolve().parent

FORHAND_KRAV = (
    "produkt_stammer",
    "pris_stammer",
    "pastaenden_stammer",
    "anatomi_ok",
    "montering_ok",
    "ai_person_vid_omdome",
)
UPPDRAG_KRAV = ("fakta", "kopskal", "vinkel", "vinnare", "fotoide")


def ladda_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("workflow") == "leverans":
        raise Fel(
            "Den här filen är ett prov. Betald leverans ritas med render_format.py, "
            "som inte ändras här."
        )
    data["workflow"] = "prov"
    return data


def _tom(value):
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, dict)) and not value:
        return True
    return False


def traffar_for(data, bas, bild_path=None):
    traffar = []
    info = []
    render = rendera(data, bas)
    block = render["block"]
    alla_texter = "\n".join(b["text"] for b in block)

    uppdrag = data.get("uppdrag") or {}
    saknas = [k for k in UPPDRAG_KRAV if _tom(uppdrag.get(k))]
    if saknas:
        traffar.append({
            "id": "UPPDRAG_SAKNAS",
            "text": "Provet ska börja i fakta, köpskäl, vinkel, vinnare och fotoidé. Saknas: " + ", ".join(saknas),
        })

    forhand = data.get("forhand") or {}
    saknad_bg = [k for k in FORHAND_KRAV if k not in forhand]
    if saknad_bg:
        traffar.append({
            "id": "BG_SAKNAS",
            "text": "BG-faktakoll saknas (" + ", ".join(saknad_bg) + "). Det är inte ett kundgodkännande.",
        })
    else:
        if forhand.get("produkt_stammer") is not True:
            traffar.append({"id": "PRODUKT", "text": "BG: produkten stämmer inte med butikens vara."})
        if forhand.get("pris_stammer") is not True or forhand.get("pastaenden_stammer") is not True:
            traffar.append({"id": "FAKTA", "text": "BG: pris eller påstående stämmer inte."})
        if forhand.get("anatomi_ok") is not True or forhand.get("montering_ok") is not True:
            traffar.append({"id": "ANATOMI", "text": "BG: anatomi eller montering är fel."})
        if forhand.get("ai_person_vid_omdome") is True:
            traffar.append({"id": "AI_PERSON", "text": "BG: AI-person står bredvid ett omdöme."})

    if data.get("produkt_png"):
        info.append("produkt_png ignoreras. Inget urklipp klistras ovanpå scenens produkt.")
    info.append("P1 och P2 mäts inte som mallandel. Helscenen har inget produkturklipp, och ett urklipp räknas inte som godkänt.")
    info.append("K6, K8 och subjektiv likhet mäts inte i kod. De är inte ett tyst ja.")

    zoner = zoner_for(render["scen"].size)
    if data.get("format") in ("9x16", "4x5") and zoner and data["format"].replace(":", "x") != zoner["namn"]:
        traffar.append({
            "id": "Z6",
            "text": f"Scenen är {zoner['namn']}, JSON säger {data['format']}. Bilden skalas inte om.",
        })
    if zoner is None:
        traffar.append({
            "id": "ZONER_SAKNAS",
            "text": f"Bilden är {render['scen'].size[0]}×{render['scen'].size[1]}, varken 9:16 eller 4:5. Ange en scen i de måtten. Ingen stapel läggs till.",
        })
    else:
        if data.get("format") in ("9x16", "4x5"):
            w, h = render["scen"].size
            mall_w = 1080
            mall_h = 1920 if data["format"] == "9x16" else 1350
            if (w, h) != (mall_w, mall_h):
                traffar.append({
                    "id": "Z6",
                    "text": f"Bilden är {w}×{h}, mallmåttet är {mall_w}×{mall_h}. Den beskärs inte och får inga staplar.",
                })
        ui_pix = 0
        linebox_ui = False
        for b in block:
            black = b["synligt_black"]
            if black is None:
                traffar.append({"id": "T2", "text": f"{b['roll']} har inget synligt bläck."})
                continue
            for etikett, x0, y0, x1, y1 in zoner["forbjudna"]:
                ui_pix += ink_pixlar_i(b["mask"], (x0, y0, x1, y1))
                if korsar_linebox(b["linebox"], (x0, y0, x1, y1)):
                    linebox_ui = True
            if not inom(b["linebox"], zoner["saker"]):
                traffar.append({
                    "id": "Z1",
                    "text": (
                        f"{b['roll']} em-ruta { _fmt(b['linebox']) } ligger utanför mallens säkra yta. "
                        f"Synligt bläck slutar på y {b['black_botten']}."
                    ),
                })
            if b["roll"] in ("pris", "bevis", "bricka") and not inom(black, zoner["bricka"]):
                traffar.append({
                    "id": "Z3",
                    "text": f"{b['roll']} {b['text']!r} ligger utanför mallens fasta brickzon. Synligt bläck {_fmt(black)}.",
                })
            if b["px"] + 0.5 < zoner["t2_min"]:
                traffar.append({
                    "id": "T2",
                    "text": f"{b['roll']} är {b['px']:.0f} px, läsgolv {zoner['t2_min']:.0f} px.",
                })
            if b["roll"] == "rubrik":
                lo, hi = zoner["rubrik_px"]
                if b["px"] < lo - 0.5 or b["px"] > hi + 0.5:
                    traffar.append({
                        "id": "T1",
                        "text": f"Rubriken är {b['px']:.0f} px, mallfönstret är {lo:.0f}–{hi:.0f}. Läsbarhet under golvet mäts som T2.",
                    })
                if ord_antal(b["text"]) > 8:
                    traffar.append({"id": "K2", "text": f"Rubriken har {ord_antal(b['text'])} ord, max 8."})
            if b["roll"] in ("pris", "bevis", "bricka") and b["px"] + 0.5 < zoner["b2_min"]:
                traffar.append({
                    "id": "B2",
                    "text": f"Bricktexten är {b['px']:.0f} px, minst {zoner['b2_min']:.0f}.",
                })
            bakgrund = luminanser_under(render["scen"], b["mask"])
            if b["bricka_farg"]:
                bakgrund = [relativ_luminans(b["bricka_farg"])]
            kvot = kontrast_kvot(b["farg"], bakgrund)
            b["kontrast"] = None if kvot is None else round(kvot, 2)
            if kvot is not None and kvot < KONTRAST_MIN:
                traffar.append({
                    "id": "K3",
                    "text": f"{b['roll']} har kontrast {kvot:.2f}:1, minst {KONTRAST_MIN}:1.",
                })
        if ui_pix:
            traffar.append({
                "id": "UI",
                "text": f"Synligt bläck ({ui_pix} pixlar över alfa {BLACK_TROSKEL}) ligger i Reels-, profil- eller kantzon.",
            })
        if linebox_ui and not ui_pix:
            info.append(
                "Em-rutan korsar en UI-gräns men synligt bläck gör det inte. "
                "UI-stopp sätts bara av bläcket. Rå Z1 står kvar om em-rutan lämnar säkra ytan."
            )
        block_ui = {"black_pixlar": ui_pix, "linebox_korsar": linebox_ui}

    low = alla_texter.lower()
    for fras in KNAPP_FRAS:
        if fras in low:
            traffar.append({"id": "B1", "text": f"Texten innehåller knappfrasen {fras!r}."})
    import re
    for monster, namn in SPARR:
        if re.search(monster, low):
            traffar.append({"id": "K10", "text": f"Spärrlista: {namn}."})
    if "—" in alla_texter or "–" in alla_texter:
        traffar.append({"id": "S1", "text": "Tankstreck i texten."})

    tillatna = set()
    for faktum in uppdrag.get("fakta") or []:
        tillatna.update(hitta_priser(str(faktum)))
    for pris in data.get("priser") or []:
        tillatna.update(hitta_priser(str(pris)))
    for hittat in hitta_priser(alla_texter):
        if hittat not in tillatna:
            traffar.append({
                "id": "FAKTA",
                "text": f"Priset {hittat} står i bilden men inte i faktan.",
            })

    if bild_path:
        ut = render["bild"]
        given = __import__("PIL").Image.open(bild_path).convert("RGBA")
        if given.size != ut.size:
            traffar.append({
                "id": "SCEN_ANDRAD",
                "text": f"Den angivna bilden är {given.size[0]}×{given.size[1]}, scenen är {ut.size[0]}×{ut.size[1]}. Ingen omformning görs för att jämföra.",
            })
        else:
            # Diff mot scenen ska bara vara textlagret.
            scen_rgb = render["scen"]
            diff = skiljda_pixlar(scen_rgb, given)
            text_diff = skiljda_pixlar(scen_rgb, ut)
            if diff is None:
                traffar.append({"id": "SCEN_ANDRAD", "text": "Kunde inte jämföra pixlar."})
            elif text_diff is not None and diff > text_diff + max(20, int(text_diff * 0.25)):
                traffar.append({
                    "id": "SCEN_ANDRAD",
                    "text": "Bilden skiljer sig från scenen mer än textlagret. Urklipp, beskärning eller staplar ska inte ligga ovanpå.",
                })

    for b in block:
        b.pop("mask", None)
        b.pop("font", None)

    matt = {
        "block": [
            {k: v for k, v in b.items() if k != "mask"}
            for b in block
        ],
        "ui": block_ui if zoner else None,
        "zon": None if zoner is None else {
            "namn": zoner["namn"],
            "t2_min_px": round(zoner["t2_min"], 2),
            "t1_mall_px": [round(v, 2) for v in zoner["rubrik_px"]],
            "brickzon": [round(v, 2) for v in zoner["bricka"]],
        },
        "black_troskel": BLACK_TROSKEL,
        "kontrast_min": KONTRAST_MIN,
        "bild_px": list(render["scen"].size),
        "produkt_urklipp": "hoppades_over" if data.get("produkt_png") else "inget",
        "beskuren": False,
        "info": info,
    }
    return traffar, matt, render


def _fmt(box):
    x0, y0, x1, y1 = box
    return f"x {x0:.0f}–{x1:.0f} y {y0:.0f}–{y1:.0f}"


def rapport(data, bas, bild_path, workflow):
    traffar, matt, render = traffar_for(data, bas, bild_path)
    klass = klassificera(traffar, workflow)
    ut = {
        "verktyg": "prov-helscen",
        "policy": "prov-helscen-2026-11-07",
        "workflow": workflow,
        "detta_ar_inte_en_leveransrendering": True,
        "andrar_inte": ["render_format.py", "mat_annons.py", "spec_v1.json"],
        "resultat_raw": klass["resultat_raw"],
        "resultat_leverans": klass["resultat_leverans"],
        "resultat_prov": klass["resultat_prov"],
        "resultat": klass["resultat"],
        "raw_ar_inte_omskriven": True,
        "stopp": len(klass["brott"]),
        "anmarkningar": len(klass["anmarkningar"]),
        "brott": klass["brott"],
        "anmarkningsrader": klass["anmarkningar"],
        "traffar": klass["traffar"],
        "hur_allvar_harleds": klass["hur_allvar_harleds"],
        "matt": matt,
        "bg": {
            "roll": "faktakoll",
            "kundgodkannande": False,
            "kalla": (data.get("forhand") or {}).get("kalla"),
        },
    }
    for rad in matt["info"]:
        if rad not in ut["hur_allvar_harleds"]:
            ut["hur_allvar_harleds"].append(rad)
    return ut, render


def mat_trio(paths):
    from PIL import Image
    bilder = [Image.open(p).convert("RGB") for p in paths]
    traffar = []
    par = []
    for i in range(len(bilder)):
        for j in range(i + 1, len(bilder)):
            a, b = bilder[i], bilder[j]
            if a.size == b.size and a.tobytes() == b.tobytes():
                slag = "identisk"
            elif a.size[0] * a.size[1] <= b.size[0] * b.size[1] and exact_crop(a, b):
                slag = "crop"
            elif b.size[0] * b.size[1] < a.size[0] * a.size[1] and exact_crop(b, a):
                slag = "crop"
            else:
                slag = "olika"
            par.append({"a": Path(paths[i]).name, "b": Path(paths[j]).name, "slag": slag})
            if slag in ("identisk", "crop"):
                traffar.append({
                    "id": "INTE_NYA_FOTON",
                    "text": f"{Path(paths[i]).name} och {Path(paths[j]).name} är {slag}, inte två nya foton.",
                })
    traffar.append({
        "id": "LIKHET",
        "niva": "varning",
        "text": "Subjektiv likhet lämnas till Jon och Martin.",
    })
    klass = klassificera(traffar, "prov")
    return {
        "verktyg": "prov-helscen",
        "policy": "prov-helscen-2026-11-07",
        "trio": [str(p) for p in paths],
        "par": par,
        "tre_nya_foton": not any(p["slag"] != "olika" for p in par),
        "resultat_raw": klass["resultat_raw"],
        "resultat": klass["resultat"],
        "raw_ar_inte_omskriven": True,
        "brott": klass["brott"],
        "anmarkningsrader": klass["anmarkningar"],
        "hur_allvar_harleds": klass["hur_allvar_harleds"] + [
            "Identisk kopia eller exakt crop stoppar påståendet tre nya foton. "
            "Övrig likhet är en anmärkning, inte ett stopp."
        ],
        "bg": {"roll": "faktakoll", "kundgodkannande": False},
    }


def main():
    parser = argparse.ArgumentParser(description="Mät ett prov i hel scen. Skriver rå nivå och provets allvar.")
    parser.add_argument("--data")
    parser.add_argument("--bild", help="Färdig PNG. Jämförs med scenen så att bara textlagret får skilja.")
    parser.add_argument("--json", required=True)
    parser.add_argument("--workflow", choices=("prov", "leverans"), default="prov")
    parser.add_argument("--trio", nargs=3)
    args = parser.parse_args()
    try:
        if args.trio:
            rapporten = mat_trio(args.trio)
        else:
            if not args.data:
                parser.error("ange --data eller --trio")
            data = ladda_json(args.data)
            bas = str(Path(args.data).resolve().parent)
            rapporten, _render = rapport(data, bas, args.bild, args.workflow)
    except Fel as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(rapporten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sys.stderr.write(
        f"{rapporten['resultat'].upper()}  rå {rapporten['resultat_raw'].upper()}  {args.json}\n"
    )
    return 0 if rapporten["resultat"] == "ja" else 1


if __name__ == "__main__":
    sys.exit(main())
