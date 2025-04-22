# Pracovní výkaz a mzdový systém

Jednoduchá aplikace v Pythonu + Streamlit pro zadávání odpracovaných hodin, výpočet mzdy i export naformátovaného výkazu do Excelu s respektem českých víkendů a státních svátků (včetně Velikonoc).

## Funkce
- **CLI i webové GUI** (Streamlit) nad stejnou podnikovo‑logickou vrstvou
- **Načtení / uložení** zaměstnanců v JSON (UTF‑8, diakritika)
- **Interaktivní zadávání hodin** po jednotlivých pracovních dnech
- **Výpočet mzdy** za zvolený měsíc/rok (hodinová sazba, typ smlouvy)
- **České státní svátky** včetně Velkého pátku a pondělí po Velikonocích
- **Excel‑šablona** s dynamickým doplněním (perioda, jméno, typ smlouvy, den, začátek, konec, přestávka, hodiny)
- **Šedivé označení** víkendů a svátků, k svátkům přidáno “SV” u dne v měsíci
- **Export a stažení** finálního `.xlsx` z CLI i Streamlitu

