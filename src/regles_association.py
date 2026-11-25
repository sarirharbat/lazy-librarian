import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from src.popularity import Popularite


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class ReglesAssociation:

    def __init__(self, confiance_min):
        self.confiance_min = confiance_min

    def fit(self, historique):
        self.historique = historique
        self.populaires = Popularite()
        self.populaires.fit(historique)

        lecteurs = []
        livres = []
        for lecteur in historique:
            for livre in historique[lecteur]:
                lecteurs.append(lecteur)
                livres.append(livre)
        emprunts = pd.DataFrame({"lecteur": lecteurs, "livre": livres})
        panier = pd.crosstab(emprunts["lecteur"], emprunts["livre"]).astype(bool)

        frequents = fpgrowth(panier, min_support=2 / len(panier), use_colnames=True, max_len=2)
        regles = association_rules(frequents, metric="confidence", min_threshold=self.confiance_min)
        regles = regles[regles["lift"] > 1]

        self.regles = {}
        for n in range(len(regles)):
            a = list(regles["antecedents"].values[n])[0]
            b = list(regles["consequents"].values[n])[0]
            if a not in self.regles:
                self.regles[a] = []
            self.regles[a].append([b, regles["confidence"].values[n]])

    def points(self, lecteur):
        points = {}
        for livre in self.historique[lecteur]:
            if livre in self.regles:
                for autre, confiance in self.regles[livre]:
                    if autre not in self.historique[lecteur]:
                        if autre not in points or confiance > points[autre]:
                            points[autre] = confiance
        return points

    def recommander(self, lecteur):
        return classer(self.points(lecteur), self.populaires.top_10)[:10]
