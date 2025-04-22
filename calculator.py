from datetime import date
import calendar
from typing import List


class MzdovySystem:
    def __init__(self, svatky: List[date]):
        self.svatky = svatky

    def vypocet_mzdy(self, zamestnanec, mesic: int, rok: int = None) -> dict:
        """Spočítá mzdu pro zaměstnance za zvolený měsíc a rok."""
        hodiny_mesic = 0.0
        for datum, hodiny in zamestnanec.odpracovane_hodiny.items():
            if datum.month == mesic and (rok is None or datum.year == rok) and self.je_pracovni_den(datum):
                hodiny_mesic += hodiny

        return {
            "jmeno": f"{zamestnanec.jmeno} {zamestnanec.prijmeni}",
            "sazba": zamestnanec.hodinova_sazba,
            "hodin": round(hodiny_mesic, 2),
            "mzda": round(hodiny_mesic * zamestnanec.hodinova_sazba, 2)
        }

    def je_pracovni_den(self, datum: date) -> bool:
        return datum.weekday() < 5 and datum not in self.svatky


class VyplatniPaska:
    def __init__(self, zamestnanci: List, svatky: List[date]):
        self.zamestnanci = zamestnanci
        self.svatky = svatky

    def je_pracovni_den(self, datum: date) -> bool:
        return datum.weekday() < 5 and datum not in self.svatky

    def _vygeneruj_pracovni_dny(self, mesic: int, rok: int) -> List[date]:
        """Vrací seznam pracovních dní daného měsíce a roku (bez svátků)."""
        return [
            date(rok, mesic, den)
            for den in range(1, calendar.monthrange(rok, mesic)[1] + 1)
            if self.je_pracovni_den(date(rok, mesic, den))
        ]

    def generuj_vykazy(self, mesic: int, rok: int) -> dict:
        """Vrací přehled odpracovaných hodin a výpočtu mezd za daný měsíc."""
        report = {}
        for zam in self.zamestnanci:
            hodiny_mesic = sum(
                h for d, h in zam.odpracovane_hodiny.items()
                if d.month == mesic and d.year == rok and self.je_pracovni_den(d)
            )
            report[f"{zam.jmeno} {zam.prijmeni}"] = {
                "sazba": zam.hodinova_sazba,
                "hodiny": round(hodiny_mesic, 2),
                "mzda": round(hodiny_mesic * zam.hodinova_sazba, 2)
            }
        return report
