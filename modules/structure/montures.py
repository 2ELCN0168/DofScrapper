import os

import requests
from bs4 import BeautifulSoup

from modules.headers import get_headers  # Import du User-Agent centralisé

from .utils import create_directory


def extract_families(section_url, parent_directory):
    session = requests.Session()
    headers = get_headers()  # Appel de la fonction pour obtenir les headers
    response = session.get(section_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    filters_section = soup.find("div", {"data-name": "item_model_family_id"})
    if not filters_section:
        print(f"Pas de familles trouvées pour {section_url}")
        return

    families = filters_section.find_all("label", class_="ak-label")
    for family in families:
        family_name = family.text.strip()
        directory_name = family_name.lower().replace(" ", "_").replace("'", "")
        directory_path = os.path.join(parent_directory, directory_name)
        create_directory(directory_path)
        print(f"Sous-dossier créé pour la famille : {directory_path}")
