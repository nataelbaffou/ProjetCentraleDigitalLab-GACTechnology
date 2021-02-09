import re
import os
import tools

source_directory = "src/"
source_file = "liste_stations_raw"
data_directory = "data/"
store_directory = data_directory + "normales_et_records/"
aggregation_directory = store_directory + "AGGREGATE/"

data_types = {'fiche_pdf':
                  {"links": source_directory + "links_fiche_climatologique_pdf",
                   "directory": store_directory + "FICHECLIM_PDF/",
                   "download": False},
              'fiche_data':
                  {"links": source_directory + "links_fiche_climatologique_data",
                   "directory": store_directory + "FICHECLIM_DATA/",
                   "download": True},
              'fiche_meta':
                  {"links": source_directory + "links_fiche_climatologique_metadonnees",
                   "directory": store_directory + "FICHECLIM_META/",
                   "download": False}
              }


def get_download_links_from_file():
    if not os.path.exists(source_directory + source_file):
        raise FileNotFoundError

    base_url = "https://donneespubliques.meteofrance.fr"

    links_fiche_pdf = []

    with open(source_directory + source_file, 'r') as f:
        list_of_links = f.read().split("href")
        for link in list_of_links:
            for match in re.findall("\"(/FichesClim/.*pdf)", link):
                links_fiche_pdf.append(match)
        f.close()

    links_fiche_pdf = [base_url + link for link in links_fiche_pdf]
    links_fiche_data = [link[:-3] + "data" for link in links_fiche_pdf]
    links_fiche_meta = [base_url + "/metadonnees_publiques/fiches/fiche_" + re.findall("_(\d+)\.pdf", link)[0] + ".pdf"
                        for link in links_fiche_pdf]

    with open(source_directory + "links_fiche_climatologique_pdf", "w") as f:
        f.write('\n'.join(links_fiche_pdf))
        f.close()

    with open(source_directory + "links_fiche_climatologique_data", "w") as f:
        f.write('\n'.join(links_fiche_data))
        f.close()

    with open(source_directory + "links_fiche_climatologique_metadonnees", "w") as f:
        f.write('\n'.join(links_fiche_meta))
        f.close()


def verify_directories():
    def verify(_path):
        if not os.path.exists(_path):
            print("path :", _path, "doesn't exist")
            os.mkdir(_path)
            print("path :", _path, "created")

    # global paths
    for path in [source_directory, data_directory, store_directory, aggregation_directory]:
        verify(path)

    # specific data paths
    for key in data_types:
        if "directory" in data_types[key].keys():
            verify(data_types[key]["directory"])


def download():
    verify_directories()
    for key in data_types:
        if "download" in data_types[key].keys() and data_types[key]["download"]:
            if "links" in data_types[key].keys() and "directory" in data_types[key].keys():
                tools.download_list_from_file(data_types[key]["links"], data_types[key]["directory"])


def transform_extension_from_data_to_csv():
    directory = store_directory + "FICHECLIM_DATA/"

    for file in os.listdir(directory):
        if file[-5:] == ".data":
            os.rename(directory+file, directory+file[:-4]+"csv")
        #open(directory + file[:-4] + "csv", "w").write(open(directory + file, 'r').read())


def aggregate():
    data_directory = store_directory + "FICHECLIM_DATA/"
    f_agg = open(aggregation_directory + 'normales_et_records.csv', "w")
    columns = "station;indicatif;alt (m);lat;lon;"
    months = ["Janv.", "Fevr.", "Mars", "Avril", "Mai", "Juin", "Juil.", "Aout", "Sept.", "Oct.", "Nov.", "Dec.",
              "Annuel"]
    vars = ["Tmax_", "Tmoy_", "Tmin_", "Pmoy_"]
    units = ["°C", "°C", "°C", "mm"]
    for var, unit in zip(vars, units):
        for month in months:
            columns += var + month + ' (' + unit + ')' + ';'
    f_agg.write(columns + "\n")

    def readline_values(line):
        if line.count(';') == 14:
            return [value.strip() for value in line.split(';') if value.strip() != ""]
        return []

    for file in os.listdir(data_directory):
        if file[-4:] == ".csv":
            f_cur = open(data_directory + file, 'r')
            i_lines_to_read = []
            for i, line in enumerate(f_cur.readlines()):
                if i == 3:
                    infos = line.strip('\n ;').split(', ')
                    values = [line.split(')')[0] + ')']
                    for info in infos:
                        if info.endswith('m'):
                            info = info[:-1]
                        values.append(info.split(' : ')[1])
                    f_agg.write(';'.join(values) + ';')
                if line in ["Précipitations : Hauteur moyenne mensuelle (mm);\n",
                            "Température maximale (Moyenne en °C);\n",
                            "Température moyenne (Moyenne en °C);\n",
                            "Température minimale (Moyenne en °C);\n"]:
                    i_lines_to_read.append(i + 1)
                    i_lines_to_read.append(i + 2)
                if i in i_lines_to_read:
                    L = readline_values(line)
                    if L:
                        f_agg.write(';'.join(L) + ';')
            f_agg.write('\n')
