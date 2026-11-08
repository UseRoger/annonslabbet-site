"""Bygg Mail-copy v3.3 från den gällande v3.2-filen.

Bara frontmatter, versionsraden och avsnittet Mail 2 Varm tillkommer.
Mail 1, ordinarie mail 2, mail 3 och övriga brödtexter lämnas orörda.
"""

V33_PARA = (
    "*v3.3 2026-11-07 (INNEHÅLL GODKÄNT, Jon t446u): ett nytt mail, **Mail 2 Varm**, "
    "till butiker Aurora flaggat som varma (stannat 30 s, laddat ner, klickat köp eller "
    "\"Skriv till Jon\"). Det ersätter ordinarie mail 2 för den butiken, aldrig båda, "
    "och går nästa vardagsmorgon, första timmen efter 07:00, minst en natt efter mail 1. Jon 7/11: dagen-efter-mailet ska "
    "ge ett skäl att beställa och visa att de tio motiven byggs runt deras kampanj, "
    "inte bara fråga om de tittat. Grok 7/11: \"exempel\", inte \"antydan\", så demon "
    "inte låter halvfärdig. Allt annat ordagrant v3.2 (mail 1, ordinarie mail 2 dag 3, "
    "mail 3, leveransmail, svarsmallar). Handbokens serveraktivering är separat och "
    "inte gjord här. Inget nytt textligt Kör väntas för innehållet.*"
)

FRONT = """---
typ: copy
datum: 2026-11-07
från: Claude (Fable) på Jons beslut 7/11 (t446u)
till: Brevbäraren (utskicken) + Samordnaren (läser)
status: INNEHÅLL GODKÄNT av Jon 7/11 (t446u). Ersätter v3.2 när handboken är aktiverad på servern. Aktiveringen är separat och inte gjord. Inget nytt textligt Kör väntas för innehållet.
jons_ord: innehåll godkänt t446u (2026-11-07). Handboksaktivering på servern väntar och görs inte av den här filen.
---
"""

WARM = """## Mail 2 Varm (nästa vardagsmorgon, första timmen efter 07:00, minst en natt efter mail 1, samma tråd, bara om inget svar, ersätter ordinarie mail 2 för den butiken)

Hann ni titta? De tre är ett exempel på vad vi kan göra för {{PRODUKT}}.

Beställer ni de tio motiven vill jag veta vad ni planerar i jul (kampanj, rea, julklappstips), så bygger jag dem runt det. Det går fortast om ni svarar här.

Jon

*Regel: `{{PRODUKT}}` som i mail 1. "i jul" byts av Brevbäraren mot aktuell säsong efter 10 januari ("i vår", "inför sommaren"), ett ord, aldrig något annat i texten. Nämn aldrig besöket. Skickas nästa vardagsmorgon, första timmen efter 07:00, minst en natt efter mail 1. Ersätter ordinarie mail 2. Ett mail 2 per butik, aldrig båda. Samma spärrar som ordinarie mail 2.*
"""

H1_GAMMAL = "# Mail-copy v3.2 (Gmail från jon@annonslabbet.se)\n"
H1_NY = "# Mail-copy v3.3 (Gmail från jon@annonslabbet.se)\n"
MAIL3 = "## Mail 3 (dag 7, samma tråd, bara om inget svar)\n"


def bygg_v33(v32: str) -> str:
    if not v32.startswith("---\n"):
        raise ValueError("v3.2 saknar frontmatter")
    slut = v32.find("\n---\n", 3)
    if slut < 0:
        raise ValueError("v3.2 har inget avslutande frontmatter")
    kropp = v32[slut + len("\n---\n"):]
    if H1_GAMMAL not in kropp:
        raise ValueError("hittar inte v3.2-rubriken")
    if MAIL3 not in kropp:
        raise ValueError("hittar inte mail 3")
    kropp = kropp.replace(H1_GAMMAL, H1_NY + "\n" + V33_PARA + "\n\n", 1)
    kropp = kropp.replace(MAIL3, WARM + "\n" + MAIL3, 1)
    return FRONT + kropp


def sektioner(text: str) -> dict:
    """Rubriker som börjar med '## ' och texten fram till nästa sådan rubrik."""
    rader = text.splitlines(keepends=True)
    ut, namn, buff = {}, None, []
    for rad in rader:
        if rad.startswith("## "):
            if namn is not None:
                ut[namn] = "".join(buff)
            namn = rad.split("\n", 1)[0]
            buff = [rad]
        elif namn is not None:
            buff.append(rad)
    if namn is not None:
        ut[namn] = "".join(buff)
    return ut
