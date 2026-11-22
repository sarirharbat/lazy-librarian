import pandas as pd


def ajouter(compteur, cle, valeur):
    if cle not in compteur:
        compteur[cle] = 0
    compteur[cle] = compteur[cle] + valeur


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class Popularite:

    def fit(self, historique):
        nb_emprunts = {}
        for lecteur in historique:
            for livre in historique[lecteur]:
                ajouter(nb_emprunts, livre, 1)
        self.top_10 = classer(nb_emprunts, [])[:10]

    def recommander(self, lecteur):
        return self.top_10
