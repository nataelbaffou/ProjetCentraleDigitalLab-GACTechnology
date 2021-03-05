# ProjetCentraleDigitalLab-GACTechnology

Vous trouverez dans ce repo :
- l'ensemble des sripts utilisés pour traiter les jeux de données 
- Les différents notebooks concernant les 3 solutions misent en place à savoir :
  - la prédiction de consommation
  - la désagrégation de consommation
  - la détection d'anomalies


### Infos supplémentaires

#### Prédiction 
Le traitement des données pour la prédiction amènent à un format précis :
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

Le traitement des données pour la détection d'anomalies est le même que pour la prédiction.
Il faut veiller à ce que les données de consommation des bâtiments soient dans le même répertoire que le fichier metadata.csv.
Le traitement des données est différent selon qu'on utilise un ou plusieurs bâtiments en données d'entrée. Les trois fonctions scaling, create_sequences et get_train_test_sets
qui permettent d'obtenir les jeux de données d'entraînement et de test dépendent de cela.


#### Désagrégation
Pour la désagrégation on utilise la bibliothèque `nilmtk` (https://github.com/nilmtk/nilmtk) ainsi que la bibliothèque neuralnilm (https://github.com/JackKelly/neuralnilm). 

##### Installation de nilmtk
Suivre les instructions d'installation décrites ici : https://github.com/nilmtk/nilmtk/blob/master/docs/manual/user_guide/install_user.md

Pour éviter des erreurs, mettre à jour pandas ```pip install pandas=1.2.2 --user```

##### Installation de neuralnilm

```
git clone https://github.com/JackKelly/neuralnilm.git
```
La bibliothèque semble avoir des syntaxes de python2 qui font que ça ne marche pas sur python3.
On vautiliser 2to3 pour régler le problème :
```
pip install 2to3
```
```
2to3 --output-dir=python3-version/neuralnilm -W -n neuralnilm
```
```
cd python3-version/neuralnilm
```
```
python setup.py install
```

Installer également keras et theano  : 
```
conda install keras
conda install theano

```

