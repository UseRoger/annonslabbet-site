---
typ: copy
datum: 2026-11-03 20:35
från: Claude (Opus, kvällschatten med Jon)
till: Brevbäraren (utskicken) + Samordnaren (läser)
status: GÄLLER från nästa mail 1. Ersätter v3.1 i sin helhet.
jons_ord: "Vi tar 1. Skicka till grok om uppdatering" (Jon 2026-11-03 20:34)
---

# Mail-copy v3.2 (Gmail från jon@annonslabbet.se)

*v3.2 2026-11-03 20:35, NY ÄMNESRAD (Jon 20:34): mail 1 heter `Jag gjorde 3 annonser för {{PRODUKT}}` i stället för `3 annonser för {{PRODUKT}}`. Varför: raden ska säga att proven är gratis utan ordet "gratis" (spamord, ny domän). Den som redan gjort jobbet tar inte betalt för det, och raden speglar mailets första mening. Gäller BARA nya mail 1 från och med nu. Trådar som redan är igång (mail 2, mail 3, leveransmail, kundsvar) behåller sin gamla ämnesrad så att svaren hamnar i samma tråd. Ämnesregeln för långa produktnamn och regeln för vanliga ord gäller som förut. Brödtexten och allt annat är ordagrant som i v3.1. Inget A/B-test, alla nya får den nya raden.*


*v3.1 2026-11-01 04:45, GARANTIN OMLÅST (Jon 04:29): receptet är villkoret. "Kör de 13 annonserna som en egen kampanj, 500 kr om dagen i sju dagar, mot er vanliga målgrupp. Får ni inte en annons till som säljer lika bra som er bästa i dag, visa oss siffrorna så får ni pengarna tillbaka. Säg till inom 30 dagar från leveransen." Ingen jämförelse "bättre än", inget bild mot bild, inget video mot video (Pro/video säljs inte just nu, Jon 04:03). Ändrat: mail 1 (garantibiten: "pengarna tillbaka om ni inte får en vinnare till"), leveransmailets garantistycke, svarsmallen Garanti, svarsmallen Video. Pro-varianten av leveransmailet står kvar för kunder som redan köpt Pro, används inte för nya. Allt annat ordagrant v3.0.*


*v3.0 2026-10-31 22:15, ERBJUDANDET 3.0 (Jons beslut i kväll): mail 1 tillbaka till en mening om paketet, allt annat flyttar till provsidan. Ramen är ny överallt: vi hjälper butiken se vilken vinkel som säljer bäst för dem, 10 motiv i **beprövade vinklar** (vinklar som redan säljer för andra butiker, i Norden och resten av världen), garantin säger **"säljer bättre än er bästa annons i dag"** i stället för "slår" (tävlingsspråk bort, villkoren oförändrade). Ändrat: mail 1 (texten), mail 3 (sista raden), svarsmallen Intresserad (två ord + ändringsraden). Allt annat ordagrant v2.9. Samma ram på provsidan (mall v3.0), startsidan, Stripe-texterna och Aurora-korten, se kontraktet 2230.*

*v2.9 2026-10-30 18:10: (1) slottarna och "max 5 per dag" borta. Mail 1 går när Auroras ångra-tid är ute (outbox 1715), max 10 per dag (outbox 2115), bara vardagar 07:00-21:00 (outbox 2100), inget minsta avstånd (outbox 2135). Samma som Brevbärarens handbok v3. (2) **Ämnesregel för långa produktnamn:** ta bort storlek, ålder och variant efter kommatecken. Är namnet fortfarande längre än fyra ord, skriv butik + produkt i bestämd form. Exempel (Jons ja 17:45): "3 annonser för TeddyPosts badrock med namn". Mailtexterna är ordagrant v2.8.*

