import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.popularity import Popularite


def ajouter(compteur, cle, valeur):
    if cle not in compteur:
        compteur[cle] = 0
    compteur[cle] = compteur[cle] + valeur


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


def representer(historique):
    livres = pd.read_csv("data/items.csv")
    livres = livres[["i", "Subjects"]]
    livres = livres.dropna()
    sujets = {}
    for n in range(len(livres)):
        sujets[livres["i"].values[n]] = livres["Subjects"].values[n]

    textes = [" ".join(sujets[livre] for livre in historique[lecteur] if livre in sujets) for lecteur in historique]
    tfidf = TfidfVectorizer()
    return tfidf.fit_transform(textes)


class Clustering:

    def __init__(self, nb_groupes):
        self.nb_groupes = nb_groupes

    def fit(self, historique):
        self.historique = historique
        self.populaires = Popularite()
        self.populaires.fit(historique)

        X = representer(historique)
        kmeans = KMeans(n_clusters=self.nb_groupes, n_init=10, random_state=0)
        kmeans.fit(X)
        groupes = kmeans.predict(X)

        lecteurs = [lecteur for lecteur in historique]
        self.groupe = {}
        self.membres = {}
        for n in range(len(lecteurs)):
            lecteur = lecteurs[n]
            groupe = groupes[n]
            self.groupe[lecteur] = groupe
            if groupe not in self.membres:
                self.membres[groupe] = []
            self.membres[groupe].append(lecteur)

    def points(self, lecteur):
        points = {}
        for membre in self.membres[self.groupe[lecteur]]:
            for livre in self.historique[membre]:
                ajouter(points, livre, 1)
        return points

    def recommander(self, lecteur):
        return classer(self.points(lecteur), self.populaires.top_10)[:10]
