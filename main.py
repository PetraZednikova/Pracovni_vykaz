# main.py

from datetime import datetime, date
from pathlib import Path
import calendar

from data_handler import DataManager
from calculator import MzdovySystem
from svatky import ceske_statni_svatky
from report_exporter import export_vykaz


def zadej_hodiny_interaktivne(zamestnanec, rok: int, mesic: int, system: MzdovySystem):
    """Interaktivně zadá hodiny pro každý pracovní den."""
    print(f"\nZadávání hodin pro {zamestnanec.jmeno} {zamestnanec.prijmeni} ({zamestnanec.typ_smlouvy})")
    for den in range(1, calendar.monthrange(rok, mesic)[1] + 1):
        datum = date(rok, mesic, den)
        if system.je_pracovni_den(datum):
            while True:
                vstup = input(f"{datum.strftime('%d.%m.%Y')} – hodiny (enter=0): ").strip()
                if not vstup:
                    hod = 0.0
                else:
                    try:
                        hod = float(vstup)
                        if hod < 0:
                            raise ValueError("Záporné číslo")
                    except ValueError:
                        print("  Neplatné číslo, zkuste znovu.")
                        continue
                try:
                    zamestnanec.pridej_hodiny(datum, hod)
                except Exception as e:
                    print(f"  Chyba: {e}")
                    continue
                break


def main():
    # Cesty
    data_dir  = Path("data")
    json_file = data_dir / "employees.json"

    # Načtení zaměstnanců
    zamestnanci = DataManager.nacti_zamestnance(json_file)
    if not zamestnanci:
        print("⚠️ Nebyli nalezeni žádní zaměstnanci.")
        return

    # Volitelné zadání roku a měsíce
    now = datetime.now()
    try:
        r = input(f"Zadej rok (enter = {now.year}): ").strip()
        m = input(f"Zadej měsíc 1–12 (enter = {now.month}): ").strip()
        rok   = int(r) if r else now.year
        mesic = int(m) if m else now.month
        if not (1 <= mesic <= 12):
            raise ValueError("Měsíc mimo 1–12")
    except Exception as e:
        print(f"⚠️ Chyba vstupu: {e}. Používám {now.year}-{now.month}.")
        rok, mesic = now.year, now.month

    # Mzdový systém se státními svátky
    svatky = ceske_statni_svatky(rok)
    system = MzdovySystem(svatky=svatky)

    # Zadávání a export
    for zam in zamestnanci:
        zadej_hodiny_interaktivne(zam, rok, mesic, system)

        # Export do Excelu podle šablony
        template_path = Path("templates") / "template.xlsx"
        out_path      = Path(f"vykaz_{mesic}_{zam.prijmeni}.xlsx")

        # zeptáme se na začátek pracovní doby po zadání hodin
        while True:
            start_time = input("Začátek pracovní doby (8:30 nebo 9:30): ").strip()
            if start_time in ("8:30", "9:30"):
                break
            print("Neplatná volba, zadej 8:30 nebo 9:30.")

        # nyní exportujeme s novým parametrem
        export_vykaz(zam, mesic, rok, template_path, out_path, start_time)



        print(f"✅ Výkaz uložen: {out_path}")

    print("\n🎉 Vše hotovo.")


if __name__ == "__main__":
    main()
