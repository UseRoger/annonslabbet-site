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
  "bg": {
    "granskad": true,
    "granskare": "Bildgranskaren",
    "produkt": "ja",
    "pastaenden": "ja",
    "anatomi": "ja",
    "montering": "ja",
    "ai_person_vid_omdome": false
  },
  "lasbarhet": {
    "bedomd": true,
    "lasbar": true,
    "av": "den som läst texten på mobil",
    "syntetisk": false,
    "kommentar": "Läst på en telefon. Inte ett pixelgolv."
  },
  "font_filer": {"ButikensSans": "ButikensSans-Bold.ttf"},
  "texter": [
    {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72, "font": "ButikensSans", "farg": "#ffffff"},
    {"roll": "pris", "text": "449 kr", "x": 180, "y": 780, "px": 64, "font": "ButikensSans", "farg": "#ffffff", "bricka_farg": "#1d3a2a"}
  ]
}
```

`bild` är den färdiga scenen, med produkten redan i fotografiet. `produkt_png` ignoreras om det följer med. `forma_om`, `crop`, `beskar`, `tvinga_format` och `staplar` avvisas.

`x` och `y` är textens eller brickans övre vänstra hörn i scenens egna pixlar. Det finns ingen fast brickplats.

`bg` är faktakoll. Den är gjord bara när `granskad` är true, `granskare` är ifylld och alla fem fält finns. Saknas något är status `ej_gjord` eller `ofullstandig`, och resultatet är nej. Äldre nycklar som `produkt_stammer` räknas inte som de fälten. `bg.kundgodkannande` och `jon_martin_ok` är false.

`lasbarhet` är ett mänskligt besked, inte ett pixelgolv. Saknas objektet, eller är `bedomd` inte true, blir träffen `LASBARHET_SAKNAS` och resultatet nej. `bedomd: true` och `lasbar: false` blir `LASBARHET` och resultatet nej. `lasbar: true` lossar inte kontrast eller synligt UI-bläck. `syntetisk: true` märker beskedet som fixture. Rapporten sätter `pa_riktig_annons` till false. En fixture är inget påstående om en riktig annons.

`font_filer` pekar på butikens ttf eller otf, relativt JSON-filen eller med absolut sökväg. Den angivna familjen ritas med just den filen. Saknas filen stannar körningen. En annan font används inte i stället.

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
| `matt.block[].synlig_hojd` | Synligt bläckets höjd i px. Ett mätvärde, inte ett golv. |
| `matt.block[].px` | Den px texten sattes med. |
| `matt.ui.black_pixlar` | Bläckpixlar i verktygets mätzon. Bara de sätter UI-stopp. |
| `matt.zon.t2_spec_px` | spec_v1 T2, 36. Rå jämförelse. Provnivå anmärkning. |
| `lasbarhet` | Det besked JSON hade. `pa_riktig_annons` är false. |
| `bg.kundgodkannande` | Alltid false. |

Kontrast under 4,5:1 (K3, spec_v1, mätt på pixlar under bläcket) är stopp i både prov och leveransjämförelsen. spec_v1 T2 på 36 px skrivs som rå träff när satt px ligger under det talet, med rå nivå stopp och provnivå anmärkning. Samma sak gäller B2 om den träffen finns. Inget nytt 36- eller 38-pixelgolv är en provspärr, och tröskeln skalas inte till en ny regel. Synligt bläck i mätzonen stoppar. Em-ruta utan synliga pixlar gör det inte.

`--trio` stoppar bara identiska bilder och exakta crop. Annan likhet är en anmärkning till Jon och Martin.
