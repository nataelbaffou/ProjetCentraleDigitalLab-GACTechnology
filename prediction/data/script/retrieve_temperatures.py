import requests

def download_temperatures(url, save_directory):
    response = requests.get(url, allow_redirects=True)
    name = url[len(url) - url[::-1].find('/'):-3].replace('synop.','temperature_')
    with open(save_directory + name, "wb") as f:
        f.write(response.content)
    return name

## Main
# on veut 2006 à 2007 et 2015 à 2017
annee = 2006
i=0
mois = 1

while annee <=2017 :
    if annee < 2008 or annee > 2014:
        string = "{}{:0>2d}".format(annee,mois)
        url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.{}.csv.gz".format(string)
        save_directory = "C:/Users/CDL/Desktop/temperatures/"
        name = download_temperatures(url,save_directory)
        print("file {} created".format(name))

    i+=1
    if i%12 == 0:
        annee += 1
    mois = i%12+1
