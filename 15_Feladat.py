# A körök összegei és a hozzájuk tartozó (1-alapú) négyzetindexek
circle_dict = {
    23: [1, 2, 5, 6],    # c0
    37: [2, 3, 6, 7],    # c1
    30: [3, 4, 7, 8],    # c2
    27: [5, 6, 9, 10],   # c4
    40: [6, 7, 10, 11],  # c5
    24: [7, 8, 11, 12],  # c6
}

# Előre rögzített négyzetértékek: 5. négyzet értéke 1, 8. négyzet értéke 5.
fixed_squares = {5: 1, 8: 5}

# Az összes négyzet indexei 1-től 12-ig (1-alapú indexelés)
all_indices = list(range(1, 13))
# Azok a négyzetek, ahol még nem adtunk értéket
free_indices = [i for i in all_indices if i not in fixed_squares]

# Az 1–12 közötti számokból kivesszük a már rögzítetteket (1 és 5)
all_numbers = set(range(1, 13))
used_numbers = set(fixed_squares.values())
free_numbers = list(all_numbers - used_numbers)
free_numbers.sort()  # Rendezhetjük a könnyebb átláthatóság érdekében

solutions = []  # Itt tároljuk a megtalált megoldásokat

def is_circle_valid(assignment, indices, target):
    """
    Ha az adott kör négyzeteihez már mind van érték, ellenőrzi, hogy az összeadásuk megegyezik-e a célértékkel.
    Ha nem minden érték van még hozzárendelve, True-t ad vissza, mert még nem lehet kizárni.
    """
    if all(idx in assignment for idx in indices):
        s = sum(assignment[idx] for idx in indices)
        return s == target
    return True

def backtrack(assignment, free_idx_list, used):
    """
    Rekurzív backtracking megoldás:
      - assignment: a jelenlegi hozzárendelés (szótár, melyben a kulcs a négyzet indexe, érték pedig a szám)
      - free_idx_list: a még kitöltendő négyzetek indexei
      - used: már használt számok halmaza
    """
    if not free_idx_list:
        # Ha minden négyzet ki lett töltve, ellenőrizzük az összes kör feltételét.
        for circle_sum, indices in circle_dict.items():
            if sum(assignment[idx] for idx in indices) != circle_sum:
                return
        solutions.append(assignment.copy())
        return

    # Válasszuk ki a következő kitöltendő négyzetet
    current_idx = free_idx_list[0]
    for num in free_numbers:
        if num in used:
            continue
        # Próbáljuk ki az aktuális számot
        assignment[current_idx] = num
        used.add(num)
        # Azok a körök, amelyek tartalmazzák ezt a négyzetet, mostantól ellenőrizendők
        valid = True
        for circle_sum, indices in circle_dict.items():
            if current_idx in indices:
                if not is_circle_valid(assignment, indices, circle_sum):
                    valid = False
                    break
        if valid:
            backtrack(assignment, free_idx_list[1:], used)
        # Backtracking: visszavonjuk az aktuális hozzárendelést
        used.remove(num)
        del assignment[current_idx]

# Kezdeti hozzárendelés: a rögzített négyzetek beállítása
initial_assignment = fixed_squares.copy()
initial_used = set(fixed_squares.values())

backtrack(initial_assignment, free_indices, initial_used)

# Eredmény kiírása
if solutions:
    print(f"{len(solutions)} megoldást találtunk.\n")
    # Az első megtalált megoldás kiírása
    sol = solutions[0]
    for idx in sorted(sol.keys()):
        print(f"s{idx} = {sol[idx]}")
else:
    print("Nincs megoldás a megadott feltételek mellett.")