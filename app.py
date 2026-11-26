import pandas as pd
import streamlit as st

st.title("The Lazy Librarian")

livres = pd.read_csv("data/items.csv")
livres = livres.fillna("")
emprunts = pd.read_csv("data/interactions.csv")


def titre(numero):
    livre = livres[livres["i"] == numero]
    return livre["Title"].values[0].rstrip(" /")


def pourquoi(raison, source):
    if raison == "deja" and source == 1:
        return "Tu l'as déjà emprunté."
    if raison == "deja":
        return "Tu l'as déjà emprunté " + str(source) + " fois."
    if raison == "livre":
        return "Souvent emprunté avec « " + titre(source) + " », que tu as emprunté."
    if raison == "contenu":
        return "Ressemble à « " + titre(source) + " », que tu as emprunté."
    if raison == "lecteurs" and source == 1:
        return "Emprunté par 1 lecteur qui a des livres en commun avec toi."
    if raison == "lecteurs":
        return "Emprunté par " + str(source) + " lecteurs qui ont des livres en commun avec toi."
    return "Un des livres les plus empruntés de la bibliothèque."


profils = {
    "Lecteur de mangas (n° 991)": 991,
    "Lecteur en soins infirmiers (n° 392)": 392,
    "Nouveau lecteur en droit pénal, 3 emprunts (n° 3089)": 3089,
}

choix = st.radio("Lecteur", list(profils) + ["Autre lecteur"])
if choix == "Autre lecteur":
    lecteur = st.number_input("Numéro du lecteur", min_value=0, max_value=int(emprunts["u"].max()), step=1)
else:
    lecteur = profils[choix]

modeles = {
    "Mélange item-to-item, user-to-user et contenu": ["melange", "0.16800"],
    "Item-to-item": ["item_to_item", "0.16373"],
    "User-to-user": ["user_to_user", "0.15366"],
    "Contenu (titre, auteur, sujets)": ["contenu", "0.14480"],
}

nom = st.selectbox("Modèle", list(modeles))
fichier, score = modeles[nom]
recommandations = pd.read_csv("recommandations/" + fichier + ".csv")

deja = emprunts[emprunts["u"] == lecteur]
deja = pd.merge(deja, livres, on="i", how="left")
deja = deja.sort_values("t", ascending=False)
tableau = pd.DataFrame({"Date": pd.to_datetime(deja["t"], unit="s"), "Titre": [titre(numero) for numero in deja["i"]], "Auteur": deja["Author"]})

st.subheader("Déjà empruntés (" + str(len(deja)) + ")")
st.dataframe(tableau, hide_index=True)

st.subheader("Recommandations")
st.write("Modèle utilisé : **" + nom + "** (score Kaggle " + score + ")")

top = recommandations[recommandations["lecteur"] == lecteur]
for n in range(len(top)):
    numero = top["livre"].values[n]
    livre = livres[livres["i"] == numero]
    auteur = livre["Author"].values[0]
    sujets = "; ".join(livre["Subjects"].values[0].split("; ")[:4])
    st.write(str(top["rang"].values[n]) + ". **" + titre(numero) + "**")
    st.write("Pourquoi : " + pourquoi(top["raison"].values[n], top["source"].values[n]))
    st.caption(" | ".join(texte for texte in [auteur, sujets] if texte != ""))
