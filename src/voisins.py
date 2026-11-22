import pandas as pd
from src.item_to_item import ItemToItem


def classer(points, a_ajouter):
    tableau = pd.DataFrame({"livre": [livre for livre in points], "points": [points[livre] for livre in points]})
    tableau = tableau.sort_values(["points", "livre"], ascending=False)
    choix = [livre for livre in tableau["livre"]]
    return choix + [livre for livre in a_ajouter if livre not in choix]


class Voisins(ItemToItem):

    def __init__(self, k):
        self.k = k

    def fit(self, historique):
        ItemToItem.fit(self, historique)
        for livre in self.proches:
            gardes = classer(self.proches[livre], [])[:self.k]
            self.proches[livre] = {proche: self.proches[livre][proche] for proche in gardes}
