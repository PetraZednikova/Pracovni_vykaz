import streamlit as st
from datetime import datetime, date
import calendar
from pathlib import Path

from data_handler import DataManager
from calculator import MzdovySystem
from svatky import ceske_statni_svatky
from report_exporter import export_vykaz


def zadat_hodiny(z, rok: int, mesic: int, system: MzdovySystem):
    st.subheader(f"Zadávání hodin pro {z.jmeno} {z.prijmeni}")
    for den in range(1, calendar.monthrange(rok, mesic)[1] + 1):
        datum = date(rok, mesic, den)
        if system.je_pracovni_den(datum):
            default = z.odpracovane_hodiny.get(datum, "")
            vstup   = st.text_input(f"{datum.day}.{mesic}", value=str(default), key=f"{datum}")
            if vstup:
                try:
                    hod = float(vstup)
                    z.pridej_hodiny(datum, hod)
                except ValueError:
                    st.warning(f"„{vstup}“ není platné číslo.")
                except Exception as e:
                    st.error(f"Chyba: {e}")


def main():
    st.title("Zadávání hodin pro zaměstnance")

    # Cesty
    data_dir      = Path("data")
    tmpl_dir      = Path("templates")
    json_file     = data_dir / "employees.json"
    backup_file   = data_dir / "employees_backup.json"
    template_path = tmpl_dir / "template.xlsx"

    # Obnova ze zálohy
    if st.button("🔁 Obnovit data ze zálohy"):
        if backup_file.exists():
            json_file.write_text(backup_file.read_text(), encoding="utf-8")
            st.success("Data obnovena ze zálohy.")
            st.experimental_rerun()
        else:
            st.warning("Záloha neexistuje.")

    # Načtení zaměstnanců
    zamestnanci = DataManager.nacti_zamestnance(json_file)
    if not zamestnanci:
        st.warning("Žádní zaměstnanci.")
        return

    # Výběr zaměstnance
    vyber = st.selectbox(
        "Vyber zaměstnance:",
        [f"{z.jmeno} {z.prijmeni}" for z in zamestnanci]
    )
    zam = next(z for z in zamestnanci if f"{z.jmeno} {z.prijmeni}" == vyber)

    # Volba období
    rok   = st.number_input("Rok:",   value=datetime.now().year, min_value=2000, max_value=2100, step=1)
    mesic = st.selectbox(    "Měsíc:", list(range(1, 13)), index=datetime.now().month - 1)

    # Mzdový systém
    svatky = ceske_statni_svatky(rok)
    system = MzdovySystem(svatky=svatky)

    # Zadání hodin
    zadat_hodiny(zam, rok, mesic, system)

    # Průběžný výpočet mzdy
    st.markdown("---")
    st.subheader("💰 Průběžný výpočet mzdy")
    report = system.vypocet_mzdy(zam, mesic, rok)
    report["typ smlouvy"] = zam.typ_smlouvy
    st.write(report)

    # Uložení dat + záloha
    if st.button("💾 Uložit data"):
        if json_file.exists():
            json_file.replace(backup_file)
        DataManager.uloz_zamestnance(zamestnanci, json_file)
        st.success("Data uložena.")
        st.balloons()

    # Volba začátku pracovní doby
    start_time = st.radio("Začátek pracovní doby:", ("8:30", "9:30"))

    # Export a stažení výkazu
    if st.button("📤 Exportovat data"):
        out_path = Path(f"vykaz_{mesic}_{zam.prijmeni}.xlsx")
        export_vykaz(zam, mesic, rok, template_path, out_path, start_time)
        with open(out_path, "rb") as f:
            st.download_button(
                label="⬇️ Stáhnout výkaz",
                data=f,
                file_name=out_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()
