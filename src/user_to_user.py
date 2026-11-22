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


class UserToUser:

    def fit(self, historique):
        self.historique = historique
        self.populaires = Popularite()
        self.populaires.fit(historique)

        nb_livres = {}
        lecteurs_du_livre = {}
        for lecteur in historique:
            for livre in sans_doublons(historique[lecteur]):
                ajouter(nb_livres, lecteur, 1)
                if livre not in lecteurs_du_livre:
                    lecteurs_du_livre[livre] = []
                lecteurs_du_livre[livre].append(lecteur)

        ensemble = {}
        for livre in lecteurs_du_livre:
            for a in lecteurs_du_livre[livre]:
                for b in lecteurs_du_livre[livre]:
                    ajouter(ensemble, (a, b), 1)

        self.proches = {}
        for a, b in ensemble:
            if a not in self.proches:
                self.proches[a] = {}
            self.proches[a][b] = ensemble[(a, b)] / (nb_livres[a] * nb_livres[b]) ** 0.5

    def points(self, lecteur):
        points = {}
        for proche in self.proches[lecteur]:
            for livre in self.historique[proche]:
                ajouter(points, livre, self.proches[lecteur][proche])
        return points

    def recommander(self, lecteur):
        return classer(self.points(lecteur), self.populaires.top_10)[:10]
