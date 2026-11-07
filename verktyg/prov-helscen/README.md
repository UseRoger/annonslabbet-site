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

`brief.json` behöver `vag`, `bild`, `format` `9x16`, `uppdrag` (fakta, köpskäl, vinkel, vinnare, fotoide) och `texter` med `x`, `y`, `px`. Prisbrickan ligger där bilden har plats.

`.mat.json` har rå nivå och provets allvar. Z1–Z5, fast brickzon, T1-fönstret och T2 på 36 px stoppar inte. Synlig texthöjd under 38 px (Bildgranskaren v6 och Samordnaren v8, vid 1080 px bredd), kontrast under 4,5:1, och synligt bläck i Reels från y 1580 eller profilraden y 0–269 stoppar. Em-rutan ensam stoppar inte.

Saknad faktagranskning är `bg.status` `ej_gjord` och resultat nej. Det är inte Bildgranskarens ok och inte Jon eller Martins ok. Fälten fylls inte i som ja för att de saknas.

`jobb.json` ska ha `job_id`. `kostnad` är talet från jobbets svar tillsammans med `kostnad_kalla`, eller exakt `ej tillgänglig`. Utan källa blir talet inte godkänt. Saldoskillnad används inte.

Till Bildgranskaren: PNG, `.mat.json`, fotoide, vinkel och källor, ett meddelande per butik. Avsnittet `till_bildgranskaren` i rapporten säger vad som är nej och vad som är anmärkning.


Betald leverans är orörd. `render_format.py`, `mat_annons.py`, `spec_v1.json` och `format/F1.html`–`F12.html` finns i Google Drive, mappen `outbox/text-i-kod` (id `1d3pBsrC1-O0pY_vUHk81hZK6u7bej7TE`). De filerna är inte ersatta och inte kopierade in hit. Leveransen är fortfarande 10 motiv i 9:16 och 4:5, med de regler de verktygen redan har.

Provet ritas inte genom att klippa ut produkten och lägga den ovanpå en färdig scen, och inte genom att beskära scenen till en gammal mall. Fotot är hela annonsen. Texten ritas sist, i kod, på den plats JSON anger.

Higgsfield-taket på 100 krediter per dag ligger inte i det här repot och höjs inte här. Verktyget genererar inga bilder.

## Kör

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest test_prov_helscen.py test_mail_v33.py -v
python3 render_helscen.py --data diagnos/01-meter-ren-ej-faktagranskad.json --ut /tmp/prov.png
python3 mat_helscen.py --data diagnos/01-meter-ren-ej-faktagranskad.json --bild /tmp/prov.png --json /tmp/prov.mat.json
python3 mat_helscen.py --trio a.png b.png c.png --json /tmp/trio.mat.json
python3 jobbmanifest.py --json jobb.json
```

Exit 0 när `resultat` är ja, exit 1 när provet har stopp, exit 2 vid fel i underlaget. Rapporten skrivs i båda de första fallen.

`--workflow leverans` byter bara allvar på samma råträffar, så man ser vad den gamla specen hade sagt. Den ritar ingen leveransbild.

Typsnitt anges som ttf eller otf i `font_filer`. Saknas filen används Inter från systemet, och rapporten säger vilken fil som ritades. woff2 är webbläsarens format i den gamla renderaren och används inte här, eftersom bläcket mäts i bilden.

## Allvar

Rå stopp står kvar i `resultat_raw` och i `traffar[].niva_raw`. Provets `resultat` kan vara ja ändå, när stoppet bara var en gammal mallregel. Det är inte samma sak som att råmätningen blev ja.

Stopp i prov, bland annat: fel pris eller påstående, BG som säger att produkt, anatomi eller montering är fel, AI-person vid omdöme, kontrast under 4,5:1, text under läsgolvet, synligt bläck i Reels- eller profilzonen, identisk bild eller exakt crop som påstås vara ett nytt foto.

Anmärkning i prov: mallens zoner, fast brickplats, produktandel, mallens rubrikfönster (T1), fel pixelmått (Z6) och subjektiv likhet.

Em-rutans underkant ensam räcker inte för att säga att texten korsar en gräns. `matt.ui.black_pixlar` är bläcket.

BG i `forhand` är faktakoll. `bg.kundgodkannande` är false.

Fält och exempel står i `SCHEMA.md`. Diagnosbilderna i `diagnos/` är syntetiska, inte kundannonser.

## Mail-copy v3.3

`fixtures/mail-v3.2.md` är Drive-filen `2026-11-03 2035 - Mail-copy v3.2` (id `1DnFGpBQlsG8lds9Ush-aPQHp-Cz_bH8v`). `mailcopy.py` bygger v3.3 genom att byta versionssidan och lägga in Mail 2 Varm. Övriga avsnitt är samma byte. Den kanoniska kopian för Brevbäraren ligger i Drive-mappen `outbox`, inte som en kundsida på sajten. Handboken aktiveras inte här.
