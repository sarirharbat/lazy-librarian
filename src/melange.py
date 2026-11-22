import pandas as pd
from src.item_to_item import ItemToItem
from src.user_to_user import UserToUser


def ajouter(compteur, cle, valeur):
    if cle not in compteur:
        compteur[cle] = 0
    compteur[cle] = compteur[cle] + valeur


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class Melange:

    def __init__(self, poids):
        self.poids = poids

    def fit(self, historique):
        self.livres = ItemToItem()
        self.livres.fit(historique)
        self.lecteurs = UserToUser()
        self.lecteurs.fit(historique)

    def recommander(self, lecteur):
        points_livres = self.livres.points(lecteur)
        points_lecteurs = self.lecteurs.points(lecteur)
        max_livres = points_livres[classer(points_livres, [])[0]]
        max_lecteurs = points_lecteurs[classer(points_lecteurs, [])[0]]

        points = {}
        for livre in points_livres:
            ajouter(points, livre, self.poids * points_livres[livre] / max_livres)
        for livre in points_lecteurs:
            ajouter(points, livre, (1 - self.poids) * points_lecteurs[livre] / max_lecteurs)
        return classer(points, self.livres.populaires.top_10)[:10]
