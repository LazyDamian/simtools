# src/game_setup.py

import numpy as np

# Konfiguration der Schiffe (Länge: Anzahl)
ANZ_SCHIFFE = {5: 1, 4: 1, 3: 2, 2: 1}
FELD_GROESSE = (10, 10)


def ist_bereich_frei_mit_abstand(feld, z, s, form):
    """
    Prüft, ob der Bereich für die Platzierung eines Schiffes frei ist,
    einschließlich eines 1-Felder-Abstands rundherum.
    """
    zeilen, spalten = feld.shape

    z1 = max(0, z - 1)
    s1 = max(0, s - 1)
    z2 = min(zeilen, z + form[0] + 1)
    s2 = min(spalten, s + form[1] + 1)

    return np.all(feld[z1:z2, s1:s2] == 0)


def erstelle_neues_spielfeld():
    """
    Erzeugt ein NEUES, zufällig platziertes Spielfeld.
    """

    neues_feld = np.zeros(FELD_GROESSE, dtype=int)
    zeilen_feld, spalten_feld = neues_feld.shape

    # Durchlaufe Schiffe von groß nach klein
    for länge in sorted(ANZ_SCHIFFE.keys(), reverse=True):
        anzahl_schiffe = ANZ_SCHIFFE[länge]

        for _ in range(anzahl_schiffe):
            platziert = False

            # Zufällige Richtung wählen (horiz/vert)
            for richtung in np.random.permutation(["vert", "horiz"]):

                if richtung == "vert":
                    form = (länge, 1)
                else:
                    form = (1, länge)

                # Finde alle möglichen Platzierungen
                mögliche_platzierung = [
                    (z, s)
                    for z in range(zeilen_feld - form[0] + 1)
                    for s in range(spalten_feld - form[1] + 1)
                    if ist_bereich_frei_mit_abstand(neues_feld, z, s, form)]

                if mögliche_platzierung:
                    # Wähle eine zufällige Platzierung
                    idx = np.random.randint(len(mögliche_platzierung))
                    z, s = mögliche_platzierung[idx]

                    neues_feld[z:z + form[0], s:s + form[1]] = länge
                    platziert = True
                    break

            # Wenn die Platzierung fehlschlägt, ist das ein kritischer Fehler
            if not platziert:
                raise RuntimeError(
                    f"Konnte Schiff der Länge {länge} nicht platzieren."
                )

    return neues_feld