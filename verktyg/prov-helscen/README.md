# Prov i hel scen

Fristående verktyg. Kör den här mappen. Klona inte repot för att producera proven.

`render_format.py` i Drive `outbox/text-i-kod` är inte ändrad och inte fixad. Den här koden anropar den inte. Leverans (10 motiv, 9:16 och 4:5) körs som förut med den filen.

## Så väljs vägen

Briefen ska ha `"vag": "prov-helscen"`. Då är det här kommandot rätt, inte `render_format.py`.

Scenen ska redan vara 1080×1920. Verktyget skalar inte om och lägger inte till staplar. `export_9x16` i `.mat.json` är true bara då.

```bash
python3 render_helscen.py --data brief.json --ut labb/bild1.png
python3 mat_helscen.py --data brief.json --bild labb/bild1.png --json labb/bild1.mat.json
python3 jobbmanifest.py --json jobb.json
```

Kör kommandona inifrån den uppackade mappen `prov-helscen`. `brief.json` behöver `vag`, `bild`, `format` `9x16`, `uppdrag` (fakta, köpskäl, vinkel, vinnare, fotoide), `font_filer` och `texter` med `x`, `y`, `px`. Prisbrickan ligger där bilden har plats.

Butikens typsnitt anges i `font_filer`, en ttf eller otf per familjenamn. Saknas filen stannar körningen och namnger sökvägen. En angiven font byts inte ut mot en annan, och ingen systemsökväg fylls i. Testpaketets egen font är `testdata/fonts/ProvSans-Bold.ttf` (licens i samma mapp, CC0). Den är bara till för de syntetiska proven.

`.mat.json` har rå nivå och provets allvar. Z1–Z5, fast brickzon, T1-fönstret, spec_v1 T2 (36 px) och B2 syns som rå träff med ursprung och nivå, och är anmärkning i prov. De är inte en ny provspärr. Kontrast under 4,5:1 (spec_v1 K3, mätt på pixlar under bläcket) stoppar. Synligt bläck i verktygets mätzon stoppar: profilrad y 0–269 och Reels från y 1580 på 1080×1920. Em-rutan ensam, utan synliga pixlar, är inte en UI-krock. Zonen är en mätning i det här verktyget, inte ett aktiverat handboksbeslut.

Saknad faktagranskning är `bg.status` `ej_gjord` och resultat nej. Saknat läsbarhetsbesked (`lasbarhet.bedomd` inte true) är `LASBARHET_SAKNAS` och resultat nej. Ett uttryckligt `lasbar: false` stoppar. Ett uttryckligt ja lossar inte kontrast eller UI-bläck. `syntetisk: true` är en fixture och inget påstående om en riktig annons. Fält fylls inte i som ja för att de saknas. Det är inte Jon eller Martins ok.

`jobb.json` ska ha `job_id`. `kostnad` är talet från jobbets svar tillsammans med `kostnad_kalla`, eller exakt `ej tillgänglig`. Utan källa blir talet inte godkänt. Saldoskillnad används inte.

Till Bildgranskaren: PNG, `.mat.json`, fotoide, vinkel och källor, ett meddelande per butik. Avsnittet `till_bildgranskaren` i rapporten säger vad som är nej och vad som är anmärkning.


Betald leverans är orörd. `render_format.py`, `mat_annons.py`, `spec_v1.json` och `format/F1.html`–`F12.html` finns i Google Drive, mappen `outbox/text-i-kod` (id `1d3pBsrC1-O0pY_vUHk81hZK6u7bej7TE`). De filerna är inte ersatta och inte kopierade in hit. Leveransen är fortfarande 10 motiv i 9:16 och 4:5, med de regler de verktygen redan har.

Provet ritas inte genom att klippa ut produkten och lägga den ovanpå en färdig scen, och inte genom att beskära scenen till en gammal mall. Fotot är hela annonsen. Texten ritas sist, i kod, på den plats JSON anger.

Higgsfield-taket på 100 krediter per dag ligger inte i det här repot och höjs inte här. Verktyget genererar inga bilder.

