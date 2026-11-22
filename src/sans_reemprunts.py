from src.item_to_item import ItemToItem


class SansReemprunts(ItemToItem):

    def points(self, lecteur):
        points = ItemToItem.points(self, lecteur)
        return {livre: points[livre] for livre in points if livre not in self.historique[lecteur]}
