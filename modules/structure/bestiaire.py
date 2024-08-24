import os

import requests
from bs4 import BeautifulSoup

from modules.headers import get_headers  # Import du User-Agent centralisé

from .utils import create_directory


def extract_zones(section_url, parent_directory):
    session = requests.Session()
    headers = get_headers()  # Appel de la fonction pour obtenir les headers
    response = session.get(section_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    filters_section = soup.find("div", {"data-name": "item_monster_zones"})
    if not filters_section:
        print(f"Pas de zones trouvées pour {section_url}")
        return

    zones = filters_section.find_all("label", class_="ak-label")
    for zone in zones:
        zone_name = zone.text.strip()
        directory_name = zone_name.lower().replace(" ", "_").replace("'", "")
        directory_path = os.path.join(parent_directory, directory_name)
        create_directory(directory_path)
        print(f"Sous-dossier créé pour la zone : {directory_path}")