*v2.8 2026-10-30 13:40 (Jon 13:35, GODKÄNN R6 + R10): Starter levereras i **9:16 och 4:5** (inte 1:1), eftersom 4:5 tar mer plats i flödet och mallarna gör det utan extra kostnad. Mail 1 säger "10 motiv till i samma **formspråk**" (inte "stil"), eftersom de tre proven nu har tre olika mallar: typsnitt och färger är butikens i alla, layouten skiljer. Ändrat i mail 1, leveransmailet och Pro-varianten. Kunder som redan fått 1:1 (Sauna Ice) berörs inte. Allt annat ordagrant som v2.7.*

*v2.7 2026-10-28 16:40 (flödesöversynen, Jon "kör" 16:08): SKICKREGELN. Mail 1, 2 och 3 (säljmailen) skickar Brevbäraren själv, direkt, utan utkast: ok:et för mail 1 är Jons FÄRDIG + "Skicka till kund" i Aurora. Allt annat till kund (leveransmail, ändringsmail, avslagssvar, Vårt fel-kvittens, Vårt fel-klart, dag 8, recensionsmail, kundsvar) läggs som Gmail-utkast i jon@annonslabbet.se och Jon trycker Skicka; raden "Utkast i Gmail: <mail> (<butik>)" går till #jon-agera. Mail 1 gick i v2.7 i fasta slottar (borta sedan 29/10, se v2.9 ovan), bara om provsidan svarar 200 och visar butiksnamnet, bara till adressen från butikens egen sajt. Mail 2/3 bara efter koll i ledger + Gmail att inget svar, köp eller studs finns. Inga mail 1-3 på helg; utkast för leverans och kundsvar läggs även helg. Texterna nedan är ordagrant v2.6.*

*v2.6 2026-10-27 (byggare H, "Vårt fel"): Vårt fel-kvittens (när Jon valt Vårt fel på kundkortet) och Vårt fel-klart (när omgången med rättelsen levererats), ändringsmailet gäller varje omgång 2, 3, 4 ... Allt annat ordagrant som v2.5.*

*v2.5 rev 16:50: driftsraden i leveransmailet ersatt av intresseanmälan (Jon), kopia till betalarens Stripe-adress när den skiljer sig från tråden. v2.5 rev 13:00 (Samordnarens kvitto 1245, fyra punkter): leveransordningen Samordnaren → "Leverans klar" → Brevbäraren, Pro-variant, variant utan prov, "inom 30 dagar från leveransdatumeten" i mail 1 (provsidans rad byts av Samordnaren till samma lydelse i nästa pass). v2.5 2026-10-26 12:45: mail 1 får den omlåsta garantin (30 dagar) + paketet som 10 motiv i 2 format, mail 3 säger "10 motiv till", leveransmailet säger 23 bilder (de 3 gratisproven följer med, rev D) och går med BCC till Trustpilot (`annonslabbet.se+ddbd347171@invite.trustpilot.com`, bara leverans- och ändringsmail). Allt annat ordagrant som v2.4. Brevbäraren äger utskicken från "Brevbäraren är igång".*

*v2.4 2026-10-25 17:00: leveransmailet skrivet för Leveranssidan 2.0 (två steg på sidan: Godkänn och ladda ner / Ändra), "5 ändringar ingår, fler kostar 100 kr per bild" överallt där ändringar nämns, leveransmailet går DIREKT vid Jons Leverera i Aurora (inte som utkast, GODKÄNN 5), nytt ändringsmail + avslagssvar. Mail 1-3 ordagrant som v2.3.*

*v2.3 2026-10-24 16:50: garantiraden i mail 1 enligt den låsta garantin, takten 5 per dag, leveransmail v1 med driftsraden. v2.2: ämnesregel för vaga produktnamn, slug + mail i länkar, godkännande = Aurora. v2.1: avregistreringsrad i mail 1 och 3. Texterna är godkända av Jon. Vill du testa en annan text: föreslå i inbox/ med motivering, byt inte själv.*

