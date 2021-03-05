import normales_et_records

"""
Partie normales et records (température et précipitations)
Fichiers téléchargés le 9/02/2021

Les fichiers sont aggrégés au sein du dossier data/normales_et_records/AGGREGATE
Pour plus d'informations sur les données récupérées voir : 
            https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=117&id_rubrique=39

Les fiches sont également téléchargeables au format PDF et des informations complémentaires 
sur les stations le sont également en modifiant les booléens dans le fichier normales_et_records.py
"""
normales_et_records.verify_directories()
#normales_et_records.get_download_links_from_file()
#normales_et_records.download()
#normales_et_records.transform_extension_from_data_to_csv()
normales_et_records.aggregate()
