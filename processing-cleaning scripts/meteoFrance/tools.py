import requests


def download_list_from_file(path_to_file, save_directory):
    print("Starting list :", path_to_file)
    print("Saving to :", save_directory)
    with open(path_to_file, "r") as f:
        urls = f.readlines()
        N = len(urls)
        for i, url in enumerate(urls):
            url = url.strip()
            print("file :", i, "/", N, "\t", url, "\r")
            download_from_url(url, save_directory)


def download_from_url(url, save_directory):
    response = requests.get(url, allow_redirects=True)
    name = url[len(url) - url[::-1].find('/'):] if url.find('/') else url
    open(save_directory + name, "wb").write(response.content)