Skickas från Gmail, en i taget, som vanlig mail (inga mallverktyg, ingen HTML, ingen signaturbild, ingen spårningspixel). **Mail 1: går när Auroras ångra-tid är ute, max 10 per dag, vardagar 07:00-21:00, Brevbäraren skickar själv.** Mail 2 och 3 i 09:00-passet, vardagar. Aldrig fler än tre mail till samma butik, aldrig på helg. Ämnesraden är densamma i alla tre (svar hamnar i samma tråd).

Variabler: `{{PRODUKT}}` (produktens namn som butiken själv kallar den), `{{PROV_URL}}`, `{{LEVERANS_URL}}` (= `https://annonslabbet.se/<slug>/leverans/`).

## Mail 1 (dag 0)

Ämne: `Jag gjorde 3 annonser för {{PRODUKT}}`. Är produktnamnet ett vanligt ord (Jullåda, Presentask, Kalender): `Jag gjorde 3 annonser för {{BUTIK}}s {{produkt i bestämd form}}`, t.ex. "Jag gjorde 3 annonser för Chokladhusets jullåda", "Jag gjorde 3 annonser för Sauna Ice-presentasken". Långa produktnamn: samma regel som v2.9, t.ex. "Jag gjorde 3 annonser för TeddyPosts badrock med namn". Trådar som startades före v3.2 behåller `3 annonser för ...`.

Jag gjorde tre annonser för {{PRODUKT}}. Ni får dem gratis, oavsett vad ni tycker:

{{PROV_URL}}

Gillar ni dem inte behöver ni aldrig svara. Gillar ni dem gör vi 10 motiv till i beprövade vinklar (20 annonser), 1 990 kr ex moms, pengarna tillbaka om ni inte får en vinnare till.

Hur det går till står på er sida ovan.

Jon
Annonslabbet, Åre

Vill ni inte ha fler mail från mig: svara nej, så hör jag inte av mig igen.

## Mail 2 (dag 3, svar i samma tråd, bara om inget svar)

Hann ni titta? Nyfiken på en sak: gör ni annonserna själva idag, eller har ni någon som hjälper er?

Jon

## Mail 3 (dag 7, samma tråd, bara om inget svar)

Sista mailet från mig. Provet ligger kvar här om ni vill använda det, det är ert:

{{PROV_URL}}

Vill ni prova nya vinklar på {{PRODUKT}} någon gång är det bara att svara.

Jon

Svara nej så hör jag inte av mig igen.

## Leveransmail (v2, när Jon tryckt Leverera i Aurora)

Svar i samma tråd som mail 1. Ämne: `Re: ` + mail 1:s ämnesrad, exakt som den gick (`Re: Jag gjorde 3 annonser för {{PRODUKT}}` från v3.2, `Re: 3 annonser för {{PRODUKT}}` för äldre trådar). Kopia (Cc) till adressen kunden betalade från i Stripe om den skiljer sig från trådens. **BCC: `annonslabbet.se+ddbd347171@invite.trustpilot.com`** (Trustpilot skickar sin inbjudan efter 7 dagar; BCC bara på leverans- och ändringsmail, aldrig mail 1-3 eller svar). **Gmail-utkast, Jon trycker Skicka (v2.7). Ordningen: Samordnaren bygger sidan + zip, kontrollerar 200, skriver lev-kortet och raden "Leverans klar <slug>" i #grok-bot. Brevbäraren väcks av den raden, lägger utkastet inom minuter, aldrig före raden, och skriver "Utkast i Gmail: leveransmail (<butik>)" i #jon-agera.** Efter att Jon skickat: `levererad_datum`, `status` = delivered, `trustpilot_bcc` i ledgern.

Tack för beställningen! Här kommer de 23 bilderna för {{PRODUKT}}: 10 motiv i 9:16 och 4:5, plus de 3 ni fick gratis på prov:

{{LEVERANS_URL}}

