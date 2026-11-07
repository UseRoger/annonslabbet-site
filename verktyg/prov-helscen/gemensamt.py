"""Gemensam ritning och mätning för prov som är hela scener.

Texten ritas i kod (Pillow), ovanpå fotografiet. Produkturklipp klistras
inte ovanpå scenen. Scenen beskärs, tänjs eller staplas inte.
"""

import re

from PIL import Image, ImageDraw, ImageFont

# Mallens säkra yta och brickzon är bara anmärkningar. De stoppar inte prov.
# UI-stopp är Bildgranskaren v6: Reels från y 1580 i 9:16, och profilraden
# överst. v6 ger ingen egen pixel för profilraden. Här används spec_v1
# topp-UI y 0–269 (profilnamn, Sponsrad, stäng), inte den gamla innehållsytan
# som började vid y 285 och inte den gamla Reels-gränsen vid y 1248.
ZON_9X16 = {
    "bredd": 1080,
    "hojd": 1920,
    "saker": (108, 285, 972, 1248),
    "forbjudna": [
        ("profilrad", 0, 0, 1080, 269),
        ("reels", 0, 1580, 1080, 1920),
    ],
    "bricka": (108, 1150, 972, 1248),
    "rubrik_px": (88, 120),
}
ZON_4X5 = {
    "bredd": 1080,
    "hojd": 1350,
    "saker": (80, 160, 1000, 1130),
    "forbjudna": [
        ("topp-ui", 0, 0, 1080, 160),
        ("botten-ui", 0, 1130, 1080, 1350),
    ],
    "bricka": (80, 1030, 1000, 1130),
    "rubrik_px": (76, 104),
}

# Synlig texthöjd, inte typsnittets px och inte spec_v1 T2 (36 px).
# Källa: Bildgranskaren v6 och Samordnaren v8, 9:16 vid 1080 px bredd.
SYNLIG_TEXT_MIN_PX = 38
SYNLIG_TEXT_KALLA = "Bildgranskaren v6 och Samordnaren v8: synliga pixlar under 38 px"
KONTRAST_MIN = 4.5
KONTRAST_KALLA = "Bildgranskaren v6 och Samordnaren v8: kontrast under 4,5:1"
BLACK_TROSKEL = 16

FONT_FALLBACK = {
    700: "/usr/share/fonts/truetype/macos/Inter-Bold.ttf",
    600: "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf",
    500: "/usr/share/fonts/truetype/macos/Inter-Medium.ttf",
    400: "/usr/share/fonts/truetype/macos/Inter-Regular.ttf",
}

PRIS_RE = re.compile(r"\d{1,3}(?:[ \u00a0]\d{3})*(?:,\d+)?\s*kr", re.IGNORECASE)
SPARR = (
    (r"\bför dig som (vill|älskar|uppskattar|söker|drömmer om)\b", "for-dig-som-vill"),
    (r"\bkvalitet\b", "kvalitet"),
    (r"\bupptäck\b", "upptack"),
    (r"\bkänn skillnaden\b", "kann-skillnaden"),
    (r"\bperfekt? present\b", "perfekt-present"),
    (r"\bögonblick\b", "ogonblick"),
)
KNAPP_FRAS = (
    "köp nu", "lägg i varukorg", "lägg i varukorgen", "handla nu",
    "beställ nu", "shoppa nu", "köp här",
)
ORD_RE = re.compile(r"[0-9A-Za-zÅÄÖåäöÉé]+")


class Fel(Exception):
    pass


def _skala_rect(rect, sx, sy):
    x0, y0, x1, y1 = rect
    return (x0 * sx, y0 * sy, x1 * sx, y1 * sy)


