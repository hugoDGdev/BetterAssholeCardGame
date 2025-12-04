from random import shuffle
from colorama import Fore, Back, Style

valeurCarte = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]
listeSymbole = ["S", "C", "H", "D"]
# Spades = Piques; Clubs = Trèfles; Hearts = Coeurs (bah ouais logique); Diamonds = Carreaux
listeCartes = []

#utils
def parserCartes(entree, joueur, typePli, min):
    entree = entree.strip()
    if not entree:
        print("Vous n'avez entré aucune carte.")
        return None
    
    codes = entree.upper().replace(" ", "").split(",")
    cartes = []

    for c in codes:
        if len(c) <2 and len(c) >2:
            print(f"Format invalide pour {c}")
            return None
        
        symbole = c[0]
        valeurTxt = c[1:]

        if symbole not in listeSymbole:
            print(f"Symbole invalide {symbole}")
            return None
    
        if valeurTxt not in valeurCarte:
            print(f"Valeur invalide {valeurTxt}")
            return None

        valeurIndex = valeurCarte.index(valeurTxt)

        carteObj = trouverCarte(joueur.main, symbole, valeurIndex)
        if not carteObj:
            print(f"Vous n'avez pas cette carte {colorCards(c)}")
            return None
        
        if carteObj in cartes:
            print(f"Vous avez entré 2x la meme carte {c}")
            return None
        
        cartes.append(carteObj)
    
    if len(cartes) != typePli:
        print(f"Vous devez jouer {typePli} carte(s)")
        return None

    valeurs = {c.valeur for c in cartes}
    if len(valeurs) != 1:
        print("Toutes les cartes jouées doivent avoir la meme valeur")
        return None
    if next(iter(valeurs)) < min:
        print("La valeur des cartes est trop basse")
        return None
    return cartes

def trouverCarte(main, symbole, valeur):
    for c in main:
        if c.symbole == symbole and c.valeur == valeur:
            return c
    return None

def demander(type):
    if type[0] == "typePli":
        while True:
            pli = input("Quel taille de pli voulez vous jouer ? (1-4)\n> ")
            try:
                pli = int(pli)
            except ValueError:
                print("Veuillez renseignez un nombre entre 1 et 4")
                continue
            if pli not in (1, 2, 3, 4):
                print("Veuillez renseignez un nombre entre 1 et 4")
                continue
            if not type[1].aCombinaison(pli):
                print("Vous n'avez pas ce type dans votre main")
                continue
            
            return pli

def absListe(liste):
    temp = []
    for l in liste:
        if l == True:
            temp.append(1)
        if l == False:
            temp.append(0)
    if sum(temp) == 0:
        return False
    elif sum(temp) == len(liste):
        return True
    else:
        return None
    
def colorCards(string):
    if string[0] == 's' or string[0] == 'c':
        color = Fore.BLACK
    else:
        color = Fore.RED
    
    colored = color + string
    return colored

class Carte:
    def __init__(self, symbole, valeur):
        self.symbole = symbole
        self.valeur = valeur
    
    def __repr__(self):
        return f"{self.symbole}{valeurCarte[self.valeur]}"
    
    def force(self):
        return self.valeur

class Joueur:
    def __init__(self, id):
        self.id = id
        self.main = []
        self.peutJouer = True

    def __repr__(self):
        return f"Joueur{self.id} : {self.main}, peut jouer : {self.peutJouer}"
    
    def trierMain(self):
        self.main.sort(key=lambda c: c.force(), reverse=True)

    def retirerCartes(self, cartes):
        for c in cartes:
            if c in self.main:
                self.main.remove(c)

    def mainVide(self):
        return len(self.main) == 0
    
    def mainCheck(self):
        occurence = {}
        for carte in self.main:
            v = carte.valeur
            occurence[v] = occurence.get(v, 0) + 1
        return occurence
    
    def aCombinaison(self, type):
        occurence = self.mainCheck()
        resultat = []

        for v in occurence:
            n = occurence.get(v)
            if n >= type:
                resultat.append(v)

        return resultat


class GameManager:
    def __init__(self, nombreJoueurs):
        self.deck = []
        self.joueurs = []
        self.actuelJoueur = 0

        for i in range(nombreJoueurs):
            self.joueurs.append(Joueur(i))
    
    def creerDeck(self):
        self.deck.clear()
        for s in listeSymbole:
            for v in range(13):
                self.deck.append(Carte(s, v))
        shuffle(self.deck)

    def distribuer(self):
        index = 0
        for joueur in self.joueurs:
            joueur.main = self.deck[index:index + 13]
            index += 13

game = GameManager(4)
game.creerDeck()
game.distribuer()

actuelJoueur = 0
nbTour = 0
typePli = 0
valeurMin = 0
dernierJoueur = None

while True:
    if nbTour == 0:
        #temp = 0
        for j in game.joueurs:
            j.peutJoeur = True

    print(f"\n\n-- Joueur {actuelJoueur} - Tour {nbTour} - Minimun : {valeurMin} - Dernier Joueur : {dernierJoueur} --")
    game.joueurs[actuelJoueur].trierMain()
    print(game.joueurs[actuelJoueur].main)
    print("Voici votre main:",
        "\nVos combinaisons simples :", game.joueurs[actuelJoueur].aCombinaison(1),
        "\nVos combinaisons paires :", game.joueurs[actuelJoueur].aCombinaison(2),
        "\nVos combinaisons brelans :", game.joueurs[actuelJoueur].aCombinaison(3),
        "\nVos combinaisons carrés :", game.joueurs[actuelJoueur].aCombinaison(4))
    
    if nbTour == 0:
        typePli = demander(["typePli", game.joueurs[actuelJoueur]])

    if game.joueurs[actuelJoueur].aCombinaison(typePli) != []:
        if max(game.joueurs[actuelJoueur].aCombinaison(typePli)) < valeurMin:
            game.joueurs[actuelJoueur].peutJouer = False
            input("Vous ne pouvez pas jouer le pli actuel !")
        else:
            while True:
                print(game.joueurs[actuelJoueur].main)
                entree = input("Quelles cartes voulez-vous jouer?\n>")

                cartesJouees = parserCartes(entree, game.joueurs[actuelJoueur], typePli, valeurMin)
                if cartesJouees is not None:
                    #TODO Fallback error handling in parse
                    break
                print("Veuillez réessayer.")
            
            valeurMin = cartesJouees[0].valeur

            print("Vous jouez :", cartesJouees)
            game.joueurs[actuelJoueur].retirerCartes(cartesJouees)
            dernierJoueur = actuelJoueur
    else:
        game.joueurs[actuelJoueur].peutJouer = False
        input("Vous ne pouvez pas jouer le pli actuel !")

    etatJoueur = []
    for j in game.joueurs:
        etatJoueur.append(j.peutJouer)
    print(etatJoueur)
    if absListe(etatJoueur) == False:
        print(f"Plus personne ne peut jouer le pli ! Dernier joueur : {dernierJoueur}")

    nbTour += 1
    if actuelJoueur < 3:
        actuelJoueur += 1
    else:
        actuelJoueur = 0
    