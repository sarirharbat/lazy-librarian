import pandas as pd

from src.lancement import charger_emprunts
from src.item_to_item import ItemToItem
from src.user_to_user import UserToUser
from src.contenu import Contenu
from src.melange_trois import MelangeTrois
from src.explications import expliquer

historique = charger_emprunts()

modeles = {
    "item_to_item": ItemToItem(),
    "user_to_user": UserToUser(),
    "contenu": Contenu(300),
    "melange": MelangeTrois([0.64, 0.16, 0.2]),
}

for nom in modeles:
    modele = modeles[nom]
    modele.fit(historique)
    colonnes = {"lecteur": [], "rang": [], "livre": [], "raison": [], "source": []}
    for lecteur in historique:
        livres = modele.recommander(lecteur)
        raisons = expliquer(nom, modele, historique, lecteur, livres)
        for n in range(len(livres)):
            colonnes["lecteur"].append(lecteur)
            colonnes["rang"].append(n + 1)
            colonnes["livre"].append(livres[n])
            colonnes["raison"].append(raisons[n][0])
            colonnes["source"].append(raisons[n][1])
    tableau = pd.DataFrame(colonnes)
    tableau.to_csv("recommandations/" + nom + ".csv", index=False)
    print("recommandations/" + nom + ".csv créé")
