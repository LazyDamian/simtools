# src/game_logic.py

import numpy as np
from .game_setup import erstelle_neues_spielfeld, ANZ_SCHIFFE, FELD_GROESSE
import random  # <--- NEUER IMPORT HINZUFÜGEN
import time


def simuliere_spiel():
    # NEU: Setze den Python- und NumPy-Zufallsgenerator für jede Simulation zurück,
    # um sicherzustellen, dass die Platzierung und die Ziele neu gemischt werden.
    # Wir verwenden die aktuelle Systemzeit als Seed, um echte Zufälligkeit zu gewährleisten.
    np.random.seed(int(time.time() * 1000000) % 2 ** 32)
    random.seed(int(time.time() * 1000000) % 2 ** 32)

    # ... der Rest des Codes bleibt wie zuvor ...

    # 1. Neues Spielfeld erstellen
    feld = erstelle_neues_spielfeld()
    zeilen, spalten = FELD_GROESSE

    # 2. Status-Tracking
    # spielfeld_zum_beschuss ist die Arbeitskopie
    spielfeld_zum_beschuss = np.copy(feld)

    # Die Gesamtanzahl der Trefferpunkte (MUSS 17 SEIN)
    gesamte_schiffsteile = np.sum([länge * ANZ_SCHIFFE[länge] for länge in ANZ_SCHIFFE])

    schüsse = 0
    treffer_zaehler = 0

    # 3. Alle möglichen Schussziele in zufälliger Reihenfolge
    alle_ziele = []
    for z in range(zeilen):
        for s in range(spalten):
            alle_ziele.append((z, s))

    np.random.shuffle(alle_ziele)

    # 4. Spiel-Loop: Stoppt, wenn 17 Treffer erreicht sind.
    while treffer_zaehler < gesamte_schiffsteile and alle_ziele:

        # Nächste zufällige Koordinate auswählen
        z, s = alle_ziele.pop()
        schüsse += 1

        # Prüfen, ob an dieser Stelle ein Schiff ist (Wert > 0)
        if spielfeld_zum_beschuss[z, s] > 0:
            # TREFFER!
            treffer_zaehler += 1
            # Markiere das Schiffsteil als getroffen (0)
            spielfeld_zum_beschuss[z, s] = 0

            # Wir lassen den Debug-Print weg, um die Simulation nicht zu verlangsamen.

    # Nur zur Sicherheit: Wenn nicht alle Treffer gefunden wurden, obwohl die Liste leer ist,
    # liegt ein Problem vor.
    if treffer_zaehler < gesamte_schiffsteile:
        # Dieser Fall sollte bei der Zufallssuche nie eintreten, da alle 17 Teile im Feld sind
        # und alle 100 Felder beschossen werden.
        return 100

    return schüsse