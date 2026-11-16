# Sécurité routière en Île-de-France

## Contexte

Commanditaire : observatoire de la sécurité routière, qui prépare sa prochaine campagne de prévention. Il veut savoir quand, où et dans quelles conditions surviennent les accidents graves, et quels usagers sont les plus touchés.

Sujet retenu : n°2, accidentalité routière (annexe A du cahier des charges CDC-DIA2-UE01-2026).

## Questions analytiques

1. Quand : à quelles heures, quels jours et quels mois les accidents graves surviennent-ils, et leur nombre évolue-t-il entre 2019 et 2024 ?
2. Où : quels départements et quels types de voie concentrent les accidents graves, rapportés à la population ?
3. Conditions : la vitesse autorisée, la lumière, la météo, l'état de la chaussée et le type de collision sont-ils associés à des accidents plus graves ?
4. Qui : quels usagers sont les plus touchés selon leur mode de déplacement, leur âge et leur place ?

Les définitions, les colonnes utilisées et les hypothèses testées sont dans [`docs/questions.md`](docs/questions.md).

## Données

| | |
|---|---|
| Jeu de données | [Bases de données annuelles des accidents corporels de la circulation routière](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024/) |
| Producteur | ONISR (Observatoire national interministériel de la sécurité routière) |
| Licence | Licence Ouverte Etalab 2.0 |
| Fichiers | caractéristiques, lieux, véhicules, usagers ; un fichier de chaque par année |
| Périmètre retenu | Île-de-France (75, 77, 78, 91, 92, 93, 94, 95), 2019 à 2024 |
| Date de téléchargement | à compléter au premier lancement de `src/download.py` |

Les fichiers bruts ne sont pas versionnés. `src/download.py` les place dans `data/raw/`.

Anomalies relevées et leur traitement : [`docs/anomalies.md`](docs/anomalies.md). Choix de méthode : [`docs/decisions.md`](docs/decisions.md).

## Installation

Python 3.11 ou plus récent.

```bash
git clone https://github.com/lounielyas709-stack/projet1-securite-routiere-idf.git
cd projet1-securite-routiere-idf
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS et Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduire l'analyse

1. Télécharger les données : `python src/download.py`
2. Exécuter `notebooks/01_exploration.ipynb`
3. Lancer le tableau de bord : `streamlit run app/dashboard.py`

## Résultats principaux

À venir.

## Limites

- La base ne recense que les accidents corporels relevés par les forces de l'ordre. Un accident sans blessé, ou sans intervention de la police ou de la gendarmerie, n'y figure pas.
- 2020 est une année de confinement : le trafic y est plus faible, et elle ne se compare pas directement aux autres.
- Paris accueille chaque jour bien plus de personnes qu'il n'y en habite, donc un taux par habitant y surestime le risque.
- Une association entre un facteur et la gravité ne prouve pas que ce facteur en est la cause.

## Équipe

| Membre | Rôle | Axe d'analyse | GitHub |
|---|---|---|---|
| Elyas Louni | Chef de projet, chargement et nettoyage | Où | [lounielyas709-stack](https://github.com/lounielyas709-stack) |
| Alex | à définir | à définir | |
| David | à définir | à définir | |
| Selyan | à définir | à définir | |
