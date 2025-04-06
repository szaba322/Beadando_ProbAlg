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


# Ha az adott kör négyzeteihez már mind van érték, ellenőrzi, hogy az összeadásuk megegyezik-e a célértékkel.
# Ha nem minden érték van még hozzárendelve, True-t ad vissza, mert még nem lehet kizárni.
def kor_ervenyes(hozzarendeles, index_lista, cel):
    if all(idx in hozzarendeles for idx in index_lista):        # Végigmegyünk az index_lista összes elemén, és ellenőrizzük hogy szerepelnek-e a hozzarendeles-be
        osszeg = sum(hozzarendeles[idx] for idx in index_lista) # Összeadjuk azokat a számokat, amik hozzarendeles-ben az index_lista indexeihez tartoznak.
        return osszeg == cel                                    # Ha az összeg megegyezik a a cel-ertekkel akkor a feltétel feljesül.
    return True

# A függvény célja, hogy a szabad négyzetekre olyan számokat rendeljünk, amelyek eleget tesznek a feltételeknek. (Négyzetek összege = Kör)
def visszalep(hozzarendeles, szabad_index_lista, hasznalt):
    if not szabad_index_lista:                                                   # szabad_index_lista: a még kitöltendő négyzetek indexei
        # Ha minden négyzet ki lett töltve, ellenőrizzük az összes kör feltételét.
        for kor_osszeg_ertek, indexek in kor_osszegek.items():
            if sum(hozzarendeles[idx] for idx in indexek) != kor_osszeg_ertek:   # Minden körnél kiszámolja az adott körhöz tartozó négyzetek értékeinek összegét.
                return
        megoldasok.append(hozzarendeles.copy())                                  # Másolat készítése a hozzarendeles dictionary-ből
        return
 
    aktualis_index = szabad_index_lista[0]                     # Kiválasztja a következő kitöltendő négyzet indexét
    for szam in szabad_szamok:                                 # A ciklus végigiterál minden olyan számot a "szabad_szamok" listából, amit feltudunk használni
        if szam in hasznalt:                                   # Ha a szám szerepel a "hasznalt" halmazban akkor kihagyja
            continue
        hozzarendeles[aktualis_index] = szam                   # Az aktuális szám kipróbálása
        hasznalt.add(szam)                                     # Hozzáadjuk a számot a "hasznalt" halmazhoz, hogy később ne használjuk újra
        ervenyes = True
        for kor_osszeg_ertek, indexek in kor_osszegek.items(): # Végigmegy a "kor_osszegek" minden elemén, ahol a kulcs az elvárt összegét jelöli, az érték pedig a korhoz tartozó négyzetek indexeit.
            if aktualis_index in indexek:
                if not kor_ervenyes(hozzarendeles, indexek, kor_osszeg_ertek): # Ha a kör ellenőrzése False-t ad (nem egyezik meg a kívánt értékkel) akkor megszakítja a ciklust.
                    ervenyes = False
                    break
        if ervenyes:
            visszalep(hozzarendeles, szabad_index_lista[1:], hasznalt)
        hasznalt.remove(szam)
        del hozzarendeles[aktualis_index]

kezdeti_hozzarendeles = rogzitett_negyzetek.copy() # Készítünk egy másolatot a "rogzitet_negyzetek"-ről. 
kezdeti_hasznalt = set(rogzitett_negyzetek.values()) 

#A "visszalep" függvény a backtracking algoritmust valósítja meg, amely a szabad négyzeteket próbálja kitölteni a megadott szabályok szerint.
visszalep(kezdeti_hozzarendeles, szabad_indexek, kezdeti_hasznalt)

# Eredmény kiírása
if megoldasok:                                                         # Ha a "megoldasok" listában van legalább egy megoldást akkor belép az IF ágba.
    print(f"A feladatra {len(megoldasok)} megoldást találtunk.\n")     # Kiírja hogy hány megoldást talált.
    elso_megoldas = megoldasok[0]                                      # Az első megtalált megoldás kiírása
    for idx in sorted(elso_megoldas.keys()):                           # Sorba rendezi az indexeket, és a for ciklus végig iterál az összes rendezett indexen, és kiírja.
        print(f"{idx}. Indexű négyzet = {elso_megoldas[idx]}")
else:                                                                  # Ha a "megoldasok" listában nincs egy megoldás se, akkor az else ág fut le.
    print("Nincs megoldás a megadott feltételek mellett.")