Titta igenom dem där. Är ni nöjda trycker ni på Godkänn och ladda ner, så får ni alla filer direkt, en och en eller som zip. Vill ni ändra något trycker ni på Ändra och skriver vad under bilden. 5 ändringar ingår, fler kostar 100 kr per bild.

Garantin gäller som sagt: kör de 13 annonserna som en egen kampanj, 500 kr om dagen i sju dagar, mot er vanliga målgrupp. Får ni inte en annons till som säljer lika bra som er bästa i dag, visa mig siffrorna så får ni pengarna tillbaka. Säg till inom 30 dagar från leveransen.

En fråga bara: skulle ni vilja att någon även körde annonserna åt er i Meta, med budget och allt? Vi tar inte sådana uppdrag än, men vi vill veta vilka som skulle vilja. Ett "ja" i svaret räcker.

Jon
Annonslabbet, Åre

Varianter: **Pro-kund:** första meningen blir "Här kommer de 23 bilderna för {{PRODUKT}}: 10 motiv i 9:16 och 4:5, plus de 3 ni fick gratis på prov, och de tre videorna:". **Kund utan provbilder** (ingen provsida): "Här kommer de 20 bilderna för {{PRODUKT}}: 10 motiv i 9:16 och 4:5:".

Regler: intresseraden om drift finns BARA här, aldrig i mail 1-3 eller på sidorna (Jon 26/10 16:46, ersätter driftsraden). Svarar kunden "ja": logga `drift_intresse` = datum i ledgern + rad i #grok-bot, svara "Noterat, vi hör av oss när vi öppnar för det." Inget pris, inga löften. Pro-kunder: "20 annonser" blir "20 annonser och tre videos".

## Ändringsmail (när Jon tryckt Leverera igen efter kundens ändringar, delivery_round 2 eller högre)

Samma tråd. Gmail-utkast, Jon trycker Skicka, rad i #jon-agera (v2.7). Har omgången Vårt fel-bilder (kund.json `var_fel` inte tom): skicka **Vårt fel-klart** nedan i stället, aldrig båda.

Era ändringar är klara, samma sida som förut:

{{LEVERANS_URL}}

De ändrade annonserna är markerade. Tryck på Godkänn och ladda ner så har ni de nya filerna.

Jon

## Avslagssvar (när Jon avslagit en eller flera av kundens ändringar i Aurora, kommentaren börjar med AVSLAGEN:)

Samma tråd, Gmail-utkast som ändringsmailet, skickas tillsammans med ändringsmailet om något annat byggdes om, annars för sig. Jons skäl ordagrant efter AVSLAGEN:, ett stycke per bild:

Motiv {{N}}: {{Jons skäl}}

Resten är ändrat enligt era anteckningar. Säg till om ni vill att jag tittar en gång till.

Jon

## Vårt fel-kvittens (när Jon valt Vårt fel på kundkortet, väckraden säger "varav N Vårt fel")

Samma tråd som kundens ändringar. **Gmail-utkast, Jon trycker Skicka, rad i #jon-agera** (v2.7), signaturblocket sist (outbox 1746). Inga tekniska ord (motiv, varv, nycklar, omgång). `{{FELET}}` = Jons Vårt fel-kommentar i kundens ord (en kort bisats, "påsen blev för stor"), `{{ANTAL}}` = antalet Vårt fel-bilder, `{{DAG}}` = veckodag + datum då sidan är klar (senast 48 h efter Jons beslut, Samordnaren säger dagen). Tre varianter, välj en:

**A. Jon tog på oss fler bilder än kunden pekade på:**

Tack för att du sa till, du har helt rätt: {{FELET}}, och det är vårt fel. Vi rättar det på alla {{ANTAL}} bilder där det syns, inte bara de du pekade på.

Det räknas inte mot dina 5 ändringar, de har du kvar. Du får ett mail när sidan är uppdaterad, senast {{DAG}}.

