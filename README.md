# ProjetCentraleDigitalLab-GACTechnology

Vous trouverez dans ce repo :
- l'ensemble des sripts utilisés pour traiter les jeux de données 
- Les différents notebooks concernant les 3 solutions misent en place à savoir :
  - la prédiction de consommation
  - la désagrégation de consommation
  - la détection d'anomalies


### Infos supplémentaires

#### Prédiction et désagrégation
Le traitement des données pour la prédiction et la désagrégation amènent à un format précis :
- Chaque bâtiment est désigné par un id
- Chaque jeu de donnée à une plage d'id séparés par des milliers (ex : jeu1 0-999 | jeu2 1000-1999) décrites dans le fichier descriptif des jeux de données utilisés
- Un fichier est créé par bâtiment avec les contraintes suivantes :
  - Son nom est au format '{id}.csv'
  - Il comporte 3 colonnes : 'timestamp', 'active_power' et 'temperature'
  - Le séparateur est ';'
- Un fichier 'metadata.csv' regroupe tous les bâtiments traités et les relis à des informations supplémentaires. Il suit les règles suivantes :
  - Son index est la colonne 'bat_id' qui contient les ids des bâtiments qui son définit
  - Les colonnes qui sont alors :
    - is_house : booleen décrivant si les bâtiment est une maison (True) ou autre chose (False) ce qui correspond ici à un bâtiment commercial ou bureaux
    - time_step : float en minutes décrivant le pas de temps entre deux mesures dans le fichier de consommation. Il prend quasiment exclusiment les valeurs 15.0, 60. et 1440.0
    - lat : float concernant la latitude du bâtiment si connue
    - long : float concernant la longitude du bâtiment si connue
    - surface : float désignant la surface du bâtiment
    - {day}_is_off : booleen décrivant l'ouverture/travail sur le lieu pour le jour {day} pour les bâtiments commerciaux et bureaux
  - Si l'information est manquante les valeurs peuvent-être omisent


#### Anomalies
