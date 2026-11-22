import pandas as pd


def charger_emprunts():
    emprunts = pd.read_csv("data/interactions.csv")
    emprunts = emprunts.sort_values("t")

    historique = {}
    for lecteur, groupe in emprunts.groupby("u"):
        historique[lecteur] = list(groupe["i"])
    return historique


def lancer(modele, numero):
    historique = charger_emprunts()
    modele.fit(historique)

    soumission = pd.read_csv("data/sample_submission.csv")
    soumission["recommendation"] = [" ".join(str(livre) for livre in modele.recommander(lecteur)) for lecteur in soumission["user_id"]]
    soumission.to_csv("submissions/tentative_" + str(numero) + ".csv", index=False)
    print("submissions/tentative_" + str(numero) + ".csv créé")
