# Questions analytiques

Version 1, à valider par le commanditaire (observatoire de la sécurité routière, sujet n°2 de l'annexe A).

## Besoin exprimé

« Nous préparons la campagne de prévention de l'an prochain. Nous voulons savoir quand, où et dans quelles conditions surviennent les accidents graves, et quels usagers sont les plus touchés. »

Périmètre : Île-de-France (75, 77, 78, 91, 92, 93, 94, 95), accidents corporels de 2019 à 2024.

## Définitions

- **Usager gravement touché** : usager tué ou blessé hospitalisé (`grav` = 2 ou 3).
- **Accident grave** : accident comptant au moins un usager gravement touché.
- **Taux de gravité** : part des usagers impliqués qui sont gravement touchés. Il permet de comparer des groupes de tailles très différentes.

## Q1. Quand

À quelles heures, quels jours et quels mois les accidents graves surviennent-ils, et leur nombre évolue-t-il entre 2019 et 2024 ?

- Colonnes : `hrmn`, `jour`, `mois`, `an` (caractéristiques), `lum`, `grav` (usagers)
- Hypothèse H1 : le taux de gravité est plus élevé la nuit que le jour.

## Q2. Où

Quels départements et quels types de voie concentrent les accidents graves, rapportés à la population ?

- Colonnes : `dep`, `com`, `agg` (caractéristiques), `catr` (lieux), population légale INSEE par département (jointure)
- Hypothèse H2 : le taux de gravité est plus élevé hors agglomération qu'en agglomération.

## Q3. Conditions

Les conditions de circulation (vitesse autorisée, lumière, météo, état de la chaussée, type de collision) sont-elles associées à des accidents plus graves ?

- Colonnes : `vma`, `surf` (lieux), `lum`, `atm`, `col` (caractéristiques)
- Hypothèse H3 : le taux de gravité augmente avec la vitesse maximale autorisée.

## Q4. Qui

Quels usagers sont les plus touchés selon leur mode de déplacement, leur âge et leur place ?

- Colonnes : `catu`, `grav`, `sexe`, `an_nais`, `place`, `secu1` (usagers), `catv` (véhicules)
- Hypothèse H4 : les usagers de deux-roues motorisés ont un taux de gravité plus élevé que les occupants de voiture.

## Q5. Passage de Paris à 30 km/h

Depuis le 30 août 2021, la vitesse est limitée à 30 km/h sur la plupart des rues de Paris. Les accidents ont-ils baissé plus vite à Paris que dans les départements voisins ?

- Colonnes : `dep`, `an`, `mois`, `jour` (caractéristiques), `grav` (usagers), `vma` (lieux) pour vérifier que la mesure apparaît dans les données
- Groupe de comparaison : la petite couronne (92, 93, 94), où le 30 km/h reste minoritaire (19 % des accidents en 2024 sur une voie à 30 km/h ou moins, contre 73 % à Paris)
- Hypothèse H5 : après septembre 2021, les accidents corporels et les tués baissent plus à Paris qu'en petite couronne.
- Méthode : comparaison avant et après entre les deux zones (différence de différences), sur les accidents corporels et les tués. Les accidents graves en sont exclus à cause de ANO-14.
- Limites : la période « avant » propre ne couvre que janvier 2019 à février 2020, puis le Covid perturbe tout jusqu'à mi-2021 ; nous n'avons pas de données de trafic, alors que la circulation automobile a baissé et le vélo a fortement augmenté à Paris ; Paris compte une trentaine de tués par an. Le résultat décrira une évolution, il ne prouvera pas l'effet de la mesure.

## Méthode de test

Chaque hypothèse est écrite ici avant le calcul (EF-05). H1 à H4 sont testées par comparaison de proportions (test du χ²), H5 par la méthode décrite dans Q5. Chacune est ensuite confirmée ou infirmée par écrit dans le notebook. Une association observée n'est pas présentée comme une cause.
