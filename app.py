import pandas as pd
import streamlit as st

from src.lancement import charger_emprunts
from src.item_to_item import ItemToItem

st.title("The Lazy Librarian")

historique = charger_emprunts()
livres = pd.read_csv("data/items.csv")

modele = ItemToItem()
modele.fit(historique)

lecteur = st.selectbox("Lecteur", [lecteur for lecteur in historique])
st.write("Modèle : item-to-item")

for numero in modele.recommander(lecteur):
    livre = livres[livres["i"] == numero]
    st.write(livre["Title"].values[0], "-", livre["Author"].values[0])