def zoner_for(storlek):
    w, h = storlek
    aspect = w / h
    if abs(aspect - (1080 / 1920)) < 0.02:
        mall = ZON_9X16
        namn = "9x16"
    elif abs(aspect - (1080 / 1350)) < 0.02:
        mall = ZON_4X5
        namn = "4x5"
    else:
        return None
    sx, sy = w / mall["bredd"], h / mall["hojd"]
    return {
        "namn": namn,
        "skala": (sx, sy),
        "saker": _skala_rect(mall["saker"], sx, sy),
        "forbjudna": [
            (etikett, *_skala_rect((x0, y0, x1, y1), sx, sy))
            for etikett, x0, y0, x1, y1 in mall["forbjudna"]
        ],
        "bricka": _skala_rect(mall["bricka"], sx, sy),
        "rubrik_px": (mall["rubrik_px"][0] * sx, mall["rubrik_px"][1] * sx),
        "synlig_min": SYNLIG_TEXT_MIN_PX * sx,
        "synlig_kalla": SYNLIG_TEXT_KALLA,
    }


def _font_sokvag(block, data, bas):
    from pathlib import Path
    fam = block.get("font") or (data.get("font") or {}).get(block.get("roll") or "", "Inter")
    if not isinstance(fam, str):
        fam = "Inter"
    filer = data.get("font_filer") or {}
    path = filer.get(fam) if isinstance(filer, dict) else None
    if isinstance(path, list) and path:
        path = path[0]["url"] if isinstance(path[0], dict) else path[0]
    if isinstance(path, str) and path:
        kandidat = Path(path)
        if not kandidat.is_absolute():
            kandidat = Path(bas) / kandidat
        if kandidat.exists():
            return str(kandidat), fam
    vikt = int(block.get("vikt") or 700)
    for grans in (700, 600, 500, 400):
        if vikt >= grans and Path(FONT_FALLBACK[grans]).exists():
            return FONT_FALLBACK[grans], fam
    raise Fel(f"Hittar inget ttf för {fam}. Ange font_filer med en ttf- eller otf-fil.")


def ladda_font(block, data, bas):
    path, fam = _font_sokvag(block, data, bas)
    px = float(block["px"])
    return ImageFont.truetype(path, px), path, fam


def radbryt(text, font, max_bredd):
    if not max_bredd:
        return [text]
    rader, cur = [], ""
    for ord_ in text.split():
        trial = ord_ if not cur else f"{cur} {ord_}"
        if font.getlength(trial) <= max_bredd or not cur:
            cur = trial
        else:
            rader.append(cur)
            cur = ord_
    if cur:
        rader.append(cur)
    return rader or [text]


def _black_ruta(bild, troskel=BLACK_TROSKEL):
    px = bild.load()
    w, h = bild.size
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > troskel:
                if x < x0:
                    x0 = x
                if y < y0:
                    y0 = y
                if x > x1:
                    x1 = x
                if y > y1:
                    y1 = y
    if x1 < 0:
        return None
    return (x0, y0, x1 + 1, y1 + 1)


def rita_block(block, data, bas):
    text = str(block.get("text") or "")
    if not text.strip():
        raise Fel("Ett textblock saknar text.")
    font, path, fam = ladda_font(block, data, bas)
    max_bredd = block.get("max_bredd")
    rader = radbryt(text, font, float(max_bredd) if max_bredd else None)
    ascent, descent = font.getmetrics()
    em = ascent + descent
    lh = float(block.get("line_height") or 1)
    if lh < 1:
        raise Fel("line_height under 1 stöds inte.")
    extra = em * (lh - 1)
    bredder = [font.getlength(rad) for rad in rader]
    bredd = max(bredder) if bredder else 0
    hojd = em * len(rader) + extra
    pad = 8
    duk = Image.new("RGBA", (int(bredd) + pad * 2 + 4, int(hojd) + pad * 2 + 4), (0, 0, 0, 0))
    draw = ImageDraw.Draw(duk)
    for i, rad in enumerate(rader):
        draw.text((pad, pad + i * em), rad, font=font, fill=(255, 255, 255, 255))
    lokal_black = _black_ruta(duk)
    return {
        "text": text,
        "rader": rader,
        "font": font,
        "font_fil": path,
        "familj": fam,
        "px": float(block["px"]),
        "ascent": ascent,
        "descent": descent,
        "em": em,
        "extra": extra,
        "bredd": bredd,
        "linebox_lokal": (0, 0, bredd, hojd),
        "black_lokal": None if lokal_black is None else (
            lokal_black[0] - pad, lokal_black[1] - pad,
            lokal_black[2] - pad, lokal_black[3] - pad,
        ),
        "mask": duk,
        "pad": pad,
    }


