import pandas as pd
import streamlit as st

st.title("The Lazy Librarian")

livres = pd.read_csv("data/items.csv")
livres = livres.fillna("")
emprunts = pd.read_csv("data/interactions.csv")
recommandations = pd.read_csv("recommandations/item_to_item.csv")

profils = {
    "Lecteur de mangas (n° 991)": 991,
    "Lecteur en soins infirmiers (n° 392)": 392,
    "Nouveau lecteur en droit pénal, 3 emprunts (n° 3089)": 3089,
}

choix = st.radio("Lecteur", list(profils) + ["Autre lecteur"])
if choix == "Autre lecteur":
    lecteur = st.number_input("Numéro du lecteur", min_value=0, max_value=int(recommandations["lecteur"].max()), step=1)
else:
    lecteur = profils[choix]

deja = emprunts[emprunts["u"] == lecteur]
deja = pd.merge(deja, livres, on="i", how="left")
deja = deja.sort_values("t", ascending=False)
tableau = pd.DataFrame({"Date": pd.to_datetime(deja["t"], unit="s"), "Titre": [titre.rstrip(" /") for titre in deja["Title"]], "Auteur": deja["Author"]})

st.subheader("Déjà empruntés (" + str(len(deja)) + ")")
st.dataframe(tableau, hide_index=True)

st.subheader("Recommandations")
st.write("Modèle : item-to-item")

ligne = recommandations[recommandations["lecteur"] == lecteur]
numeros = ligne["recommandation"].values[0].split(" ")
for n in range(len(numeros)):
    livre = livres[livres["i"] == int(numeros[n])]
    titre = livre["Title"].values[0].rstrip(" /")
    auteur = livre["Author"].values[0]
    sujets = "; ".join(livre["Subjects"].values[0].split("; ")[:4])
    st.write(str(n + 1) + ". **" + titre + "**")
    st.caption(" | ".join(texte for texte in [auteur, sujets] if texte != ""))
