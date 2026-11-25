import pandas as pd
from src.item_to_item import ItemToItem
from src.user_to_user import UserToUser
from src.regles_association import ReglesAssociation
from src.clustering import Clustering


def ajouter(compteur, cle, valeur):
    if cle not in compteur:
        compteur[cle] = 0
    compteur[cle] = compteur[cle] + valeur


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class MelangeComplet:

    def __init__(self, poids):
        self.poids = poids

    def fit(self, historique):
        self.livres = ItemToItem()
        self.modeles = [self.livres, UserToUser(), ReglesAssociation(0.35), Clustering(11)]
        for modele in self.modeles:
            modele.fit(historique)

    def recommander(self, lecteur):
        points = {}
        for n in range(len(self.modeles)):
            points_modele = self.modeles[n].points(lecteur)
            if len(points_modele) > 0:
                maximum = points_modele[classer(points_modele, [])[0]]
                for livre in points_modele:
                    ajouter(points, livre, self.poids[n] * points_modele[livre] / maximum)
        return classer(points, self.livres.populaires.top_10)[:10]
