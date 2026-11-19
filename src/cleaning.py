"""Chargement, typage et nettoyage des 4 fichiers BAAC, restreints à l'Île-de-France.

Usage :
    from src.cleaning import load_idf
    tables = load_idf()
    tables["usagers"]

Les traitements appliqués renvoient aux entrées de docs/anomalies.md (ANO-xx).
"""

from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
RAW_DIR = RACINE / "data" / "raw"
PROCESSED_DIR = RACINE / "data" / "processed"
ANNEES = range(2019, 2025)
TYPES = ("caracteristiques", "lieux", "vehicules", "usagers")
DEPARTEMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]

# Valeurs qui veulent dire « non renseigné » une fois les espaces retirés (ANO-05, ANO-11).
VALEURS_VIDES = ["", "-", "N/A", "(1)"]

# Colonnes de codes, converties en entiers. Les autres restent en texte (identifiants,
# adresse, numéro de voie...). id_vehicule contient des espaces insécables : il reste
# en texte, identique dans vehicules et usagers.
CODES = {
    "caracteristiques": ["jour", "mois", "an", "lum", "agg", "int", "atm", "col"],
    "lieux": [
        "catr", "circ", "nbv", "vosp", "prof", "plan", "surf", "infra", "situ", "vma",
    ],
    "vehicules": ["senc", "catv", "obs", "obsm", "choc", "manv", "motor", "occutc"],
    "usagers": [
        "place", "catu", "grav", "sexe", "an_nais", "trajet",
        "secu1", "secu2", "secu3", "locp", "etatp",
    ],
}  # fmt: skip

# Colonnes comptées pour choisir la ligne de lieux à garder (ANO-01).
COLONNES_LIEU = [
    "voie", "circ", "nbv", "vosp", "prof", "plan", "surf", "infra", "situ", "vma",
]  # fmt: skip


def lire(type_, annee):
    """Lit un fichier brut, tout en texte, sans espaces parasites."""
    df = pd.read_csv(RAW_DIR / f"{type_}-{annee}.csv", sep=";", dtype=str)
    df = df.rename(columns={"Accident_Id": "Num_Acc"})  # ANO-02
    df = df.apply(lambda colonne: colonne.str.strip())
    return df.replace(VALEURS_VIDES, pd.NA)


def typer_codes(df, colonnes):
    """Convertit les codes en entiers ; -1 (non renseigné) devient une valeur manquante."""
    for colonne in colonnes:
        valeurs = pd.to_numeric(df[colonne], errors="coerce").astype("Int64")
        df[colonne] = valeurs.mask(valeurs == -1)
    return df


def nettoyer_caracteristiques(df):
    df["dep"] = df["dep"].str.zfill(2)  # ANO-03
    df = df[df["dep"].isin(DEPARTEMENTS_IDF)].copy()
    df = typer_codes(df, CODES["caracteristiques"])  # mois sans zéro : ANO-04
    for colonne in ("lat", "long"):  # ANO-07
        df[colonne] = pd.to_numeric(df[colonne].str.replace(",", "."), errors="coerce")

    hors_idf = ~(df["lat"].between(48.0, 49.3) & df["long"].between(1.4, 3.6))  # ANO-13
    print(f"ANO-13 : {hors_idf.sum()} accidents aux coordonnées hors IDF mises à vide")
    df.loc[hors_idf, ["lat", "long"]] = pd.NA

    df["heure"] = pd.to_numeric(df["hrmn"].str[:2], errors="coerce").astype("Int64")
    return df


def nettoyer_lieux(df):
    df = typer_codes(df, CODES["lieux"])

    # ANO-08 : 130 est la limite la plus haute en France ; de 1 à 9, ce sont des saisies
    # isolées (1, 2, 3...) qui ne correspondent pas à une limitation de voie publique.
    improbable = (df["vma"] > 130) | (df["vma"] < 10)
    print(f"ANO-08 : {improbable.sum()} vitesses hors de 10-130 mises à vide")
    df["vma"] = df["vma"].mask(improbable)

    # ANO-01 : depuis 2023, une ligne par voie d'une intersection. On garde la plus
    # renseignée ; idxmax prend la première du fichier en cas d'égalité.
    renseignes = df[COLONNES_LIEU].notna().sum(axis=1)
    lignes_gardees = renseignes.groupby(df["Num_Acc"]).idxmax()
    print(
        f"ANO-01 : {len(df) - len(lignes_gardees)} lignes de lieux en double retirées"
    )
    return df.loc[lignes_gardees].reset_index(drop=True)


def nettoyer_usagers(df):
    df = typer_codes(df, CODES["usagers"])
    print(f"ANO-06 : {df['grav'].isna().sum()} usagers sans gravité")

    # ANO-09 : l'année de l'accident est dans les 4 premiers chiffres de Num_Acc.
    annee_accident = df["Num_Acc"].str[:4].astype("Int64")
    df["age"] = annee_accident - df["an_nais"]
    improbable = df["age"] > 100
    print(f"ANO-09 : {improbable.sum()} âges au-dessus de 100 ans mis à vide")
    df["age"] = df["age"].mask(improbable)
    df["an_nais"] = df["an_nais"].mask(improbable)
    return df


def construire():
    brut = {
        t: pd.concat([lire(t, a) for a in ANNEES], ignore_index=True) for t in TYPES
    }

    caracteristiques = nettoyer_caracteristiques(brut["caracteristiques"])
    accidents_idf = set(caracteristiques["Num_Acc"])

    def idf(df):
        return df[df["Num_Acc"].isin(accidents_idf)].copy()

    tables = {
        "caracteristiques": caracteristiques.reset_index(drop=True),
        "lieux": nettoyer_lieux(idf(brut["lieux"])),
        "vehicules": typer_codes(idf(brut["vehicules"]), CODES["vehicules"]),
        "usagers": nettoyer_usagers(idf(brut["usagers"])),
    }
    tables["vehicules"] = tables["vehicules"].reset_index(drop=True)
    tables["usagers"] = tables["usagers"].reset_index(drop=True)

    for nom in ("caracteristiques", "lieux"):
        if tables[nom]["Num_Acc"].duplicated().any():
            raise ValueError(f"{nom} : plusieurs lignes pour un même accident")
    return tables


def load_idf(reconstruire=False):
    """Renvoie {"caracteristiques", "lieux", "vehicules", "usagers"} pour l'IDF 2019-2024.

    Le premier appel lit les CSV de data/raw/ (lancer src/download.py avant) et enregistre
    le résultat en parquet dans data/processed/ ; les appels suivants relisent le parquet.
    reconstruire=True force la relecture des CSV, à faire après toute modification ici.
    """
    chemins = {t: PROCESSED_DIR / f"{t}.parquet" for t in TYPES}
    if not reconstruire and all(c.exists() for c in chemins.values()):
        return {t: pd.read_parquet(c) for t, c in chemins.items()}

    tables = construire()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for t, df in tables.items():
        df.to_parquet(chemins[t], index=False)
    return tables


if __name__ == "__main__":
    for nom, df in load_idf(reconstruire=True).items():
        print(f"{nom} : {len(df)} lignes, {df.shape[1]} colonnes")
