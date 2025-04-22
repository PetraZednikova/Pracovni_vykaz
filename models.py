from datetime import date
from typing import Dict

class Zamestnanec:
    def __init__(self, jmeno: str, prijmeni: str, typ_smlouvy: str, hodinova_sazba: float):
        self._validace(jmeno, prijmeni, typ_smlouvy, hodinova_sazba)
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.typ_smlouvy = typ_smlouvy.upper()
        self.hodinova_sazba = hodinova_sazba
        self.odpracovane_hodiny: Dict[date, float] = {}

    def _validace(self, jmeno, prijmeni, typ, sazba):
        if not jmeno.strip():
            raise ValueError("Jméno nesmí být prázdné")
        if not prijmeni.strip():
            raise ValueError("Příjmení nesmí být prázdné")
        if typ.upper() not in {"DPČ", "DPP", "IČO"}:
            raise ValueError("Neplatný typ smlouvy")
        if sazba <= 0:
            raise ValueError("Hodinová sazba musí být kladné číslo")

    def pridej_hodiny(self, datum: date, hodiny: float):
        if datum.weekday() >= 5:
            raise ValueError("Nelze zadat práci o víkendu")
        if self.typ_smlouvy == "DPČ" and hodiny > 20:
            raise ValueError("DPČ max 20 hodin/týdně")
        self.odpracovane_hodiny[datum] = hodiny
