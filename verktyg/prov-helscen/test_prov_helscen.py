"""Prov i hel scen: rå mätning kvar, mallregler är anmärkningar, bläcket avgör UI."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

import gemensamt
import mat_helscen
import policy
from gemensamt import Fel, exact_crop, rita_block

ROOT = Path(__file__).resolve().parent


def _uppdrag():
    return {
        "fakta": ["Badrock med namnbrodyr", "449 kr"],
        "kopskal": "Första julen med eget namn",
        "vinkel": "Present, inte en produkt på vitt",
        "vinnare": "Presentvinkel som redan säljer hos andra butiker, bara som referens",
        "fotoide": "Barn i badrock på trägolv, lugn yta för rubriken",
    }


def _forhand():
    return {
        "kalla": "BG",
        "produkt_stammer": True,
        "pris_stammer": True,
        "pastaenden_stammer": True,
        "anatomi_ok": True,
        "montering_ok": True,
        "ai_person_vid_omdome": False,
    }


def _data(bild, texter, **extra):
    data = {
        "vag": "prov-helscen",
        "workflow": "prov",
        "bild": bild,
        "format": "9x16",
        "uppdrag": _uppdrag(),
        "forhand": _forhand(),
        "texter": texter,
    }
    data.update(extra)
    return data


def _scen(path, farg=(26, 42, 34, 255), storlek=(1080, 1920)):
    bild = Image.new("RGBA", storlek, farg)
    ImageDraw.Draw(bild).ellipse((360, 700, 760, 1280), fill=(214, 186, 140, 255))
    bild.save(path)
    return path


class PolicyTest(unittest.TestCase):
    def test_leverans_behaller_z3_och_k3(self):
        traffar = [
            {"id": "Z3", "text": "bricka utanför zonen"},
            {"id": "K3", "text": "kontrast 2.1"},
        ]
        lev = policy.klassificera(traffar, "leverans")
        prov = policy.klassificera(traffar, "prov")
        self.assertEqual(lev["resultat_raw"], "nej")
        self.assertEqual(lev["resultat"], "nej")
        self.assertIn("Z3", lev["brott"][0])
        self.assertTrue(any(rad.startswith("K3") for rad in lev["brott"]))
        self.assertEqual(prov["resultat_raw"], "nej")
        self.assertEqual(prov["resultat"], "nej")
        self.assertTrue(all(not rad.startswith("Z3") for rad in prov["brott"]))
        self.assertTrue(any(rad.startswith("Z3") for rad in prov["anmarkningar"]))
        self.assertTrue(any(rad.startswith("K3") for rad in prov["brott"]))
        self.assertTrue(prov["raw_ar_inte_omskriven"])

    def test_t1_ar_anmarkning_t2_ar_stopp(self):
        bara_t1 = policy.klassificera([{"id": "T1", "text": "72 px"}], "prov")
        self.assertEqual(bara_t1["resultat_raw"], "nej")
        self.assertEqual(bara_t1["resultat_prov"], "ja")
        self.assertEqual(bara_t1["resultat_leverans"], "nej")
        las = policy.klassificera([{"id": "LASBAR", "text": "synlig höjd 30 px"}], "prov")
        self.assertEqual(las["resultat_prov"], "nej")
        self.assertEqual(policy.klassificera([{"id": "LASBAR", "text": "30 px"}], "leverans")["resultat"], "nej")
        gammal_t2 = policy.klassificera([{"id": "T2", "text": "36 px-regeln"}], "prov")
        self.assertEqual(gammal_t2["resultat_prov"], "ja")

    def test_t1_stangs_inte_av_i_bulk(self):
        self.assertIn("LASBAR", policy.ALLTID_STOPP)
        self.assertIn("K3", policy.ALLTID_STOPP)
        self.assertNotIn("K3", policy.PROV_ANMARKNING)
        self.assertIn("T1", policy.PROV_ANMARKNING)
        self.assertIn("T2", policy.PROV_ANMARKNING)
        self.assertIn("B2", policy.PROV_ANMARKNING)


class RenderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.scen = _scen(self.dir / "scen.png")

    def tearDown(self):
        self.tmp.cleanup()

    def _mat(self, data, bild=None, workflow="prov"):
        path = self.dir / "annons.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return mat_helscen.rapport(data, str(self.dir), None if bild is None else str(bild), workflow)

    def test_klistrar_inte_produkt_och_behaller_matt(self):
        rod = self.dir / "produkt.png"
        Image.new("RGBA", (400, 400), (220, 0, 0, 255)).save(rod)
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72},
        ], produkt_png=str(rod))
        rapport, render = self._mat(data)
        self.assertEqual(render["bild"].size, (1080, 1920))
        self.assertEqual(render["scen"].size, (1080, 1920))
        # Mitten av den ritade produkten i scenen ska vara oförändrad.
        self.assertEqual(render["bild"].getpixel((560, 900))[:3], render["scen"].getpixel((560, 900))[:3])
        self.assertEqual(rapport["matt"]["produkt_urklipp"], "hoppades_over")
        self.assertFalse(rapport["matt"]["beskuren"])
        self.assertIn("produkt_png ignoreras", " ".join(rapport["matt"]["info"]))

    def test_forma_om_och_fel_proportion_beskars_inte(self):
        fyrkant = self.dir / "fyrkant.png"
        Image.new("RGBA", (640, 640), (20, 20, 20, 255)).save(fyrkant)
        data = _data("fyrkant.png", [
            {"roll": "rubrik", "text": "Kort rubrik", "x": 80, "y": 80, "px": 48},
        ])
        with self.assertRaises(Fel):
            gemensamt.rendera({**data, "forma_om": True}, str(self.dir))
        rapport, render = self._mat(data)
        self.assertEqual(render["bild"].size, (640, 640))
        self.assertTrue(any(t["id"] == "ZONER_SAKNAS" for t in rapport["traffar"]))
        self.assertEqual(rapport["resultat_prov"], "nej")

    def test_fri_bricka_ar_lasbar_och_rav_stopp_star_kvar(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72},
            {"roll": "pris", "text": "449 kr", "x": 180, "y": 780, "px": 64, "farg": "#ffffff", "bricka_farg": "#1d3a2a"},
        ])
        rapport, _render = self._mat(data)
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertIn("Z3", ids)
        self.assertIn("T1", ids)
        self.assertNotIn("UI", ids)
        self.assertNotIn("K3", ids)
        self.assertNotIn("LASBAR", ids)
        self.assertNotIn("T2", ids)
        self.assertNotIn("B2", ids)
        self.assertIn("BG_SAKNAS", ids)
        self.assertEqual(rapport["resultat_raw"], "nej")
        self.assertEqual(rapport["resultat"], "nej")
        self.assertEqual(rapport["bg"]["status"], "ej_gjord")
        self.assertFalse(rapport["jon_martin_ok"])
        self.assertFalse(rapport["bg"]["kundgodkannande"])
        self.assertTrue(rapport["gamla_mallregler_stoppar_inte"])
        self.assertFalse(rapport["gamla_verktyget_andrat"])
        bricka = next(b for b in rapport["matt"]["block"] if b["roll"] == "pris")
        self.assertGreater(bricka["kontrast"], 4.5)
        self.assertLess(bricka["synligt_black"][1], 1150)

    def test_linebox_utan_black_ar_inte_ui_stopp(self):
        matt = rita_block({"text": "HALLO", "px": 80, "roll": "rubrik"}, {}, str(self.dir))
        ink_botten = matt["black_lokal"][3]
        em_botten = matt["linebox_lokal"][3]
        self.assertLess(ink_botten, em_botten)
        grans = 1580
        y = grans - (ink_botten + em_botten) / 2
        self.assertLess(y + ink_botten, grans)
        self.assertGreaterEqual(y + em_botten, grans)
        # Platt mörk scen, så kontrasten inte beror på var produkten sitter.
        Image.new("RGBA", (1080, 1920), (26, 42, 34, 255)).save(self.dir / "platt.png")
        data = _data("platt.png", [
            {"roll": "rubrik", "text": "HALLO", "x": 200, "y": y, "px": 80, "farg": "#ffffff"},
        ])
        rapport, _render = self._mat(data)
        block = rapport["matt"]["block"][0]
        self.assertLess(block["black_botten"], grans)
        self.assertGreaterEqual(block["linebox_botten"], grans)
        self.assertEqual(rapport["matt"]["ui"]["black_pixlar"], 0)
        self.assertTrue(rapport["matt"]["ui"]["linebox_korsar"])
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertNotIn("UI", ids)
        self.assertIn("BG_SAKNAS", ids)
        self.assertEqual(rapport["resultat"], "nej")
        self.assertFalse(rapport["jon_martin_ok"])
        text = " ".join(rapport["hur_allvar_harleds"])
        self.assertIn("bläck", text.lower())

    def test_synligt_black_i_reels_ar_stopp(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn", "x": 200, "y": 1600, "px": 72, "farg": "#ffffff"},
        ])
        rapport, _render = self._mat(data)
        self.assertIn("UI", {t["id"] for t in rapport["traffar"]})
        self.assertGreater(rapport["matt"]["ui"]["black_pixlar"], 0)
        self.assertEqual(rapport["resultat_prov"], "nej")
        self.assertEqual(rapport["resultat_raw"], "nej")
        self.assertEqual(rapport["resultat"], "nej")

    def test_svag_kontrast_ar_stopp_i_prov(self):
        ljus = _scen(self.dir / "ljus.png", (250, 250, 250, 255))
        data = _data("ljus.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72, "farg": "#ffffff"},
        ])
        rapport, _render = self._mat(data)
        self.assertIn("K3", {t["id"] for t in rapport["traffar"]})
        self.assertEqual(rapport["resultat_prov"], "nej")
        self.assertTrue(ljus.exists())

    def test_hittat_pris_stopp_och_bg_saknas(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72},
            {"roll": "pris", "text": "999 kr", "x": 180, "y": 780, "px": 42},
        ])
        data["forhand"] = {}
        rapport, _render = self._mat(data)
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertIn("FAKTA", ids)
        self.assertIn("BG_SAKNAS", ids)
        self.assertEqual(rapport["resultat_prov"], "nej")
        self.assertFalse(rapport["bg"]["kundgodkannande"])

    def test_anatomi_och_ai_person(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72},
        ])
        data["bg"] = {
            "granskad": True,
            "granskare": "Bildgranskaren",
            "produkt": "ja",
            "pastaenden": "ja",
            "anatomi": "nej",
            "montering": "ja",
            "ai_person_vid_omdome": True,
        }
        rapport, _render = self._mat(data)
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertIn("ANATOMI", ids)
        self.assertIn("AI_PERSON", ids)
        self.assertEqual(rapport["resultat_prov"], "nej")

    def test_scen_som_andrats_utanfor_texten(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72},
        ])
        _rapport, render = self._mat(data)
        fejk = render["bild"].copy()
        ImageDraw.Draw(fejk).rectangle((100, 900, 500, 1300), fill=(255, 0, 0, 255))
        fejk_path = self.dir / "fejk.png"
        fejk.convert("RGB").save(fejk_path)
        rapport, _render = self._mat(data, bild=fejk_path)
        self.assertIn("SCEN_ANDRAD", {t["id"] for t in rapport["traffar"]})
        self.assertEqual(rapport["resultat_prov"], "nej")

    def test_trio_dubblett_crop_och_olika(self):
        a = Image.new("RGB", (80, 60), (10, 20, 30))
        ImageDraw.Draw(a).rectangle((10, 10, 40, 40), fill=(200, 180, 40))
        b = a.copy()
        c = a.crop((5, 5, 70, 50))
        d = Image.new("RGB", (80, 60), (80, 10, 10))
        ImageDraw.Draw(d).ellipse((8, 8, 60, 50), fill=(240, 220, 200))
        pa, pb, pc, pd = [self.dir / n for n in ("a.png", "b.png", "c.png", "d.png")]
        a.save(pa)
        b.save(pb)
        c.save(pc)
        d.save(pd)
        self.assertTrue(exact_crop(c, a))
        samma = mat_helscen.mat_trio([pa, pb, pd])
        self.assertFalse(samma["tre_nya_foton"])
        self.assertEqual(samma["resultat"], "nej")
        self.assertEqual(samma["resultat_raw"], "nej")
        crop = mat_helscen.mat_trio([pa, pc, pd])
        self.assertFalse(crop["tre_nya_foton"])
        self.assertTrue(any(p["slag"] == "crop" for p in crop["par"]))
        pe = self.dir / "e.png"
        Image.new("RGB", (90, 70), (0, 40, 90)).save(pe)
        olika = mat_helscen.mat_trio([pa, pd, pe])
        self.assertTrue(olika["tre_nya_foton"])
        self.assertEqual(olika["resultat"], "ja")
        self.assertTrue(any(rad.startswith("LIKHET") for rad in olika["anmarkningsrader"]))
        self.assertFalse(any(p["slag"] != "olika" for p in olika["par"]))

    def test_gammal_reelsgrans_1248_stoppar_inte(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn", "x": 200, "y": 1400, "px": 72, "farg": "#ffffff"},
        ])
        rapport, _render = self._mat(data)
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertNotIn("UI", ids)
        block = rapport["matt"]["block"][0]
        self.assertGreater(block["black_botten"], 1248)
        self.assertLess(block["black_botten"], 1580)

    def test_synlig_hojd_under_38_stoppar_36_px_regeln_gor_det_inte(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Liten", "x": 200, "y": 400, "px": 28, "farg": "#ffffff"},
        ])
        rapport, _render = self._mat(data)
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertIn("LASBAR", ids)
        self.assertNotIn("T2", ids)
        self.assertNotIn("B2", ids)
        self.assertLess(rapport["matt"]["block"][0]["synlig_hojd"], 38)
        self.assertIn("38", rapport["matt"]["zon"]["synlig_kalla"])

    def test_bg_ja_ar_inte_jon_ok(self):
        data = _data("scen.png", [
            {"roll": "rubrik", "text": "Eget namn i jul", "x": 160, "y": 340, "px": 72, "farg": "#ffffff"},
            {"roll": "pris", "text": "449 kr", "x": 180, "y": 780, "px": 64, "farg": "#ffffff", "bricka_farg": "#1d3a2a"},
        ])
        data["bg"] = {
            "granskad": True,
            "granskare": "Bildgranskaren",
            "produkt": "ja",
            "pastaenden": "ja",
            "anatomi": "ja",
            "montering": "ja",
            "ai_person_vid_omdome": False,
        }
        rapport, _render = self._mat(data)
        ids = {t["id"] for t in rapport["traffar"]}
        self.assertNotIn("BG_SAKNAS", ids)
        self.assertNotIn("UI", ids)
        self.assertNotIn("LASBAR", ids)
        self.assertFalse(rapport["jon_martin_ok"])
        self.assertFalse(rapport["bg"]["kundgodkannande"])


class DiagnosTest(unittest.TestCase):
    def test_diagnos_filer(self):
        import skriv_diagnos
        ut = ROOT / "diagnos"
        if ut.exists():
            shutil.rmtree(ut)
        skriv_diagnos.skriv(ut)
        matt = json.loads((ut / "01-meter-ren-ej-faktagranskad.mat.json").read_text(encoding="utf-8"))
        self.assertNotIn("UI", {t["id"] for t in matt["traffar"]})
        self.assertNotIn("LASBAR", {t["id"] for t in matt["traffar"]})
        self.assertEqual(matt["bg"]["status"], "ej_gjord")
        self.assertEqual(matt["resultat"], "nej")
        self.assertFalse(matt["jon_martin_ok"])
        self.assertTrue(matt["matt"]["export_9x16"])
        self.assertTrue((ut / "01-meter-ren-ej-faktagranskad.png").exists())
        line = json.loads((ut / "02-linebox.mat.json").read_text(encoding="utf-8"))
        self.assertEqual(line["matt"]["ui"]["black_pixlar"], 0)
        self.assertTrue(line["matt"]["ui"]["linebox_korsar"])
        self.assertNotIn("UI", {t["id"] for t in line["traffar"]})
        krock = json.loads((ut / "03-ui-krock.mat.json").read_text(encoding="utf-8"))
        self.assertEqual(krock["resultat"], "nej")
        self.assertIn("UI", {t["id"] for t in krock["traffar"]})
        self.assertGreater(krock["matt"]["ui"]["black_pixlar"], 0)
        trio = json.loads((ut / "trio.mat.json").read_text(encoding="utf-8"))
        self.assertTrue(trio["tre_nya_foton"])


if __name__ == "__main__":
    unittest.main()
