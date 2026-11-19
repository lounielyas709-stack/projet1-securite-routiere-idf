# Journal des anomalies

Repérées au premier chargement des fichiers 2019-2024. Les ampleurs portent sur la France entière ; elles seront recalculées par le code sur le périmètre Île-de-France. Aucune ligne n'est supprimée ou corrigée sans entrée ici.

## ANO-01. Plusieurs lignes par accident dans `lieux` à partir de 2023

- Colonnes concernées : `Num_Acc` (fichier lieux)
- Description : le fichier avait une ligne par accident jusqu'en 2022. Il en compte 70 860 pour 54 822 accidents en 2023, et 70 248 pour 54 402 en 2024.
- Ampleur : 31 884 lignes en trop sur 2023-2024, soit environ 23 % du fichier lieux de ces deux années. En Île-de-France, 5 987 accidents sur 15 943 en 2023 (37 %) et 5 581 sur 15 366 en 2024 (36 %).
- Cause probable : depuis 2023, une ligne par voie quand l'accident a lieu à une intersection. Tous les accidents IDF à plusieurs lignes sont en intersection (`int` différent de 1), contre environ 9 % de ceux à une seule ligne. La notice du 21/10/2026 décrit toujours `lieux` comme « le lieu principal de l'accident même si celui-ci s'est déroulé à une intersection » et ne mentionne pas ce changement.
- Traitement retenu : on garde une ligne par accident, celle qui a le plus de champs renseignés (`voie`, `circ`, `nbv`, `vosp`, `prof`, `plan`, `surf`, `infra`, `situ`, `vma`), et la première du fichier en cas d'égalité. La première ligne n'est la plus renseignée que dans 76 à 77 % des cas, et il lui manque `vma` dans 1 133 accidents IDF où une autre ligne l'a. Prendre le `vma` maximum aurait favorisé la route la plus rapide de l'intersection.
- Impact sur l'analyse : faible. `catr` ne varie jamais entre les lignes d'un même accident et `surf` dans 1 % des cas. Pour `vma`, la répartition par tranche change de moins d'un point selon la règle choisie (première ligne, maximum ou minimum). Sans ce traitement, une jointure directe compterait ces accidents deux fois ou plus.

## ANO-02. Clé d'accident renommée en 2022

- Colonnes concernées : `Accident_Id` (caractéristiques 2022), `Num_Acc` partout ailleurs
- Description : la clé de jointure change de nom pour une seule année.
- Ampleur : 55 302 accidents, toute l'année 2022.
- Cause probable : changement de nomenclature du producteur.
- Traitement retenu : renommée en `Num_Acc` au chargement.
- Impact sur l'analyse : aucun une fois renommée. Sans ce renommage, 2022 disparaît des jointures.

## ANO-03. Codes département sans zéro initial en 2019

- Colonnes concernées : `dep` (caractéristiques)
- Description : `"1"` au lieu de `"01"` pour une partie des accidents.
- Ampleur : 2 966 accidents en 2019, aucun les autres années.
- Cause probable : type numérique lors de l'export.
- Traitement retenu : complété à 2 caractères au chargement.
- Impact sur l'analyse : aucun sur l'Île-de-France (75 à 95 n'ont pas de zéro initial), mais à corriger pour toute comparaison nationale.

## ANO-04. Mois sans zéro initial en 2019 et 2020

- Colonnes concernées : `mois` (caractéristiques)
- Description : `"1"` et `"01"` cohabitent selon l'année.
- Ampleur : 43 484 accidents en 2019, 35 836 en 2020.
- Cause probable : changement de format d'export.
- Traitement retenu : converti en entier au chargement.
- Impact sur l'analyse : agrégations mensuelles fausses si le mois reste en texte.

## ANO-05. Code « non renseigné » `-1` précédé d'une espace

- Colonnes concernées : `vma`, `larrout`, `pr`, `pr1`, `v1`, `circ`, `nbv` (lieux) ; `secu2`, `secu3`, `locp`, `actp`, `etatp`, `sexe`, `trajet` (usagers)
- Description : la valeur brute est `" -1"`, que pandas ne reconnaît pas comme manquante.
- Ampleur : `vma` 3,2 %, `secu2` 40,6 %, `larrout` 69,7 %, `secu3` 97,3 %.
- Cause probable : convention de codification du producteur.
- Traitement retenu : espaces retirées et `-1` converti en valeur manquante.
- Impact sur l'analyse : moyennes et répartitions faussées si `-1` reste une valeur.

## ANO-06. Gravité non renseignée

- Colonnes concernées : `grav` (usagers)
- Description : `grav = -1` alors que la gravité est la variable centrale.
- Ampleur : 419 usagers (60 en 2021, 241 en 2022, 118 en 2023).
- Cause probable : saisie incomplète.
- Traitement retenu : ces usagers sont exclus du calcul des taux de gravité, et leur nombre est indiqué.
- Impact sur l'analyse : très faible sur les taux de gravité.

## ANO-07. Coordonnées avec virgule décimale

- Colonnes concernées : `lat`, `long` (caractéristiques)
- Description : `48,8962100` au lieu de `48.8962100`.
- Ampleur : 100 % des lignes.
- Cause probable : format régional français.
- Traitement retenu : virgule remplacée par un point, puis conversion en nombre.
- Impact sur l'analyse : carte impossible sans conversion.

## ANO-08. Vitesses maximales autorisées hors domaine

- Colonnes concernées : `vma` (lieux)
- Description : valeurs supérieures à 130 km/h, qui n'existent pas sur le réseau français.
- Ampleur : 95 lignes.
- Cause probable : erreur de saisie.
- Traitement retenu : ces lignes sont exclues de l'analyse par vitesse, et leur nombre est indiqué.
- Impact sur l'analyse : hypothèse H3.

## ANO-09. Années de naissance manquantes ou improbables

- Colonnes concernées : `an_nais` (usagers)
- Description : années manquantes et usagers de plus de 100 ans, avec un minimum à 1900.
- Ampleur : 11 118 manquantes, 221 âges supérieurs à 100 ans.
- Cause probable : saisie incomplète ou valeur par défaut.
- Traitement retenu : un âge supérieur à 100 ans devient une valeur manquante.
- Impact sur l'analyse : Q4, analyse par âge.

## ANO-10. Identifiant d'usager absent en 2019 et 2020

- Colonnes concernées : `id_usager` (usagers)
- Description : la colonne n'existe qu'à partir de 2021.
- Ampleur : 238 272 usagers, environ 32 % des lignes.
- Cause probable : ajout de colonne par le producteur.
- Traitement retenu : non utilisée ; l'usager est identifié par sa ligne.
- Impact sur l'analyse : aucun, la colonne n'est pas utilisée.

## ANO-11. Formats divers dans les fichiers lieux

- Colonnes concernées : `v2`, `pr`, `pr1` (lieux)
- Description : `N/A`, `(1)` et fins de ligne Windows dans les fichiers 2020.
- Ampleur : à mesurer.
- Cause probable : exports hétérogènes selon les années.
- Traitement retenu : colonnes non utilisées pour l'instant.
- Impact sur l'analyse : aucun sur les questions retenues.

## ANO-12. Année 2020 atypique

- Colonnes concernées : toutes
- Description : 47 744 accidents contre 58 840 en 2019, soit environ 19 % de moins.
- Ampleur : toute l'année 2020.
- Cause probable : confinements et baisse du trafic.
- Traitement retenu : conservée, signalée sur chaque graphique d'évolution.
- Impact sur l'analyse : toutes les évolutions sur 2019-2024.
