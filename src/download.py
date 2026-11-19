"""Récupération des fichiers BAAC 2019-2024 depuis data.gouv.fr vers data/raw/."""

import re
from datetime import date
from pathlib import Path

import requests

API_URL = "https://www.data.gouv.fr/api/1/datasets/53698f4ca3a729239d2036df/"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
ANNEES = range(2019, 2025)
TYPES = ("caracteristiques", "lieux", "vehicules", "usagers")

# Les titres varient selon l'année : caracteristiques-2019, carcteristiques-2021,
# Caract_2024, Lieux_2024. Les vehicules-immatricules-baac-* ne correspondent pas.
TITRE = re.compile(
    r"^(cara?ct\w*|lieux|vehicules|usagers)[-_](\d{4})\.csv$", re.IGNORECASE
)


def lister_fichiers():
    """Renvoie {(type, année): url} pour les 24 fichiers de la période."""
    reponse = requests.get(API_URL, timeout=30)
    reponse.raise_for_status()

    fichiers = {}
    for ressource in reponse.json()["resources"]:
        trouve = TITRE.match(ressource["title"])
        if not trouve:
            continue
        nom, annee = trouve.group(1).lower(), int(trouve.group(2))
        if annee not in ANNEES:
            continue
        type_ = "caracteristiques" if nom.startswith("car") else nom
        if (type_, annee) in fichiers:
            raise ValueError(f"Deux fichiers pour {type_} {annee}")
        fichiers[(type_, annee)] = ressource["url"]

    manquants = [(t, a) for t in TYPES for a in ANNEES if (t, a) not in fichiers]
    if manquants:
        raise ValueError(f"Fichiers introuvables sur data.gouv.fr : {manquants}")
    return fichiers


def telecharger(url, chemin):
    # Écrit d'abord dans un .part pour ne jamais laisser un fichier tronqué à son nom final.
    partiel = chemin.with_suffix(".part")
    with requests.get(url, stream=True, timeout=60) as reponse:
        reponse.raise_for_status()
        with open(partiel, "wb") as f:
            f.writelines(reponse.iter_content(chunk_size=1024 * 1024))
    partiel.rename(chemin)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fichiers = lister_fichiers()

    nouveaux = 0
    for (type_, annee), url in sorted(fichiers.items()):
        chemin = RAW_DIR / f"{type_}-{annee}.csv"
        if chemin.exists():
            print(f"déjà présent : {chemin.name}")
            continue
        print(f"téléchargement : {chemin.name}")
        telecharger(url, chemin)
        nouveaux += 1

    if nouveaux:
        (RAW_DIR / "date_telechargement.txt").write_text(
            date.today().isoformat() + "\n"
        )
    date_fichier = (RAW_DIR / "date_telechargement.txt").read_text().strip()
    print(f"{nouveaux} fichier(s) téléchargé(s), données du {date_fichier}")


if __name__ == "__main__":
    main()
