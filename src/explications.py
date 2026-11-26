import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def plus_grand(points):
    choix = None
    for cle in points:
        if choix is None or points[cle] > points[choix]:
            choix = cle
    return choix


def par_livre(modele, lecteur, livres):
    raisons = []
    for livre in livres:
        points = {}
        for emprunte in modele.historique[lecteur]:
            if livre in modele.proches[emprunte]:
                points[emprunte] = modele.proches[emprunte][livre]
        if len(points) > 0:
            raisons.append(["livre", plus_grand(points)])
        else:
            raisons.append(["populaire", 0])
    return raisons


def par_lecteurs(modele, lecteur, livres):
    nombre = {}
    for proche in modele.proches[lecteur]:
        if proche != lecteur:
            for livre in livres:
                if livre in modele.historique[proche]:
                    if livre not in nombre:
                        nombre[livre] = 0
                    nombre[livre] = nombre[livre] + 1
    raisons = []
    for livre in livres:
        if livre in nombre:
            raisons.append(["lecteurs", nombre[livre]])
        else:
            raisons.append(["populaire", 0])
    return raisons


def par_contenu(modele, lecteur, livres):
    lignes = [modele.position[emprunte] for emprunte in modele.historique[lecteur]]
    colonnes = [modele.position[livre] for livre in livres]
    similarite = cosine_similarity(modele.X[lignes], modele.X[colonnes])
    raisons = []
    for n in range(len(livres)):
        meilleur = np.argsort(-similarite[:, n], kind="stable")[0]
        if similarite[meilleur, n] > 0:
            raisons.append(["contenu", modele.historique[lecteur][meilleur]])
        else:
            raisons.append(["populaire", 0])
    return raisons


def par_melange(modele, historique, lecteur, livres):
    noms = ["item_to_item", "user_to_user", "contenu"]
    raisons = [["populaire", 0] for livre in livres]
    meilleure_part = [0 for livre in livres]
    for n in range(len(modele.modeles)):
        points = modele.modeles[n].points(lecteur)
        if len(points) > 0:
            maximum = points[plus_grand(points)]
            raisons_modele = expliquer(noms[n], modele.modeles[n], historique, lecteur, livres)
            for k in range(len(livres)):
                if livres[k] in points:
                    part = modele.poids[n] * points[livres[k]] / maximum
                    if part > meilleure_part[k]:
                        meilleure_part[k] = part
                        raisons[k] = raisons_modele[k]
    return raisons


def expliquer(nom, modele, historique, lecteur, livres):
    if nom == "item_to_item":
        raisons = par_livre(modele, lecteur, livres)
    elif nom == "user_to_user":
        raisons = par_lecteurs(modele, lecteur, livres)
    elif nom == "contenu":
        raisons = par_contenu(modele, lecteur, livres)
    else:
        raisons = par_melange(modele, historique, lecteur, livres)

    for n in range(len(livres)):
        fois = historique[lecteur].count(livres[n])
        if fois > 0:
            raisons[n] = ["deja", fois]
    return raisons
