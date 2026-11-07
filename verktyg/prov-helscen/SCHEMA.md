# Prov i hel scen, JSON

Ett prov. Betald leverans använder fortfarande `render_format.py` och `spec_v1.json` i Drive `outbox/text-i-kod`. De filerna ändras inte här, och F1–F12 är inte ett recept som provet måste följa.

```json
{
  "workflow": "prov",
  "bild": "scen.png",
  "format": "9x16",
  "uppdrag": {
    "fakta": ["Badrock med namnbrodyr", "449 kr"],
    "kopskal": "Första julen med eget namn",
    "vinkel": "Present",
    "vinnare": "Vilken vinnande vinkel som informerade idén",
    "fotoide": "Hela scenen, med lugn yta där texten ska ligga"
  },
  "forhand": {
    "kalla": "BG",
    "produkt_stammer": true,
    "pris_stammer": true,
    "pastaenden_stammer": true,
    "anatomi_ok": true,
    "montering_ok": true,
    "ai_person_vid_omdome": false
  },
  "font_filer": {"Inter": "Inter-Bold.ttf"},
  "texter": [
    {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72, "farg": "#ffffff"},
    {"roll": "pris", "text": "449 kr", "x": 180, "y": 780, "px": 42, "farg": "#ffffff", "bricka_farg": "#1d3a2a"}
  ]
}
```

`bild` är den färdiga scenen, med produkten redan i fotografiet. `produkt_png` ignoreras om det följer med. `forma_om`, `crop`, `beskar`, `tvinga_format` och `staplar` avvisas.

`x` och `y` är textens eller brickans övre vänstra hörn i scenens egna pixlar. Det finns ingen fast brickplats.

`forhand` är BG:s faktakoll, inte ett kundgodkännande. Saknas den blir resultatet nej.

## Rapport

`mat_helscen.py` skriver en JSON med:

| Fält | Betydelse |
|---|---|
| `resultat_raw` | Ja bara om inget rått stopp finns. Skrivs inte om till ja. |
| `resultat_leverans` | Samma träffar med specens nivåer. Inte en leveransbild. |
| `resultat_prov` | Mallzoner, fast bricka, produktandel, mallens rubrikfönster (T1) och Z6 är anmärkningar. |
| `resultat` | Följer `--workflow`, normalt prov. |
| `traffar[].niva_raw` | Nivån innan provregeln. |
| `matt.block[].linebox_botten` | Em-rutans underkant. |
| `matt.block[].black_botten` | Synligt bläck, alfa över 16. |
| `matt.ui.black_pixlar` | Bläckpixlar i Reels-, profil- eller kantzon. Bara de sätter UI-stopp. |
| `bg.kundgodkannande` | Alltid false. |

Kontrast under 4,5:1 (K3) och text under läsgolvet 36 px vid 1080 bredd (T2) är stopp i både prov och leveransjämförelsen. Trösklarna skalas med bildens bredd mot 1080.

`--trio` stoppar bara identiska bilder och exakta crop. Annan likhet är en anmärkning till Jon och Martin.
