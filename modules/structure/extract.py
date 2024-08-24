import os

import requests
from bs4 import BeautifulSoup

from modules.headers import get_headers  # Import du User-Agent centralisé

from .bestiaire import extract_zones
from .montures import extract_families
from .utils import create_directory

base_url = "https://www.dofus.com/fr/mmorpg/encyclopedie"
output_dir = "encyclopedie"


def extract_and_create_dirs():
    session = requests.Session()
    headers = get_headers()  # Appel de la fonction pour obtenir les headers
    response = session.get(base_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main_sections = soup.find_all("a", class_="ak-item")

    for section in main_sections:
        section_name = section.find("div", class_="ak-title").text.strip()
        section_link = "https://www.dofus.com" + section["href"]
        directory_name = section_name.lower().replace(" ", "_").replace("'", "")
        directory_path = os.path.join(output_dir, directory_name)
        create_directory(directory_path)
        print(f"Dossier créé : {directory_path}")

        if section_name.lower() == "bestiaire":
            extract_zones(section_link, directory_path)
        elif section_name.lower() == "montures":
            extract_families(section_link, directory_path)
        else:
            extract_types(section_link, directory_path)


def extract_types(section_url, parent_directory):
    session = requests.Session()
    headers = get_headers()  # Appel de la fonction pour obtenir le dictionnaire
    response = session.get(section_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    filters_section = soup.find("div", {"data-name": "item_type_id"})
    if not filters_section:
        return

    item_types = filters_section.find_all("label", class_="ak-label")
    for item_type in item_types:
        item_name = item_type.text.strip()
        directory_name = item_name.lower().replace(" ", "_").replace("'", "")
        directory_path = os.path.join(parent_directory, directory_name)
        create_directory(directory_path)
        print(f"Sous-dossier créé : {directory_path}")
