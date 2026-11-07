"""Allvar för prov, vid sidan av betald leverans.

spec_v1.json, render_format.py och mat_annons.py i Drive outbox/text-i-kod
ändras inte. Nivåerna nedan är avskrivna från spec_v1.json
(id 1DiNpmHt3fqRgMvk5ZHLr8jPIzQXpsa3A, ändrad 2026-10-30) så att
jämförelseläget "leverans" behåller samma stopp som den filen.

Provmallen nedklassar gamla mallregler (zoner, brickplats, produktandel,
mallens rubrikfönster, specens T2 på 36 px och B2) till anmärkning.
Kontrast och synligt UI-bläck förblir stopp. Ett nytt 36- eller 38-pixelgolv
är inte en provregel. Saknat eller nekande läsbarhetsbesked förblir stopp.
Rå nivån skrivs alltid kvar. Ett rått stopp blir inte ett tyst ja.
"""

LEVERANS_NIVA = {
    "Z1": "stopp",
    "Z2": "varning",
    "Z3": "stopp",
    "Z4": "varning",
    "Z5": "stopp",
    "Z6": "stopp",
    "T1": "stopp",
    "T2": "stopp",
    "T3": "stopp",
    "T4": "stopp",
    "T5": "varning",
    "T6": "stopp",
    "T7": "stopp",
    "T8": "stopp",
    "T9": "varning",
    "T10": "stopp",
    "T11": "stopp",
    "K2": "stopp",
    "K3": "stopp",
    "K5": "manuell",
    "K6": "manuell",
    "K7": "manuell",
    "K8": "manuell",
    "K9": "stopp",
    "K10": "stopp",
    "K11": "stopp",
    "K12": "stopp",
    "B1": "stopp",
    "B2": "stopp",
    "P1": "stopp",
    "P2": "stopp",
    "P3": "varning",
    "S1": "stopp",
    "S2": "stopp",
    "S3": "varning",
}

# Gamla mallregler. De mäts och syns i rårapporten, men stoppar inte ett prov.
PROV_ANMARKNING = {
    "Z1", "Z2", "Z3", "Z4", "Z5", "Z6",
    "P1", "P2", "P3",
    "K2", "K10", "K11",
    "T1", "T2", "T9", "B2",
    "LIKHET",
}

# T2 (spec_v1, 36 px) och B2 är råa mallträffar och anmärkningar i prov.
# Inget pixelgolv på 36 eller 38 px läggs till som provspärr.
ALLTID_STOPP = {
    "UI", "K3", "K9", "K12", "B1",
    "S1", "S2", "T3", "T4", "T6", "T7", "T8", "T10", "T11",
    "FAKTA", "ANATOMI", "AI_PERSON", "PRODUKT",
    "BG_SAKNAS", "LASBARHET_SAKNAS", "LASBARHET", "INGET_BLACK",
    "INTE_NYA_FOTON", "SCEN_ANDRAD",
    "UPPDRAG_SAKNAS", "ZONER_SAKNAS", "VAG_SAKNAS", "KOSTNAD",
}

SKAL = {
    "Z1": "Rå Z1 är mallens säkra yta (DOM- eller em-ruta). I prov är den en anmärkning. Synligt bläck mot Reels- eller profil-UI är regeln UI och förblir stopp.",
    "Z2": "Rubrikzonen i mallen är en anmärkning i prov.",
    "Z3": "Fast brickzon är en gammal mallregel. I prov får brickan ligga där den är läsbar och fri från UI.",
    "Z4": "Produktzonens mittpunkt är en mallregel, anmärkning i prov.",
    "Z5": "Text över produktens urklippsruta är en mallregel. Helscenen har inget urklipp.",
    "Z6": "Annonsen tvingas inte till mallens pixelmått. Ingen beskärning och inga staplar läggs till för att träffa måttet.",
    "T1": "Mallens rubrikfönster (88–120 px) är en anmärkning. Läsbarhet är ett uttryckligt besked, inte ett 36- eller 38-pixelgolv.",
    "T2": "spec_v1 T2, 36 px, är en rå träff. I prov är den anmärkning. Inget nytt pixelgolv införs.",
    "B2": "spec_v1 B2, bricka under 38 px, är en rå träff om den mäts. I prov är den anmärkning.",
    "P1": "Kravet på ett eget produkturklipp gäller inte helscen.",
    "P2": "Produktens andel av ytan är en mallregel och stoppar inte provet.",
    "K11": "F1–F12 är referenser för prov, inte tre obligatoriska mallar.",
    "LIKHET": "Subjektiv likhet avgörs av Jon och Martin, inte av mätaren.",
}


def niva_leverans(traff):
    if traff.get("niva"):
        return traff["niva"]
    return LEVERANS_NIVA.get(traff["id"], "stopp")


def niva_prov(traff):
    rid = traff["id"]
    if rid in ALLTID_STOPP:
        return "stopp"
    raw = niva_leverans(traff)
    if rid in PROV_ANMARKNING and raw == "stopp":
        return "anmarkning"
    if raw == "stopp":
        return "stopp"
    if raw == "varning":
        return "anmarkning"
    return raw


def klassificera(traffar, workflow):
    if workflow not in ("prov", "leverans"):
        raise ValueError("workflow ska vara prov eller leverans")
    rader = []
    for traff in traffar:
        raw = niva_leverans(traff)
        prov = niva_prov(traff)
        rader.append({
            "id": traff["id"],
            "text": traff.get("text") or "",
            "niva_raw": raw,
            "niva_leverans": raw,
            "niva_prov": prov,
        })

    def effektiv(rad):
        return rad["niva_leverans"] if workflow == "leverans" else rad["niva_prov"]

    brott_raw = [r for r in rader if r["niva_raw"] == "stopp"]
    brott = [r for r in rader if effektiv(r) == "stopp"]
    anmarkningar = [r for r in rader if effektiv(r) in ("anmarkning", "varning")]
    harledning = []
    for rad in rader:
        if rad["niva_raw"] == "stopp" and rad["niva_prov"] != "stopp":
            harledning.append(
                f"{rad['id']}: rå nivå stopp står kvar. "
                f"I prov blir den anmärkning. {SKAL.get(rad['id'], '')}"
            )
        elif rad["niva_raw"] == "stopp" and rad["niva_prov"] == "stopp":
            harledning.append(
                f"{rad['id']}: stopp i både rå mätning och prov. "
                "Den nedklassas inte."
            )
    if not harledning:
        harledning.append("Inga råa stopp att omklassificera.")
    resultat_raw = "nej" if brott_raw else "ja"
    resultat = "nej" if brott else "ja"
    return {
        "workflow": workflow,
        "resultat_raw": resultat_raw,
        "resultat_leverans": "nej" if any(r["niva_leverans"] == "stopp" for r in rader) else "ja",
        "resultat_prov": "nej" if any(r["niva_prov"] == "stopp" for r in rader) else "ja",
        "resultat": resultat,
        "raw_ar_inte_omskriven": True,
        "traffar": rader,
        "brott": [f"{r['id']}: {r['text']}" for r in brott],
        "anmarkningar": [f"{r['id']}: {r['text']}" for r in anmarkningar],
        "hur_allvar_harleds": harledning,
    }
