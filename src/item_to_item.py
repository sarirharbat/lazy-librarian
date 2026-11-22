import pandas as pd
from src.popularity import Popularite


def ajouter(compteur, cle, valeur):
    if cle not in compteur:
        compteur[cle] = 0
    compteur[cle] = compteur[cle] + valeur


def sans_doublons(livres):
    uniques = []
    for livre in livres:
        if livre not in uniques:
            uniques.append(livre)
    return uniques


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class ItemToItem:

    def fit(self, historique):
        self.historique = historique
        self.populaires = Popularite()
        self.populaires.fit(historique)

        nb_lecteurs = {}
        ensemble = {}
        for lecteur in historique:
            livres = sans_doublons(historique[lecteur])
            for a in livres:
                ajouter(nb_lecteurs, a, 1)
                for b in livres:
                    ajouter(ensemble, (a, b), 1)

        self.proches = {}
        for a, b in ensemble:
            if a not in self.proches:
                self.proches[a] = {}
            self.proches[a][b] = ensemble[(a, b)] / (nb_lecteurs[a] * nb_lecteurs[b]) ** 0.5

    def points(self, lecteur):
        points = {}
        for livre in self.historique[lecteur]:
            for proche in self.proches[livre]:
                ajouter(points, proche, self.proches[livre][proche])
        return points

    def recommander(self, lecteur):
        return classer(self.points(lecteur), self.populaires.top_10)[:10]
