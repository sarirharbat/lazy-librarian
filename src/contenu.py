import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.popularity import Popularite


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class Contenu:

    def __init__(self, nb_candidats):
        self.nb_candidats = nb_candidats

    def fit(self, historique):
        self.historique = historique
        self.populaires = Popularite()
        self.populaires.fit(historique)

        livres = pd.read_csv("data/items.csv")
        livres = livres.fillna("")
        textes = livres["Title"] + " " + livres["Author"] + " " + livres["Subjects"]
        tfidf = TfidfVectorizer()
        self.X = tfidf.fit_transform(textes)

        self.numeros = list(livres["i"])
        self.position = {}
        for n in range(len(self.numeros)):
            self.position[self.numeros[n]] = n

    def points(self, lecteur):
        lignes = [self.position[livre] for livre in self.historique[lecteur]]
        similarite = cosine_similarity(self.X[lignes], self.X).sum(axis=0)
        meilleurs = np.argsort(-similarite, kind="stable")[:self.nb_candidats]
        return {self.numeros[n]: similarite[n] for n in meilleurs if similarite[n] > 0}

    def recommander(self, lecteur):
        return classer(self.points(lecteur), self.populaires.top_10)[:10]
