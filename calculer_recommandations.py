import pandas as pd

from src.lancement import charger_emprunts
from src.item_to_item import ItemToItem
from src.user_to_user import UserToUser
from src.contenu import Contenu
from src.melange_trois import MelangeTrois

historique = charger_emprunts()
lecteurs = [lecteur for lecteur in historique]

modeles = {
    "item_to_item": ItemToItem(),
    "user_to_user": UserToUser(),
    "contenu": Contenu(300),
    "melange": MelangeTrois([0.64, 0.16, 0.2]),
}

for nom in modeles:
    modele = modeles[nom]
    modele.fit(historique)
    tableau = pd.DataFrame({"lecteur": lecteurs, "recommandation": [" ".join(str(livre) for livre in modele.recommander(lecteur)) for lecteur in lecteurs]})
    tableau.to_csv("recommandations/" + nom + ".csv", index=False)
    print("recommandations/" + nom + ".csv créé")
