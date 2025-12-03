dico = {12: 1, 10: 1, 8: 2, 7: 1, 5: 1, 4: 1, 3: 1, 2: 2, 1: 2, 0: 1}

resultat = []

for v in dico:
    n = dico.get(v)
    if n >= 1:
        resultat.append(v)

for r in resultat:
    i = resultat.index(r)
    print(r, i)