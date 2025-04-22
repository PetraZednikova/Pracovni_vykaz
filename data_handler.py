import json
from pathlib import Path
from models import Zamestnanec
from datetime import date
from typing import List


class DataManager:
    @staticmethod
    def nacti_zamestnance(soubor: Path) -> List[Zamestnanec]:
        try:
            # Zkontrolujeme, zda soubor existuje
            if not soubor.exists():
                return []

            # Načteme JSON v UTF-8, aby se správně četla čeština
            with open(soubor, "r", encoding="utf-8") as f:
                data = json.load(f)

            zamestnanci = []
            for z in data:
                # Načtení jednotlivých zaměstnanců
                zam = Zamestnanec(
                    jmeno=z.get("jméno", ""),
                    prijmeni=z.get("příjmení", ""),
                    typ_smlouvy=z.get("typ_smlouvy", ""),
                    hodinova_sazba=z.get("hodinová_sazba", 0.0)
                )

                # Načtení odpracovaných hodin (pokud existují)
                odpracovane = z.get("odpracované_hodiny", {})
                for d, h in odpracovane.items():
                    try:
                        zam.pridej_hodiny(date.fromisoformat(d), h)
                    except ValueError:
                        print(f"Chyba při načítání hodin pro {zam.jmeno} {zam.prijmeni}: Neplatný formát data {d}")

                zamestnanci.append(zam)
            return zamestnanci

        except FileNotFoundError:
            print(f"Soubor {soubor} nebyl nalezen.")
            return []
        except json.JSONDecodeError:
            print("Chyba při čtení JSON souboru. Zkontrolujte, zda je soubor ve správném formátu.")
            return []

    @staticmethod
    def uloz_zamestnance(zamestnanci: List[Zamestnanec], soubor: Path):
        try:
            data = [{
                "jméno": z.jmeno,
                "příjmení": z.prijmeni,
                "typ_smlouvy": z.typ_smlouvy,
                "hodinová_sazba": z.hodinova_sazba,
                "odpracované_hodiny": {d.isoformat(): h for d, h in z.odpracovane_hodiny.items()}
            } for z in zamestnanci]

            # Uložíme JSON v UTF-8 a zajistíme, že se české znaky nezmění na unicode escape
            with open(soubor, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Data byla úspěšně uložena do souboru {soubor}")

        except Exception as e:
            print(f"Chyba při ukládání dat: {e}")
