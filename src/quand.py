"""Axe Quand : accidents graves par heure, jour, mois, année, et test de H1."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.cleaning import load_idf

FIG = Path("figures")
FIG.mkdir(exist_ok=True)

# --- 1. Table au niveau accident -------------------------------------------
t = load_idf()
c = t["caracteristiques"].copy()
u = t["usagers"]

# grav : 1 indemne, 2 tué, 3 blessé hospitalisé, 4 blessé léger
# accident grave = au moins un usager tué (2) ou hospitalisé (3)
grave = u.assign(g=u["grav"].isin([2, 3])).groupby("Num_Acc")["g"].max()
acc = c.merge(grave.rename("grave"), on="Num_Acc", how="left")
acc["grave"] = acc["grave"].fillna(False).astype(int)

acc["heure"] = pd.to_numeric(acc["heure"], errors="coerce")
date = pd.to_datetime(
    {"year": acc["an"], "month": acc["mois"], "day": acc["jour"]}, errors="coerce"
)
acc["jour_semaine"] = date.dt.dayofweek  # 0 = lundi

print("Accidents :", len(acc), "| dont graves :", acc["grave"].sum())

g = acc[acc["grave"] == 1]


def barres(serie, titre, fichier, etiquettes=None, couleurs=None, xlabel=""):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = etiquettes if etiquettes is not None else serie.index
    ax.bar([str(v) for v in x], serie.values, color=couleurs or "#2b6cb0")
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Accidents graves")
    ax.text(0.99, -0.18, "Source : ONISR, IDF 2019-2024", transform=ax.transAxes,
            ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / fichier, dpi=150)
    plt.close(fig)


# --- 2. Quatre graphiques ----------------------------------------------------
par_heure = g["heure"].value_counts().sort_index()
barres(par_heure, "Accidents graves par heure", "quand_heure.png", xlabel="Heure")

jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
par_jour = g["jour_semaine"].value_counts().sort_index()
barres(par_jour, "Accidents graves par jour de la semaine", "quand_jour.png",
       etiquettes=[jours[int(i)] for i in par_jour.index])

mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
par_mois = g["mois"].value_counts().sort_index()
barres(par_mois, "Accidents graves par mois", "quand_mois.png",
       etiquettes=[mois[int(i) - 1] for i in par_mois.index])

par_an = g["an"].value_counts().sort_index()
barres(par_an, "Accidents graves par année (2020 = confinement)", "quand_annee.png",
       couleurs=["#c53030" if int(a) == 2020 else "#2b6cb0" for a in par_an.index])

# --- 3. H1 : taux de gravité nuit vs jour -----------------------------------
# lum : 1 plein jour, 2 crépuscule/aube, 3-5 nuit
acc["periode"] = acc["lum"].map(
    {1: "Jour", 2: "Crépuscule/aube", 3: "Nuit", 4: "Nuit", 5: "Nuit"}
)
h1 = acc.groupby("periode")["grave"].agg(["sum", "count", "mean"])
h1.columns = ["graves", "accidents", "taux"]
h1["taux"] = (h1["taux"] * 100).round(1)
print("\nH1 : taux de gravité par période (%)")
print(h1)

h1 = h1.reindex(["Jour", "Crépuscule/aube", "Nuit"])
fig, ax = plt.subplots(figsize=(6, 4.5))
barres_h1 = ax.bar(h1.index, h1["taux"], color=["#2b6cb0", "#718096", "#1a365d"])
ax.bar_label(barres_h1, fmt="%.1f %%", padding=3)
ax.set_title("Part d'accidents graves selon la luminosité")
ax.set_ylabel("% d'accidents graves")
ax.set_ylim(0, 18)
ax.text(0.99, -0.12, "Source : ONISR, IDF 2019-2024", transform=ax.transAxes,
        ha="right", fontsize=8)
fig.tight_layout()
fig.savefig(FIG / "quand_h1_nuit.png", dpi=150)
plt.close(fig)

# --- 4. Chiffres à citer dans les slides ------------------------------------
print("\nHeure du pic :", par_heure.idxmax(), "->", par_heure.max())
print("Jour du pic :", jours[int(par_jour.idxmax())], "->", par_jour.max())
print("Mois du pic :", mois[int(par_mois.idxmax()) - 1], "->", par_mois.max())
print("\nPar année :\n", par_an)
print("\nFigures enregistrées dans", FIG.resolve())