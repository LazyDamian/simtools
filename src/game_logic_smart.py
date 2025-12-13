# src/game_logic_smart.py (OPTIMIERTE VERSION: Mit Versenkt-Prüfer)

import numpy as np
from collections import deque
import random
import time
from .game_setup import erstelle_neues_spielfeld, ANZ_SCHIFFE, FELD_GROESSE

# Globale Konstanten für den KI-Status
STATUS_UNBEKANNT = 0
STATUS_WASSER = 1
STATUS_TREFFER = 2


def get_nachbarn(z, s, zeilen, spalten):
    """Gibt alle orthogonalen und diagonalen Nachbarn zurück (für den Abstand um Schiffe)."""
    nachbarn = []
    for dz in [-1, 0, 1]:
        for ds in [-1, 0, 1]:
            if dz == 0 and ds == 0:
                continue
            nz, ns = z + dz, s + ds
            if 0 <= nz < zeilen and 0 <= ns < spalten:
                nachbarn.append((nz, ns))
    return nachbarn


def markiere_versenktes_schiff(z_start, s_start, spielfeld_original, ki_status):
    """
    Prüft, ob das Schiff, das an (z_start, s_start) liegt, vollständig versenkt ist.
    Wenn ja, markiert es den umgebenden Bereich als STATUS_WASSER in ki_status.

    :return: True, wenn das Schiff versenkt wurde, False sonst.
    """
    schiffs_laenge = spielfeld_original[z_start, s_start]
    zeilen, spalten = ki_status.shape

    # 1. Sammle alle Koordinaten dieses Schiffes
    schiffs_koordinaten = []

    # Der Wert im Originalfeld ist die Länge des Schiffes
    alle_moeglichen_koordinaten = np.argwhere(spielfeld_original == schiffs_laenge)

    # Iteriere über alle Teile dieser Länge und prüfe, ob sie zusammenhängen
    # Da das spielfeld_original nur die Schiffslänge enthält, müssen wir
    # das Trefferverhalten über ki_status prüfen.

    treffer_zaehler = 0

    # Finde alle Teile des Schiffes in der ki_status Matrix (die den Treffer-Status speichert)
    # WICHTIG: Die ursprüngliche Logik gibt nicht einfach die Schiffskoordinaten zurück.
    # Wir müssen das Originalfeld verwenden, um die gesamte Form zu erkennen.

    # Vereinfachte Prüfung (funktioniert nur, wenn wir die Schiffsteile im Originalfeld auf 0 setzen würden, was wir nicht tun.)
    # Wir müssen hier auf dem Originalfeld iterieren und im KI-Status prüfen, ob alle Teile getroffen sind.

    # Alternativer, robuster Ansatz: Zähle alle Treffer des Schiffstyps
    for z, s in alle_moeglichen_koordinaten:
        if ki_status[z, s] == STATUS_TREFFER:
            treffer_zaehler += 1
            schiffs_koordinaten.append((z, s))

    # 2. Prüfe auf Versenkung
    if treffer_zaehler == schiffs_laenge:
        # Schiff ist versenkt!

        # 3. Markiere den Abstand als Wasser
        for z_schiff, s_schiff in schiffs_koordinaten:
            for nz, ns in get_nachbarn(z_schiff, s_schiff, zeilen, spalten):
                # Markiere nur Felder, die noch unbekannt sind
                if ki_status[nz, ns] == STATUS_UNBEKANNT:
                    ki_status[nz, ns] = STATUS_WASSER

        return True

    return False


# Die Hauptsimulationsfunktion
def simuliere_spiel_smart():
    # --- 1. Initialisierung und Setup ---
    # Setting Seed (wie zuvor, um faire Simulationen zu gewährleisten)
    aktuelle_zeit = int(time.time() * 1000000)
    np.random.seed(aktuelle_zeit % 2 ** 32)
    random.seed(aktuelle_zeit % 2 ** 32)

    feld = erstelle_neues_spielfeld()
    zeilen, spalten = FELD_GROESSE

    # spielfeld_original enthält die Längen der Schiffe und dient als Nachschlagewerk (Read-Only)
    spielfeld_original = np.copy(feld)

    # spielfeld_zum_beschuss wird verändert (Treffer auf 0 gesetzt)
    spielfeld_zum_beschuss = np.copy(feld)

    gesamte_schiffsteile = np.sum([länge * ANZ_SCHIFFE[länge] for länge in ANZ_SCHIFFE])

    schüsse = 0
    treffer_zaehler = 0

    # ki_status: 0: Unbekannt, 1: Wasser (Miss), 2: Treffer (Hit)
    ki_status = np.zeros(FELD_GROESSE, dtype=int)

    # Warteschlange für den Zielmodus
    ziel_warteschlange = deque()

    # --- 2. Haupt-Schleife: Jagd- und Zielmodus ---
    while treffer_zaehler < gesamte_schiffsteile:

        # --- BESTIMMEN DES NÄCHSTEN SCHUSSES ---
        if ziel_warteschlange:
            # ZIELMODUS
            z, s = ziel_warteschlange.popleft()

            # Überspringe, wenn das Feld bereits bekannt ist
            if ki_status[z, s] != STATUS_UNBEKANNT:
                continue

        else:
            # JAGDMODUS (Checkerboard Pattern)

            z, s = None, None
            # Jagdstrategie: Wir suchen nur Felder, die UNBEKANNT sind UND auf dem Schachbrettmuster liegen.
            alle_unbekannten = [(z_unk, s_unk)
                                for z_unk in range(zeilen)
                                for s_unk in range(spalten)
                                if ki_status[z_unk, s_unk] == STATUS_UNBEKANNT]

            # Finde ein unbekanntes Feld im Schachbrettmuster
            for z_jagd, s_jagd in alle_unbekannten:
                if (z_jagd + s_jagd) % 2 == 0:
                    z, s = z_jagd, s_jagd
                    break

            # Fallback: Wenn das Muster keine Felder mehr hat, schießen wir zufällig (aber nur auf Unbekannt)
            if z is None and alle_unbekannten:
                z, s = alle_unbekannten.pop(np.random.randint(len(alle_unbekannten)))

            if z is None:
                # Sollte nur passieren, wenn alle 100 Felder bekannt sind (Spielende)
                break

                # --- SCHUSS AUSFÜHREN ---
        schüsse += 1

        if spielfeld_zum_beschuss[z, s] > 0:
            # TREFFER!
            treffer_zaehler += 1
            ki_status[z, s] = STATUS_TREFFER  # Markiere als Treffer

            # Versenkt-Prüfer aufrufen: Markiere Abstand als Wasser
            if markiere_versenktes_schiff(z, s, spielfeld_original, ki_status):
                # Wenn versenkt, leere die Warteschlange, da das Schiff erledigt ist
                ziel_warteschlange.clear()

            # Neue umliegende Ziele zur Warteschlange hinzufügen (nur orthogonal)
            for nz, ns in [(z + 1, s), (z - 1, s), (z, s + 1), (z, s - 1)]:
                if 0 <= nz < zeilen and 0 <= ns < spalten and ki_status[nz, ns] == STATUS_UNBEKANNT:
                    ziel_warteschlange.append((nz, ns))

        else:
            # WASSER
            ki_status[z, s] = STATUS_WASSER

    return schüsse