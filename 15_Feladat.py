#15. Feladat. Számok a szomszédban. (max 4 fő)
#Írj olyan programot, amely elhelyezi az 1-től 12-ig terjedő számokat az ábrában úgy, hogy a körökkel
#szomszédos mezőkbe kerülő számok összege megegyezzen a körben lévő számmal! Könnyítésül két számot előre beírtunk.

# A körök összegei és a hozzájuk tartozó (1-alapú) négyzetindexek
kor_osszegek = {
    23: [1, 2, 5, 6],    # k0
    37: [2, 3, 6, 7],    # k1
    30: [3, 4, 7, 8],    # k2
    27: [5, 6, 9, 10],   # k4
    40: [6, 7, 10, 11],  # k5
    24: [7, 8, 11, 12],  # k6
}

# Előre rögzített négyzetek értékei: az 5. négyzet értéke 1, a 8. négyzet értéke 5.
rogzitett_negyzetek = {5: 1, 8: 5}

# Az összes négyzet indexelése 1-től 12-ig
osszes_index = list(range(1, 13))

# Azok a négyzetek amig még nem rendelkeznek értékkel
szabad_indexek = [i for i in osszes_index if i not in rogzitett_negyzetek]

# Az 1–12 közötti számok, kivéve a már rögzítetteket (1 és 5)
osszes_szam = set(range(1, 13))
felhasznalt_szamok = set(rogzitett_negyzetek.values())       # Felvesszük a rogzitett_negyzetek értékeit
szabad_szamok = list(osszes_szam - felhasznalt_szamok)       # Csak a még szabadon lévő számokat tartalmazza

megoldasok = []                                              # Ebben a listában lesznek a program által megtalált megoldások

def kor_ervenyes(hozzarendeles, index_lista, cel):
    """
    Ha az adott kör négyzeteihez már mind van érték, ellenőrzi, hogy az összeadásuk megegyezik-e a célértékkel.
    Ha nem minden érték van még hozzárendelve, True-t ad vissza, mert még nem lehet kizárni.
    """
    if all(idx in hozzarendeles for idx in index_lista):    # Végigmegyünk az index_lista összes elemén, és ellenőrizzük hogy szerepelnek-e a hozzarendeles-be
        osszeg = sum(hozzarendeles[idx] for idx in index_lista) # Összeadjuk azokat a számokat, amik hozzarendeles-ben az index_lista indexeihez tartoznak.
        return osszeg == cel                                # Ha az összeg megegyezik a a cel-ertekkel akkor a feltétel feljesül.
    return True

def visszalep(hozzarendeles, szabad_index_lista, hasznalt):
    """
    Rekurzív backtracking megoldás:
      - hozzarendeles: a jelenlegi hozzárendelés (szótár, ahol a kulcs a négyzet indexe, az érték a szám)
      - szabad_index_lista: a még kitöltendő négyzetek indexei
      - hasznalt: már használt számok halmaza
    """
    if not szabad_index_lista:
        # Ha minden négyzet ki lett töltve, ellenőrizzük az összes kör feltételét.
        for kor_osszeg_ertek, indexek in kor_osszegek.items():
            if sum(hozzarendeles[idx] for idx in indexek) != kor_osszeg_ertek:
                return
        megoldasok.append(hozzarendeles.copy())
        return

    # Válasszuk ki a következő kitöltendő négyzet indexét
    aktualis_index = szabad_index_lista[0]
    for szam in szabad_szamok:
        if szam in hasznalt:
            continue
        # Próbáljuk ki az aktuális számot
        hozzarendeles[aktualis_index] = szam
        hasznalt.add(szam)
        # Azok a körök, amelyek tartalmazzák ezt a négyzetet, mostantól ellenőrizendők
        ervenyes = True
        for kor_osszeg_ertek, indexek in kor_osszegek.items():
            if aktualis_index in indexek:
                if not kor_ervenyes(hozzarendeles, indexek, kor_osszeg_ertek):
                    ervenyes = False
                    break
        if ervenyes:
            visszalep(hozzarendeles, szabad_index_lista[1:], hasznalt)
        # Backtracking: visszavonjuk az aktuális hozzárendelést
        hasznalt.remove(szam)
        del hozzarendeles[aktualis_index]

# Kezdeti hozzárendelés: a rögzített négyzetek beállítása
kezdeti_hozzarendeles = rogzitett_negyzetek.copy()
kezdeti_hasznalt = set(rogzitett_negyzetek.values())

visszalep(kezdeti_hozzarendeles, szabad_indexek, kezdeti_hasznalt)

# Eredmény kiírása
if megoldasok:
    print(f"{len(megoldasok)} megoldást találtunk.\n")
    # Az első megtalált megoldás kiírása
    elso_megoldas = megoldasok[0]
    for idx in sorted(elso_megoldas.keys()):
        print(f"s{idx} = {elso_megoldas[idx]}")
else:
    print("Nincs megoldás a megadott feltételek mellett.")
