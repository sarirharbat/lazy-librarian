from tentatives_non_retenues_pour_non_conformite_aux_consignes.melange_complet import MelangeComplet
from src.contenu import Contenu


class MelangeContenu(MelangeComplet):

    def fit(self, historique):
        MelangeComplet.fit(self, historique)
        contenu = Contenu(300)
        contenu.fit(historique)
        self.modeles.append(contenu)