Jon

**B. Bara kundens egna bilder var vårt fel:**

Tack för att du sa till, du har helt rätt: {{FELET}}, och det är vårt fel. Vi rättar det, och det räknas inte mot dina 5 ändringar.

Du får ett mail när sidan är uppdaterad, senast {{DAG}}.

Jon

**C. Blandat (några var vårt fel, några var kundens önskemål):** variant A eller B, plus en mening sist före Jon: "Det andra du bad om gör vi samtidigt, det räknas som vanligt." Avslag skrivs som Avslagssvar i samma mail, ett stycke per bild.

**Återbetalning** (kortet säger "Återbetala N × 100 kr"): lägg till "Du betalade för {{N}} extra, de pengarna får du tillbaka i dagarna." Skicka aldrig den raden innan Jon sagt i #grok-bot att återbetalningen är gjord eller beslutad.

## Vårt fel-klart (när Jon tryckt Leverera för omgången med rättelsen)

Samma tråd. Gmail-utkast, Jon trycker Skicka, rad i #jon-agera (v2.7). Ersätter ändringsmailet för den här omgången. BCC Trustpilot som ändringsmailet.

Nu är det rättat, samma sida som förut:

{{LEVERANS_URL}}

Bilderna vi rättat är markerade. Tryck på Godkänn och ladda ner så har ni de nya filerna. Rättelsen räknas inte mot era ändringar, {{KVAR_RAD}}. Och tack igen för att ni sa till, det gjorde annonserna bättre.

Jon

`{{KVAR_RAD}}` ur kund.json `andringar_kvar`: 5 = "alla 5 har ni kvar", 1-4 = "{{andringar_kvar}} av de 5 har ni kvar", 0 = "de 5 som ingick är använda sedan tidigare". Inga tekniska ord.

## Svarsmallar (ur FAQ-filen, kortversioner)

Intresserad: "Kul! Här är länken för 10 motiv i beprövade vinklar, 20 annonser (1 990 kr ex moms): https://buy.stripe.com/3cI5kC0Zafp25VGdZlc3m00?client_reference_id=<slug>&prefilled_email=<mail>. När betalningen är inne har ni dem inom 48 timmar. 5 ändringar ingår, vill ni ändra mer kostar det 100 kr per bild."
Video (Pro säljs inte just nu, Jon 1/11): "Inte just nu, vi återkommer när vi öppnar för det." + rad i #jon-agera.
Garanti (om kunden frågar): "Kör de 13 annonserna som en egen kampanj, 500 kr om dagen i sju dagar, mot er vanliga målgrupp. Får ni inte en annons till som säljer lika bra som er bästa i dag, visa oss siffrorna så får ni pengarna tillbaka. Säg till inom 30 dagar från leveransen."
Ändringar (om kunden frågar innan leverans): "5 ändringar ingår. Vill ni ändra fler kostar det 100 kr per bild, ni ser det direkt på leveranssidan."
Ringa/ses: "Absolut, Jon hör av sig idag." (Slack till Jon.)
Nej: "Tack för att ni svarade. Provet är ert, använd det gärna."

## Regler
- Inga tankstreck. Ingen "Hej [Namn]". Inga bilagor (länken räcker, bilagor sänker leveransen).
- Ingen rad om var vi hittade butiken.
- Godkännande sker i Aurora, inte i Slack. **Skickregeln (v2.7):** mail 1 går när Jon tryckt "Skicka till kund" på provkortet, mail 2 och 3 går automatiskt efter spärrkollen, Brevbäraren skickar alla tre själv. Allt annat till kund är Gmail-utkast som Jon trycker Skicka på, raden i #jon-agera. Kundsvar: utkastet skrivs i Gmail (inte i Slack), svarsmallarna ovan är texterna.
- "nej", "sluta", "ta bort" = förlorad, inga fler mail. Två studsar samma dag = stoppa dagens utskick.
