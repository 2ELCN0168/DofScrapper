<p align="center">
  <img src="https://static.ankama.com/dofus/ng/modules/mmorpg/discover/illu-block3.png" />
</p>

# DofScrapper

**DofScrapper** est un projet Python dont l'objectif est de récupérer les liens des pages de l'encyclopédie et d'en extraire les images de tous les éléments. Les téléchargements sont faits selon l'arborescence de l'Encyclopédie et triés de manière pertinente grâce aux filtres.

> [!warning]
> Projet bancal, toute aide est la bienvenue

**Disclaimer :**

Je n'ai pas à l'heure actuelle de connaissances très poussées en Python. 95% de ce code m'a été fourni grâce à ChatGPT car je voulais uniquement quelque chose de fonctionnel et rapide. Le code est certainement sale et mal organisé, mais il fonctionne plutôt bien.
**Je compte refaire le projet de zéro d'ici quelques mois, lorsque j'aurai appris à faire du scrapping efficacement. En attendant, il faut se contenter de cette version.

## Fonctionnement 

**DofScrapper** propose un menu, il fonctionne par étapes : 
1. Scanner les pages de l'encyclopédie pour récupérer tous les liens selon les catégories et les filtres ;
2. Téléchargement des images grâce au remplissage au préalable d'un fichier JSON grâce aux scans ;
3. *(Optionnel)* Création de l'arborescence uniquement, uniquement les répertoires.

Le scan ainsi que le téléchargement effectuent des requêtes en parallèle, ce qui a pour conséquence de se faire bloquer par le serveur *(erreur 403)*. Ce blocage dure environ 5 minutes. Il est possible de tout télécharger comme il faut mais c'est le seul point de friction de DofScrapper hormis les défauts de conception précédemment décrits.

## Installation 

1. Cloner ce dépôt ;
2. Créer un environnement virtuel *(non fourni)* avec `python -m venv env` en étant dans le répertoire de **DofScrapper** ;
3. Activer le script dans `env/bin/activate` *(Sous Linux, il faut utliser `source env/bin/activate`, pour Windows, ouvrir Powershell et exécuter `./env/bin/Activate.ps1`)* ;
4. Télécharger les dépendances une fois dans l'environnement virtuel avec `pip -r install requirements.txt` ;
5. Exécuter `python DofScrapper.py`.

Le fichier JSON, résultant d'un scan de ma part est fourni. Il peut ne plus être à jour en fonction des changements dans l'encyclopédie.