def lagg_text(overlay, block, matt):
    x, y = float(block["x"]), float(block["y"])
    roll = block.get("roll") or "text"
    farg = _hex(block.get("farg") or "#ffffff")
    bricka = roll in ("pris", "bevis", "bricka")
    if bricka:
        pad_x = float(block.get("pad_x") or 28)
        pad_y = float(block.get("pad_y") or 14)
        radie = float(block.get("radie") or 8)
        bw = matt["bredd"] + pad_x * 2
        bh = matt["em"] * len(matt["rader"]) + pad_y * 2
        form = _hex(block.get("bricka_farg") or "#1d3a2a")
        draw = ImageDraw.Draw(overlay)
        draw.rounded_rectangle((x, y, x + bw, y + bh), radius=radie, fill=form + (255,))
        tx, ty = x + pad_x, y + pad_y
        ruta_black_extra = (x, y, x + bw, y + bh)
    else:
        tx, ty = x, y
        bw = bh = None
        ruta_black_extra = None
    draw = ImageDraw.Draw(overlay)
    for i, rad in enumerate(matt["rader"]):
        draw.text((tx, ty + i * matt["em"]), rad, font=matt["font"], fill=farg + (255,))
    mask = matt["mask"]
    # Synligt bläck mäts på det som faktiskt ritades, inklusive brickans fyllning.
    ensam = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    if bricka:
        ImageDraw.Draw(ensam).rounded_rectangle(
            (x, y, x + bw, y + bh), radius=float(block.get("radie") or 8), fill=(255, 255, 255, 255)
        )
    ensam.alpha_composite(mask, (int(round(tx)) - matt["pad"], int(round(ty)) - matt["pad"]))
    black = _black_ruta(ensam)
    if ruta_black_extra and black:
        black = (
            min(black[0], ruta_black_extra[0]),
            min(black[1], ruta_black_extra[1]),
            max(black[2], ruta_black_extra[2]),
            max(black[3], ruta_black_extra[3]),
        )
    linebox = (
        tx + matt["linebox_lokal"][0],
        ty + matt["linebox_lokal"][1],
        tx + matt["linebox_lokal"][2],
        ty + matt["linebox_lokal"][3] + matt["extra"],
    )
    return {
        "roll": roll,
        "text": matt["text"],
        "px": matt["px"],
        "familj": matt["familj"],
        "font_fil": matt["font_fil"],
        "farg": farg,
        "bricka_farg": _hex(block.get("bricka_farg") or "#1d3a2a") if bricka else None,
        "linebox": [round(v, 2) for v in linebox],
        "synligt_black": None if black is None else [round(v, 2) for v in black],
        "linebox_botten": round(linebox[3], 2),
        "black_botten": None if black is None else round(black[3], 2),
        "mask": ensam,
    }


def _hex(value):
    v = str(value).strip().lstrip("#")
    if len(v) != 6:
        raise Fel(f"Färg ska vara #rrggbb, fick {value!r}.")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def oppna_scen(path):
    bild = Image.open(path).convert("RGBA")
    return bild


def rendera(data, bas):
    for nyckel in ("forma_om", "crop", "beskar", "tvinga_format", "staplar"):
        if data.get(nyckel):
            raise Fel(
                f"{nyckel} är avstängt. En hel scen beskärs, tänjs eller staplas inte "
                "för att passa en gammal mall."
            )
    if not data.get("bild"):
        raise Fel("JSON saknar bild (själva scenen).")
    scen = oppna_scen(_abs(bas, data["bild"]))
    overlay = Image.new("RGBA", scen.size, (0, 0, 0, 0))
    block_matt = []
    for block in data.get("texter") or []:
        matt = rita_block(block, data, bas)
        placerad = lagg_text(overlay, block, matt)
        block_matt.append(placerad)
    ut = Image.alpha_composite(scen, overlay)
    return {"scen": scen, "overlay": overlay, "bild": ut, "block": block_matt}


