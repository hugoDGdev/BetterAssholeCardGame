l = [True, True, True, True]

def absListe(liste):
    prev = None
    all = None
    counter = 0
    for l in liste:
        if counter == 0:
            if l == True:
                all = True
                prev = True
            if l == False:
                all = False
                prev = False
        else:
            if prev == True and l == True:
                prev = True
                all = True
            elif prev == False and l == False:
                prev = False
                all = False
            else:
                all = None
                break
        counter +=1
    return all
print(absListe(l))
