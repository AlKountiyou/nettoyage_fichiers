import os
import time
import argparse
import logging
import sys

# Configuration du logger
logging.basicConfig(
    filename='nettoyage_fichiers.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def verifier_acces_superutilisateur():
    """Vérifie si le script est exécuté avec les droits de superutilisateur."""
    if os.geteuid() != 0:
        print("Ce script doit être exécuté avec les privilèges de superutilisateur.")
        logging.critical("Tentative d'exécution sans privilèges de superutilisateur.")
        sys.exit(1)


def obtenir_taille_fichier(fichier):
    """Retourne la taille du fichier en Mo."""
    try:
        return os.path.getsize(fichier) / (1024 * 1024)
    except Exception as e:
        logging.error(f"Erreur lors de la recuperation de la taille du fichier {fichier}: {e}")
        return 0

def nettoyer_fichiers_temp(repertoire, duree_max_jours, taille_min_mo):
    """Supprime les fichiers temporaires en demandant confirmation a l'utilisateur."""
    maintenant = time.time()
    duree_max_secondes = duree_max_jours * 24 * 60 * 60
    fichiers_supprimes = False

    logging.info(f"Debut du nettoyage dans le repertoire : {repertoire}")
    try:
        for dossier_racine, dossiers, fichiers in os.walk(repertoire):
            for fichier in fichiers:
                chemin_fichier = os.path.join(dossier_racine, fichier)
                try:
                    age_fichier = maintenant - os.path.getmtime(chemin_fichier)
                    taille_fichier = obtenir_taille_fichier(chemin_fichier)
                    if age_fichier > duree_max_secondes and taille_fichier >= taille_min_mo:
                        taille_fichier = obtenir_taille_fichier(chemin_fichier)
                        age_jours = age_fichier / (24 * 60 * 60)

                        print(f"Fichier trouve : {chemin_fichier}")
                        print(f"Taille : {taille_fichier:.2f} Mo | Âge : {age_jours:.1f} jours")
                        confirmation = ""
                        while confirmation not in ['oui', 'non']:
                            confirmation = input("Voulez-vous supprimer ce fichier ? (oui/non) : ").lower()

                        if confirmation == 'oui':
                            os.remove(chemin_fichier)
                            fichiers_supprimes = True
                            logging.info(f"Fichier supprime : {chemin_fichier}")
                            print(f"Fichier supprime : {chemin_fichier}\n")
                        else:
                            logging.info(f"Fichier conserve : {chemin_fichier}")
                            print(f"Fichier conserve : {chemin_fichier}\n")
                except Exception as e:
                    logging.error(f"Erreur lors du traitement du fichier {chemin_fichier}: {e}")
    except Exception as e:
        logging.critical(f"Erreur critique lors du parcours du repertoire {repertoire}: {e}")
    finally:
        if not fichiers_supprimes:
            print(f"Aucun fichier à supprimer ne correspond aux critères (plus ancien que {duree_max_jours} jours et supérieur à {taille_min_mo} Mo) ou validé par l'utilisateur.")
            logging.info(f"Aucun fichier supprimé : aucun fichier ne correspond aux critères ou n'a été validé par l'utilisateur.")
        logging.info(f"Nettoyage termine pour le repertoire : {repertoire}")

def main():
    #verifier_acces_superutilisateur()
    
    parser = argparse.ArgumentParser(description='Nettoyage des fichiers temporaires.')
    parser.add_argument('repertoire', type=str, help="Le repertoire a nettoyer")
    parser.add_argument('--jours', type=int, default=30, help="Nombre de jours apres lesquels les fichiers sont consideres comme obsoletes (par defaut 30 jours)")
    parser.add_argument('--taille_min', type=float, default=500, help="Taille minimale des fichiers à supprimer (en Mo, par défaut 500 Mo)")

    args = parser.parse_args()

    if not os.path.exists(args.repertoire):
        logging.error(f"Le repertoire specifie n'existe pas : {args.repertoire}")
        print(f"Erreur : Le repertoire specifie n'existe pas : {args.repertoire}")
        return

    nettoyer_fichiers_temp(args.repertoire, args.jours, args.taille_max)

if __name__ == "__main__":
    main()