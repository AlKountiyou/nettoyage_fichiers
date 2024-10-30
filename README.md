# Nettoyage de Fichiers

Ce projet contient un script Python pour le nettoyage de fichiers.

## Structure du Projet

- `nettoyage_fichiers.py` : Script principal pour le nettoyage de fichiers.
- `README.md` : Ce fichier, fournissant des informations sur le projet.

## Pré-Requis
- python 3.x

## Utilisation

Pour exécuter le script, utilisez la commande suivante :

```sh
python nettoyage_fichiers.py ../Downloads --jours 60 --taille_max 200

- `../Downloads`: répertoire à nettoyer
- `--jours 60`: supprimer les fichiers plus anciens que 60 jours
- `--taille_max 200`: supprimer les fichiers plus gros que 200 Mo
