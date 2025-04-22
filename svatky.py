from datetime import date

def velikonoce(rok: int) -> date:
    """Vypočítá datum Velikonoční neděle (gregoriánský kalendář)."""
    a = rok % 19
    b = rok // 100
    c = rok % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mesic = (h + l - 7 * m + 114) // 31
    den = ((h + l - 7 * m + 114) % 31) + 1
    return date(rok, mesic, den)

def ceske_statni_svatky(rok: int) -> list[date]:
    """Vrací seznam státních svátků ČR včetně Velikonoc."""
    velikonocni_nedele = velikonoce(rok)
    velky_patek = velikonocni_nedele.replace(day=velikonocni_nedele.day - 2)
    velikonočni_pondeli = velikonocni_nedele.replace(day=velikonocni_nedele.day + 1)

    return [
        date(rok, 1, 1),   # Nový rok
        velky_patek,
        velikonočni_pondeli,
        date(rok, 5, 1),   # Svátek práce
        date(rok, 5, 8),   # Den vítězství
        date(rok, 7, 5),   # Cyril a Metoděj
        date(rok, 7, 6),   # Jan Hus
        date(rok, 9, 28),  # Svatý Václav
        date(rok, 10, 28), # Vznik ČSR
        date(rok, 11, 17), # Den boje za svobodu
        date(rok, 12, 24), # Štědrý den
        date(rok, 12, 25), # 1. svátek vánoční
        date(rok, 12, 26), # 2. svátek vánoční
    ]
