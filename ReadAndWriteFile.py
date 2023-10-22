import os
import csv
from datetime import datetime
import Processor
class ReadAndWriteFile:
    def __init__(self):
        pass
        #Enregistrer les données dans fichierscsv
    def Enregistrer(self,list):

        with open('data/files/episodes.csv', 'w+',newline="") as file:
            writer=csv.writer(file)
            colonnes = list[0].keys()
            writer.writerow(colonnes)
            for ligne in list:
                writer.writerow(ligne.values())

        print(f"Les données ont été enregistrées dans episodes.csv")



    #Lire les fichiers à partie du ficher crée
    def lire_fichier_csv(self,chemin_fichier):
        chemin_absolu = os.path.abspath(f"data\\files\\{chemin_fichier}")
        #print(chemin_absolu)
        liste_episodes = []  # Initialiser la liste pour stocker les données
        
        # Ouvrir le fichier en mode lecture
        with open(chemin_absolu, 'r+') as fichier:
            lignes = fichier.readlines()  # Lire toutes les lignes du fichier
            #print(lignes)
            # Parcourir chaque ligne
            for ligne in lignes:
                # Diviser la ligne en utilisant la virgule comme séparateur
                elements = ligne.strip().split(',')
                
                # Convertir les éléments en types appropriés (par exemple, str, int, etc.)
                nom_serie = elements[0]
                pays_origine = elements[1]
                try:
                    numero_saison = int(elements[2])
                    numero_episode = int(elements[3])
                except ValueError:
                    numero_saison =None
                    numero_episode=None
                try:
                    date_diffusion = datetime.strptime(elements[4], "%d/%m/%Y").date()
                    
                except ValueError:
                    date_diffusion = None
                
                chaine_diffusion = elements[5]
                url_episode = elements[6]
                
                # Créer un tuple avec les données converties
                episode = (nom_serie, pays_origine, numero_saison, numero_episode, date_diffusion, chaine_diffusion, url_episode)
                
                # Ajouter le tuple à la liste
                liste_episodes.append(episode)
        
        return liste_episodes


