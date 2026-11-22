import pandas as pd

# lecture les emprunts 
emprunts = pd.read_csv("data/interactions.csv")

print(emprunts.head())
emprunts.info()


#bloc 1 : volume et sparsite
nb_emprunts =len(emprunts)
nb_lecteurs = emprunts['u'].nunique()
nb_livres = emprunts['i'].nunique()

remplissage = nb_emprunts / (nb_lecteurs * nb_livres) *100

print("Emprunts : ", nb_emprunts)
print("Lecteurs : ", nb_lecteurs)
print("Livres : ", nb_livres)
print("Remplissage : ", round (remplissage, 3), "%")



# bloc 2 : emprunt par lecteur
par_lecteur = emprunts.groupby('u').size()

print(par_lecteur.describe())

print("Lecteur a 5 emprunts ou moins : ", (par_lecteur <= 5).sum())
print("soit", round((par_lecteur <= 5).mean() * 100, 1), "%")


#bloc 3 : emprunt par livre
par_livre = emprunts.groupby('i').size()

print(par_livre.describe())

print("Livre empruntes une seule fois : ", (par_livre == 1).sum())
print("soit", round((par_livre == 1).mean() * 100, 1), "%")

print("Livre empruntes 5 fois ou moins : ", (par_livre <= 5).sum())
print("soit", round((par_livre <= 5).mean() * 100, 1), "%")
top_100 = par_livre.sort_values(ascending=False).head(100)
print("Part des emprunts captee par le top 100: ", round(top_100.sum() / nb_emprunts * 100, 1), "%")


# bloc 4 : les reemprunts
reemprunts = emprunts.duplicated(subset=['u', 'i'])

print("Lignes qui sont un reemprunt : ", reemprunts.sum())
print("soit", round(reemprunts.mean() * 100, 1), "%")

livres_differents = emprunts.groupby('u')['i'].nunique()
print("Lecteurs ayant au moins un reemprunt : ", (par_lecteur > livres_differents).sum())
print("soit", round((par_lecteur > livres_differents).mean() * 100, 1), "%")