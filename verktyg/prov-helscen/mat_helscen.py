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
    KONTRAST_KALLA,
    KONTRAST_MIN,
    KNAPP_FRAS,
    SPARR,
    SPEC_T2_KALLA,
    SPEC_T2_PX,
    UI_ZON_KALLA,
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

UPPDRAG_KRAV = ("fakta", "kopskal", "vinkel", "vinnare", "fotoide")
BG_FALT = ("produkt", "pastaenden", "anatomi", "montering", "ai_person_vid_omdome")


def las_bg(data):
    """Saknad granskning är ej gjord, aldrig ett tyst ja."""
    raw = data.get("bg") if isinstance(data.get("bg"), dict) else {}
    if not raw and isinstance(data.get("forhand"), dict):
        raw = data["forhand"]
    granskad = raw.get("granskad") is True and not _tom(raw.get("granskare"))
    falt = {}
    for nyckel in BG_FALT:
        if nyckel not in raw:
            falt[nyckel] = "saknas"
        else:
            falt[nyckel] = raw[nyckel]
    if not granskad:
        status = "ej_gjord"
    elif any(varde == "saknas" for varde in falt.values()):
        status = "ofullstandig"
    else:
        status = "gjord"
    return {
        "status": status,
        "granskare": raw.get("granskare"),
        "falt": falt,
        "roll": "faktakoll",
        "jon_martin_ok": False,
        "kundgodkannande": False,
    }


def las_lasbarhet(data):
    """Saknat besked är inte ja. En syntetisk fixture är inget påstående om en riktig annons."""
    raw = data.get("lasbarhet") if isinstance(data.get("lasbarhet"), dict) else {}
    bedomd = raw.get("bedomd") is True
    syntetisk = raw.get("syntetisk") is True or data.get("syntetisk") is True
    if not bedomd:
        lasbar = None
    else:
        lasbar = raw.get("lasbar") is True
    if syntetisk:
        notis = "Syntetisk fixture, inget påstående om en riktig annons."
    else:
        notis = "Verktyget intygar inte en riktig annons. Beskedet är det som står i JSON."
    return {
        "bedomd": bedomd,
        "lasbar": lasbar,
        "av": raw.get("av"),
        "syntetisk": syntetisk,
        "pa_riktig_annons": False,
        "kommentar": raw.get("kommentar"),
        "notis": notis,
    }


def _ja(varde):
    return varde is True or varde == "ja"


