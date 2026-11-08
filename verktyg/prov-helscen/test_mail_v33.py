"""Mail-copy v3.3 får bara lägga till Mail 2 Varm och versionsraden."""

import unittest
from pathlib import Path

from mailcopy import FRONT, WARM, bygg_v33, sektioner

ROOT = Path(__file__).resolve().parent
V32 = (ROOT / "fixtures" / "mail-v3.2.md").read_text(encoding="utf-8")
V33 = (ROOT / "fixtures" / "mail-v3.3.md").read_text(encoding="utf-8")


class MailTest(unittest.TestCase):
    def test_byggs_fran_v32(self):
        self.assertEqual(bygg_v33(V32), V33)

    def test_bara_varm_sektion_tillkommer(self):
        gamla = sektioner(V32)
        nya = sektioner(V33)
        extra = set(nya) - set(gamla)
        self.assertEqual(len(extra), 1)
        rubrik = next(iter(extra))
        self.assertTrue(rubrik.startswith("## Mail 2 Varm"))
        for namn, text in gamla.items():
            self.assertEqual(nya[namn], text, namn)

    def test_kundmeningarna_och_metadatat(self):
        body = WARM
        self.assertIn("De tre är ett exempel på vad vi kan göra för {{PRODUKT}}.", body)
        self.assertNotIn("antydan", body.split("*Regel:")[0])
        self.assertIn("vad ni planerar i jul", body)
        self.assertIn("nästa vardagsmorgon, första timmen efter 07:00, minst en natt efter mail 1", body)
        self.assertNotIn("Varm-raden", body)
        self.assertNotIn("samma dygn", body)
        self.assertIn("Ett mail 2 per butik, aldrig båda", body)
        self.assertIn("Samma spärrar som ordinarie mail 2", body)
        self.assertIn("t446u", FRONT)
        self.assertNotIn("väntar Jons Kör", V33)
        self.assertNotIn("FÖRSLAG", V33)
        self.assertIn("Handbokens serveraktivering är separat", V33)
        self.assertIn("Inget nytt textligt Kör väntas", V33)


if __name__ == "__main__":
    unittest.main()
