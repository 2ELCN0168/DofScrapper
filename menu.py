import asyncio
import json
import os
import platform

import aiohttp

from modules.headers import get_headers
from modules.images.download_images import download_images_for_category
from modules.images.scan_pages import (scan_category_with_pagination,
                                       scan_category_without_filters)
from modules.structure import bestiaire, extract, montures

CATEGORIES = {
    "1": (
        "Armes",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/armes",
        extract.extract_types,
    ),
    "2": (
        "Bestiaire",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/monstres",
        bestiaire.extract_zones,
    ),
    "3": (
        "Montures",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/montures",
        montures.extract_families,
    ),
    "4": (
        "Équipements",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/equipements",
        extract.extract_types,
    ),
    "5": (
        "Ressources",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/ressources",
        extract.extract_types,
    ),
    "6": (
        "Familiers",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/familiers",
        extract.extract_types,
    ),
    "7": (
        "Consommables",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/consommables",
        extract.extract_types,
    ),
    "8": (
        "Objets d'apparat",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/objets-d-apparat",
        extract.extract_types,
    ),
    "9": (
        "Harnachements",
        "https://www.dofus.com/fr/mmorpg/encyclopedie/harnachements",
        extract.extract_types,
    ),
}

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def afficher_menu_parent():
    while True:
        clear_console()  # Nettoie la console avant d'afficher le menu
        print("=== Menu Principal ===")
        print("1. Créer la structure de l'encyclopédie")
        print("2. Scanner les pages")
        print("3. Télécharger les liens du fichier JSON")
        print("4. Quitter")

        choix = input("Choisissez une option : ")

        if choix == "1":
            afficher_menu_structure()
        elif choix == "2":
            asyncio.run(menu_scan())  # Exécutez la fonction asynchrone
        elif choix == "3":
            asyncio.run(menu_download())
        elif choix == "4":
            print("Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

def afficher_menu_structure():
    while True:
        clear_console()  # Nettoie la console avant d'afficher le menu
        print("=== Menu Structure ===")
        print("1. Créer l'arborescence pour une catégorie spécifique")
        print("2. Créer toute l'arborescence")
        print("3. Retour au menu principal")

        choix = input("Choisissez une option : ")

        if choix == "1":
            choisir_categorie()
        elif choix == "2":
            extract.extract_and_create_dirs()
            input("Appuyez sur Entrée pour revenir au menu.")
        elif choix == "3":
            break
        else:
            print("Choix invalide, veuillez réessayer.")

def choisir_categorie():
    while True:
        clear_console()  # Nettoie la console avant d'afficher le menu
        print("=== Choisir une Catégorie ===")
        for key, (name, _, _) in CATEGORIES.items():
            print(f"{key}. {name}")
        print("10. Retour au menu structure")

        choix = input("Choisissez une catégorie : ")

        if choix in CATEGORIES:
            name, url, func = CATEGORIES[choix]
            func(url, f"encyclopedie/{name.lower().replace(' ', '_').replace('\'', '')}")
            input("Appuyez sur Entrée pour revenir au menu.")
        elif choix == "10":
            return
        else:
            print("Choix invalide, veuillez réessayer.")

async def menu_scan():
    while True:
        clear_console()
        print("=== Menu de Scan ===")
        print("1. Scanner les pages pour les Armes")
        print("2. Scanner les pages pour les Équipements")
        print("3. Scanner les pages pour le Bestiaire")
        print("4. Scanner les pages des Familiers")
        print("5. Scanner les pages des Montures")
        print("6. Scanner les pages des Consommables")
        print("7. Scanner les pages des Ressources")
        print("8. Scanner les pages des Objets d'apparat")
        print("9. Scanner les pages des Compagnons")
        print("10. Scanner les pages des Havres-sacs")
        print("11. Scanner les pages des Harnachements")
        print("12. Revenir au menu précédent")

        choix = input("Choisissez une option : ")

        json_file = "encyclopedie.json"
        
        async with aiohttp.ClientSession(headers=get_headers()) as session:
            if choix == "1":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/armes", "armes", json_file)
                input("Scan des Armes terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "2":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/equipements", "equipements", json_file)
                input("Scan des Équipements terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "3":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/monstres", "bestiaire", json_file)
                input("Scan du Bestiaire terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "4":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/familiers", "familiers", json_file)
                input("Scan des Familiers terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "5":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/montures", "montures", json_file)
                input("Scan des Montures terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "6":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/consommables", "consommables", json_file)
                input("Scan des Consommables terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "7":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/ressources", "ressources", json_file)
                input("Scan des Ressources terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "8":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/objets-d-apparat", "objets-d-apparat", json_file)
                input("Scan des Objets d'apparat terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "9":
                await scan_category_without_filters(session, "https://www.dofus.com/fr/mmorpg/encyclopedie/compagnons", "compagnons", json_file)
                input("Scan des Compagnons terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "10":
                await scan_category_without_filters(session, "https://www.dofus.com/fr/mmorpg/encyclopedie/havres-sacs", "havres-sacs", json_file)
                input("Scan des Havres-sacs terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "11":
                await scan_category_with_pagination("https://www.dofus.com/fr/mmorpg/encyclopedie/harnachements", "harnachements", json_file)
                input("Scan des Harnachements terminé. Appuyez sur Entrée pour revenir au menu.")
            elif choix == "12":
                return
            else:
                print("Choix invalide, veuillez réessayer.")


async def menu_download():
    while True:
        clear_console()
        print("=== Menu de Téléchargement ===")
        print("1. Télécharger les pages pour les Armes")
        print("2. Télécharger les pages pour les Équipements")
        print("3. Télécharger les pages pour le Bestiaire")
        print("4. Télécharger les pages pour les Familiers")
        print("5. Télécharger les pages pour les Montures")
        print("6. Télécharger les pages pour les Consommables")
        print("7. Télécharger les pages pour les Ressources")
        print("8. Télécharger les pages pour les Objets d'apparat")
        print("9. Télécharger les pages pour les Compagnons")
        print("10. Télécharger les pages pour les Havres-sacs")
        print("11. Télécharger les pages pour les Harnachements")
        print("12. Revenir au menu précédent")

        choix = input("Choisissez une option : ")

        json_file = "encyclopedie.json"
        
        async with aiohttp.ClientSession(headers=get_headers()) as session:
            if choix == "1":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "armes" in data:
                    await download_images_for_category(session, "armes", data["armes"])
                    input("Téléchargement des images pour les Armes terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Armes")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "2":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "equipements" in data:
                    await download_images_for_category(session, "equipements", data["equipements"])
                    input("Téléchargement des images pour les Équipements terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Équipements")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "3":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "bestiaire" in data:
                    await download_images_for_category(session, "bestiaire", data["bestiaire"])
                    input("Téléchargement des images pour le Bestiaire terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour le Bestiaire")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "4":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "familiers" in data:
                    await download_images_for_category(session, "familiers", data["familiers"])
                    input("Téléchargement des images pour les Familiers terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Familiers")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "5":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "montures" in data:
                    await download_images_for_category(session, "montures", data["montures"])
                    input("Téléchargement des images pour les Montures terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Montures")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "6":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "consommables" in data:
                    await download_images_for_category(session, "consommables", data["consommables"])
                    input("Téléchargement des images pour les Consommables terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Consommables")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "7":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "ressources" in data:
                    await download_images_for_category(session, "ressources", data["ressources"])
                    input("Téléchargement des images pour les Ressources terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Ressources")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "8":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "objets_d_apparat" in data:
                    await download_images_for_category(session, "objets_d_apparat", data["objets_d_apparat"])
                    input("Téléchargement des images pour les Objets d'apparat terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Objets d'apparat")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "9":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "compagnons" in data:
                    await download_images_for_category(session, "compagnons", data["compagnons"])
                    input("Téléchargement des images pour les Compagnons terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Compagnons")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "10":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "havres_sacs" in data:
                    await download_images_for_category(session, "havres_sacs", data["havres_sacs"])
                    input("Téléchargement des images pour les Havres-sacs terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Havres-sacs")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "11":
                with open(json_file, "r") as f:
                    data = json.load(f)
                if "harnachements" in data:
                    await download_images_for_category(session, "harnachements", data["harnachements"])
                    input("Téléchargement des images pour les Harnachements terminé. Appuyez sur Entrée pour revenir au menu.")
                else:
                    print("Aucune donnée trouvée pour les Harnachements")
                    input("Appuyez sur Entrée pour revenir au menu.")
            elif choix == "12":
                return
            else:
                print("Choix invalide, veuillez réessayer.")
if __name__ == "__main__":
    afficher_menu_parent()

