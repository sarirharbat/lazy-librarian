import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from src.lancement import charger_emprunts
from tentatives_non_retenues_pour_non_conformite_aux_consignes.clustering import representer

historique = charger_emprunts()
X = representer(historique)

inerties = []
for k in range(2, 51):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0)
    kmeans.fit(X)
    inerties.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(2, 51), inerties, marker="o")
plt.title("Méthode du coude")
plt.xlabel("Nombre de groupes k")
plt.ylabel("Inertie")
plt.savefig("tentatives_non_retenues_pour_non_conformite_aux_consignes/coude.png")