def _abs(bas, path):
    from pathlib import Path
    p = Path(path)
    if not p.is_absolute():
        p = Path(bas) / p
    return str(p)


def ink_pixlar_i(mask, rect):
    x0, y0, x1, y1 = rect
    px = mask.load()
    w, h = mask.size
    ax0, ay0 = max(0, int(x0)), max(0, int(y0))
    ax1, ay1 = min(w, int(round(x1))), min(h, int(round(y1)))
    n = 0
    for y in range(ay0, ay1):
        for x in range(ax0, ax1):
            if px[x, y][3] > BLACK_TROSKEL:
                n += 1
    return n


def korsar_linebox(linebox, rect):
    return not (
        linebox[2] <= rect[0] or rect[2] <= linebox[0]
        or linebox[3] <= rect[1] or rect[3] <= linebox[1]
    )


def relativ_luminans(rgb):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def kontrast_kvot(text_rgb, bakgrund_luminanser):
    if not bakgrund_luminanser:
        return None
    vals = sorted(bakgrund_luminanser)
    text_l = relativ_luminans(text_rgb)
    median = vals[len(vals) // 2]
    if text_l >= median:
        bg = vals[min(len(vals) - 1, int(round(0.9 * (len(vals) - 1))))]
    else:
        bg = vals[min(len(vals) - 1, int(round(0.1 * (len(vals) - 1))))]
    ljus, mork = max(text_l, bg), min(text_l, bg)
    return (ljus + 0.05) / (mork + 0.05)


def luminanser_under(scen, mask):
    sp, mp = scen.load(), mask.load()
    w, h = mask.size
    ut = []
    for y in range(h):
        for x in range(0, w, 2):
            if mp[x, y][3] > BLACK_TROSKEL:
                ut.append(relativ_luminans(sp[x, y][:3]))
    return ut


def normalisera_pris(text):
    return re.sub(r"\s+", "", text.lower()).replace("\u00a0", "")


def hitta_priser(text):
    return [normalisera_pris(m.group(0)) for m in PRIS_RE.finditer(text or "")]


def ord_antal(text):
    return len(ORD_RE.findall(text or ""))


def inom(rect, outer, tol=1):
    return (
        rect[0] >= outer[0] - tol and rect[1] >= outer[1] - tol
        and rect[2] <= outer[2] + tol and rect[3] <= outer[3] + tol
    )


def skiljda_pixlar(a, b, troskel=12):
    if a.size != b.size:
        return None
    ap, bp = a.convert("RGBA").load(), b.convert("RGBA").load()
    w, h = a.size
    n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            pa, pb = ap[x, y], bp[x, y]
            if any(abs(pa[i] - pb[i]) > troskel for i in range(3)):
                n += 1
    return n


def exact_crop(inner, outer):
    """True om inner är outer, eller en exakt pixelbeskärning av outer."""
    if inner.mode != "RGB":
        inner = inner.convert("RGB")
    if outer.mode != "RGB":
        outer = outer.convert("RGB")
    if inner.size == outer.size:
        return inner.tobytes() == outer.tobytes()
    iw, ih = inner.size
    ow, oh = outer.size
    if iw > ow or ih > oh or iw < 1 or ih < 1:
        return False
    ib, ob = inner.tobytes(), outer.tobytes()
    si, so = iw * 3, ow * 3
    row0 = ib[:si]
    for y in range(oh - ih + 1):
        line = ob[y * so:(y + 1) * so]
        start = 0
        while True:
            x = line.find(row0, start)
            if x < 0:
                break
            if x % 3 == 0:
                ok = True
                for r in range(ih):
                    a = r * si
                    b = (y + r) * so + x
                    if ob[b:b + si] != ib[a:a + si]:
                        ok = False
                        break
                if ok:
                    return True
            start = x + 3
    return False