## Kör

Pillow 10 eller nyare ska redan finnas. `requirements.txt` är listan. `pip install` behövs bara om Pillow saknas, och det kräver nät. Kommandona nedan gör det inte.

```bash
python3 -m unittest test_prov_helscen.py test_mail_v33.py -v
python3 render_helscen.py --data diagnos/01-meter-ren-ej-faktagranskad.json --ut /tmp/prov.png
python3 mat_helscen.py --data diagnos/01-meter-ren-ej-faktagranskad.json --bild diagnos/01-meter-ren-ej-faktagranskad.png --json /tmp/prov.mat.json
python3 mat_helscen.py --data diagnos/02-linebox.json --bild diagnos/02-linebox.png --json /tmp/linebox.mat.json
python3 mat_helscen.py --data diagnos/03-ui-krock.json --bild diagnos/03-ui-krock.png --json /tmp/ui.mat.json
python3 mat_helscen.py --trio diagnos/scen-01.png diagnos/scen-02.png diagnos/scen-03.png --json /tmp/trio.mat.json
python3 jobbmanifest.py --json jobb.exempel.json
```

Indata ligger i paketet: `diagnos/01-meter-ren-ej-faktagranskad.json`, `diagnos/02-linebox.json`, `diagnos/03-ui-krock.json`, scenerna `diagnos/scen-0{1,2,3}.png` och testfonten `diagnos/ProvSans-Bold.ttf`. Samma font och licensen ligger i `testdata/fonts/`. Inget av kommandona behöver sudo eller en förvald sökväg på värden.

Exit 0 när `resultat` är ja, exit 1 när provet har stopp, exit 2 vid fel i underlaget. Rapporten skrivs i båda de första fallen. De tre diagnoserna är syntetiska och har stopp, så de tre `mat_helscen.py --data`-kommandona slutar med exit 1.

`--workflow leverans` byter bara allvar på samma råträffar, så man ser vad den gamla specen hade sagt. Den ritar ingen leveransbild.

woff2 är webbläsarens format i den gamla renderaren och används inte här, eftersom bläcket mäts i bilden.

## Allvar

Rå stopp står kvar i `resultat_raw` och i `traffar[].niva_raw`. Provets `resultat` kan vara ja ändå, när stoppet bara var en gammal mallregel. Det är inte samma sak som att råmätningen blev ja.

Stopp i prov: fel pris eller påstående, saknad faktagranskning, BG som säger att produkt, anatomi eller montering är fel, AI-person vid omdöme, kontrast under 4,5:1, saknat eller nekande läsbarhetsbesked, inget synligt bläck, synligt bläck i mätzonen, identisk bild eller exakt crop som påstås vara ett nytt foto.

Anmärkning i prov: mallens zoner, fast brickplats, produktandel, mallens rubrikfönster (T1), spec_v1 T2 (36 px) och B2, fel pixelmått (Z6) och subjektiv likhet. Satt px och synlig höjd skrivs som mätvärden. De inför inget nytt globalt pixelgolv.

Em-rutans underkant ensam räcker inte för att säga att texten korsar en gräns. `matt.ui.black_pixlar` är bläcket.

BG kräver `granskad`, `granskare` och fälten produkt, pastaenden, anatomi, montering, ai_person_vid_omdome. Äldre nycklar i `forhand` räknas inte som gjord granskning. `bg.kundgodkannande` är false.

Fält och exempel står i `SCHEMA.md`. Diagnosbilderna i `diagnos/` är syntetiska, inte kundannonser.

## Mail-copy v3.3

`fixtures/mail-v3.2.md` är Drive-filen `2026-11-03 2035 - Mail-copy v3.2` (id `1DnFGpBQlsG8lds9Ush-aPQHp-Cz_bH8v`). `mailcopy.py` bygger v3.3 genom att byta versionssidan och lägga in Mail 2 Varm. Övriga avsnitt är samma byte. Den kanoniska kopian för Brevbäraren ligger i Drive-mappen `outbox`, inte som en kundsida på sajten. Handboken aktiveras inte här.
