#!/usr/bin/env python3
"""Kontrollera jobbets egen kostnadsrad. Hittar inte på ett pris.

    python3 jobbmanifest.py --json jobb.json

jobb.json:
    {"job_id": "…", "kostnad": 2.75, "kostnad_kalla": "higgsfield.job.kostnad", "credits": 2.75}

Saknas kostnaden i svaret: "kostnad": "ej tillgänglig", utan kostnad_kalla.
Ett tal utan källa godkänns inte. Saldoskillnad används inte.
"""

import argparse
import json
import sys
from pathlib import Path

from mat_helscen import las_jobb


def main():
    parser = argparse.ArgumentParser(description="Kvitto på job_id och kostnad från jobbets eget svar.")
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.json).read_text(encoding="utf-8"))
    if "jobb" not in data and "job_id" in data:
        data = {"jobb": data}
    resultat = las_jobb(data)
    sys.stdout.write(json.dumps(resultat, ensure_ascii=False) + "\n")
    return 0 if resultat["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
