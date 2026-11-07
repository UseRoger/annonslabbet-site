# Prov i hel scen

Det här är en egen väg för **prov**. Den ligger i git-repot `annonslabbet-site` för att den ska kunna testas och granskas. De verktyg samordnaren redan kör ligger inte här.

Betald leverans är orörd. `render_format.py`, `mat_annons.py`, `spec_v1.json` och `format/F1.html`–`F12.html` finns i Google Drive, mappen `outbox/text-i-kod` (id `1d3pBsrC1-O0pY_vUHk81hZK6u7bej7TE`). De filerna är inte ersatta och inte kopierade in hit. Leveransen är fortfarande 10 motiv i 9:16 och 4:5, med de regler de verktygen redan har.

Provet ritas inte genom att klippa ut produkten och lägga den ovanpå en färdig scen, och inte genom att beskära scenen till en gammal mall. Fotot är hela annonsen. Texten ritas sist, i kod, på den plats JSON anger.

Higgsfield-taket på 100 krediter per dag ligger inte i det här repot och höjs inte här. Verktyget genererar inga bilder.

## Kör

```bash
cd verktyg/prov-helscen
python3 -m pip install -r requirements.txt
python3 -m unittest test_prov_helscen.py test_mail_v33.py -v
python3 render_helscen.py --data diagnos/01-fri-bricka.json --ut /tmp/prov.png
python3 mat_helscen.py --data diagnos/01-fri-bricka.json --bild /tmp/prov.png --json /tmp/prov.mat.json
python3 mat_helscen.py --trio a.png b.png c.png --json /tmp/trio.mat.json
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
