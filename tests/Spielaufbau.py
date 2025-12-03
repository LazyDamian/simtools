import numpy as np
import matplotlib.pyplot as plt


def ist_bereich_frei_mit_abstand(feld, z, s, form):
    zeilen, spalten = feld.shape
    z1 = max(0, z - 1)
    s1 = max(0, s - 1)
    z2 = min(zeilen, z + form[0] + 1)
    s2 = min(spalten, s + form[1] + 1)


    return np.all(feld[z1:z2, s1:s2] == 0)

spielfeld = np.zeros((10, 10), dtype=int)
anzahl = {5:1, 4:1, 3:2, 2:1}

def schiffe_platzieren():
    zeilen_feld, spalten_feld = spielfeld.shape

    for länge in sorted(anzahl.keys(), reverse=True):
        nummer = anzahl[länge]
        for i in range(nummer):
            platziert = False


            for richtung in np.random.permutation(["vert", "horiz"]):

                if richtung == "vert":
                    form = (länge, 1)
                else:
                    form = (1, länge)

                mögliche_platzierung = [
                    (z, s)
                    for z in range(zeilen_feld - form[0] + 1)
                    for s in range(spalten_feld - form[1] + 1)
                    if ist_bereich_frei_mit_abstand(spielfeld, z, s, form)]

                if mögliche_platzierung:

                    z, s = mögliche_platzierung[np.random.randint(len(mögliche_platzierung))]
                    spielfeld[z:z + form[0], s:s + form[1]] = länge
                    platziert = True
                    break

            if not platziert:
                for richtung in ["vert", "horiz"]:
                    if richtung == "vert":
                        form = (länge, 1)
                    else:
                        form = (1, länge)

                    for z in range(zeilen_feld - form[0] + 1):
                        for s in range(spalten_feld - form[1] + 1):
                            if ist_bereich_frei_mit_abstand(spielfeld, z, s, form):
                                spielfeld[z:z + form[0], s:s + form[1]] = länge
                                platziert = True
                                break
                        if platziert:
                            break
                    if not platziert:
                        raise RuntimeError(f"Schiff kann nicht platziert werden: Länge {länge}, Schiff {i+1}")



    return spielfeld

spielfeld = schiffe_platzieren()

np.set_printoptions(linewidth=120)


fig, ax = plt.subplots(figsize=(6,6))

im = ax.imshow(spielfeld)


ax.set_xticks(np.arange(10))
ax.set_yticks(np.arange(10))
ax.set_xticklabels([chr(ord('A') + i) for i in range(10)])
ax.set_yticklabels([str(i+1) for i in range(10)])


ax.set_xticks(np.arange(-0.5, 10, 1), minor=True)
ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
ax.grid(which="minor")


plt.show()