def las_jobb(data):
    jobb = data.get("jobb") if isinstance(data.get("jobb"), dict) else {}
    jobb_id = jobb.get("job_id")
    if "kostnad" not in jobb:
        kostnad = "ej tillgänglig"
    else:
        kostnad = jobb.get("kostnad")
    kalla = jobb.get("kostnad_kalla")
    fel = None
    if isinstance(kostnad, (int, float)) and _tom(kalla):
        fel = "Kostnad utan kostnad_kalla räknas inte. Saldoskillnad används inte."
        kostnad = "ej tillgänglig"
    elif kostnad not in ("ej tillgänglig", None) and not isinstance(kostnad, (int, float)):
        fel = "Kostnad ska vara ett tal från jobbets svar, eller ej tillgänglig."
        kostnad = "ej tillgänglig"
    return {
        "ok": bool(jobb_id) and fel is None,
        "job_id": jobb_id,
        "kostnad": "ej tillgänglig" if kostnad is None else kostnad,
        "kostnad_kalla": None if _tom(kalla) else kalla,
        "credits": jobb.get("credits"),
        "fel": fel,
    }


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

    if data.get("vag") != "prov-helscen":
        traffar.append({
            "id": "VAG_SAKNAS",
            "text": "Briefen har inte vag prov-helscen. Leverans ritas inte här. render_format.py är orörd och inte fixad.",
        })
    bg = las_bg(data)
    if bg["status"] != "gjord":
        traffar.append({
            "id": "BG_SAKNAS",
            "text": "Faktagranskning är " + bg["status"] + ". Saknade fält är inte ja. Det här är inte Bildgranskarens ok och inte Jon eller Martins ok.",
        })
    else:
        falt = bg["falt"]
        if not _ja(falt["produkt"]):
            traffar.append({"id": "PRODUKT", "text": "BG: produkten stämmer inte med butikens vara."})
        if not _ja(falt["pastaenden"]):
            traffar.append({"id": "FAKTA", "text": "BG: pris eller påstående stämmer inte."})
        if not _ja(falt["anatomi"]) or not _ja(falt["montering"]):
            traffar.append({"id": "ANATOMI", "text": "BG: anatomi eller montering är fel."})
        if falt["ai_person_vid_omdome"] is True or falt["ai_person_vid_omdome"] == "ja":
            traffar.append({"id": "AI_PERSON", "text": "BG: AI-person står bredvid ett omdöme."})
    jobb = las_jobb(data)
    if jobb["fel"]:
        traffar.append({"id": "KOSTNAD", "text": jobb["fel"]})
    lasbarhet = las_lasbarhet(data)
    if not lasbarhet["bedomd"]:
        traffar.append({
            "id": "LASBARHET_SAKNAS",
            "text": "Nödvändigt läsbarhetsbesked saknas. Det blir inte ja genom default. " + lasbarhet["notis"],
        })
    elif lasbarhet["lasbar"] is not True:
        traffar.append({
            "id": "LASBARHET",
            "text": "Uttryckligt besked: texten är inte läsbar på mobil. " + lasbarhet["notis"],
        })

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
                b["synlig_hojd"] = 0
                traffar.append({
                    "id": "INGET_BLACK",
                    "text": (
                        f"{b['roll']} har inget synligt bläck (alfa över {BLACK_TROSKEL}). "
                        "Det är en mätning, inte ett pixelgolv."
                    ),
                })
            else:
                b["synlig_hojd"] = round(black[3] - black[1], 2)
            for etikett, x0, y0, x1, y1 in zoner["forbjudna"]:
                ui_pix += ink_pixlar_i(b["mask"], (x0, y0, x1, y1))
                if korsar_linebox(b["linebox"], (x0, y0, x1, y1)):
                    linebox_ui = True
            if not inom(b["linebox"], zoner["saker"]):
                traffar.append({
                    "id": "Z1",
                    "text": (
                        f"{b['roll']} em-ruta { _fmt(b['linebox']) } ligger utanför mallens säkra yta. "
                        f"Synligt bläck slutar på y {b['black_botten']}. Rå Z1 står kvar. I prov är den anmärkning."
                    ),
                })
            if black is not None and b["roll"] in ("pris", "bevis", "bricka") and not inom(black, zoner["bricka"]):
                traffar.append({
                    "id": "Z3",
                    "text": f"{b['roll']} {b['text']!r} ligger utanför mallens fasta brickzon. Synligt bläck {_fmt(black)}.",
                })
            if b["px"] + 0.5 < SPEC_T2_PX:
                traffar.append({
                    "id": "T2",
                    "text": (
                        f"{b['roll']} är satt till {b['px']:.0f} px. "
                        f"Synlig höjd {b['synlig_hojd']:.0f} px är ett mätvärde. {SPEC_T2_KALLA}"
                    ),
                })
            if b["roll"] == "rubrik":
                lo, hi = zoner["rubrik_px"]
                if b["px"] < lo - 0.5 or b["px"] > hi + 0.5:
                    traffar.append({
                        "id": "T1",
                        "text": f"Rubriken är {b['px']:.0f} px, mallfönstret är {lo:.0f}–{hi:.0f}. Det stoppar inte provet.",
                    })
                if ord_antal(b["text"]) > 8:
                    traffar.append({"id": "K2", "text": f"Rubriken har {ord_antal(b['text'])} ord, malltak 8. Anmärkning i prov."})
            bakgrund = luminanser_under(render["scen"], b["mask"])
            if b["bricka_farg"]:
                bakgrund = [relativ_luminans(b["bricka_farg"])]
            kvot = kontrast_kvot(b["farg"], bakgrund)
            b["kontrast"] = None if kvot is None else round(kvot, 2)
            if kvot is not None and kvot < KONTRAST_MIN:
                traffar.append({
                    "id": "K3",
                    "text": f"{b['roll']} har kontrast {kvot:.2f}:1, minst {KONTRAST_MIN}:1. {KONTRAST_KALLA}",
                })
        if ui_pix:
            traffar.append({
                "id": "UI",
                "text": (
                    f"Synligt bläck ({ui_pix} pixlar över alfa {BLACK_TROSKEL}) ligger i mätzonen. "
                    f"{UI_ZON_KALLA} Em-rutan räknas inte."
                ),
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
            "t2_spec_px": SPEC_T2_PX,
            "t2_kalla": SPEC_T2_KALLA,
            "ui_kalla": UI_ZON_KALLA,
            "reels_fran_y": 1580 * zoner["skala"][1],
            "t1_mall_px": [round(v, 2) for v in zoner["rubrik_px"]],
            "brickzon": [round(v, 2) for v in zoner["bricka"]],
        },
        "lasbarhet": lasbarhet,
        "black_troskel": BLACK_TROSKEL,
        "kontrast_min": KONTRAST_MIN,
        "bild_px": list(render["scen"].size),
        "export_9x16": list(render["scen"].size) == [1080, 1920],
        "produkt_urklipp": "hoppades_over" if data.get("produkt_png") else "inget",
        "beskuren": False,
        "bg": bg,
        "jobb": jobb,
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
        "vag": data.get("vag"),
        "render": "prov-helscen, text i kod. render_format.py anropas inte och är inte ändrad.",
        "gamla_verktyget_andrat": False,
        "andrar_inte": ["render_format.py", "mat_annons.py", "spec_v1.json"],
        "gamla_mallregler_stoppar_inte": True,
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
        "bg": matt["bg"],
        "jobb": matt["jobb"],
        "jon_martin_ok": False,
        "lasbarhet": matt["lasbarhet"],
        "pa_riktig_annons": False,
        "till_bildgranskaren": {
            "stopp_hon_ska_se_som_nej": [
                "K3", "UI", "INGET_BLACK", "LASBARHET_SAKNAS", "LASBARHET",
                "FAKTA", "PRODUKT", "ANATOMI", "AI_PERSON", "BG_SAKNAS", "INTE_NYA_FOTON",
            ],
            "anmarkning": ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "P1", "P2", "T1", "T2", "B2", "K2", "K11", "LIKHET"],
            "maste_hon_gora_sjalv": "Produkt, påståenden mot kallor, anatomi, omdöme och om texten faktiskt är läsbar på mobil. Saknad granskning och saknat läsbarhetsbesked är inte ja.",
            "skick": "Ett meddelande per butik: PNG, den här .mat.json, fotoide, vinkel, kallor. Inte ett kund-ok och inte Jon eller Martins ok.",
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
