# Avec la syntaxe from ... import ... on import un seul  objet
import Scrapping2
from Processor import Processor
from ReadAndWriteFile import ReadAndWriteFile
from DataBases import DataBases
from Algorithme import Algorithme
from Scrapping2 import Scrapping2

#from alerter import Alerter

# Avec la syntaxe import .... on import tout le package
import datetime

# Avec la syntaxe from ... import * on importe tout  🚨🚨 a ne pas utiliser
# risque de conflit avec un autre objet (fonction, class, variable)
# qui aurait le même nom
# ici pas de risque : seulement une fonction nommée time_exec
#from time_exec import *


def main():
    starting_time = datetime.datetime.now()
    url = "https://www.spin-off.fr/calendrier_des_series.html"
    #Récupérer les données relatives à la difuution d'episode 
    processor_instance = Processor(limit=40)
    serie_info = processor_instance.recuprer(url)
    for serie in serie_info:
        print(serie) 
    print(f"************************* FILES***********************")
    read_write_file_instance=ReadAndWriteFile()
    #Enregistrer les données récupérées dans un ficher csv
    read_file=read_write_file_instance.Enregistrer(serie_info)
    #Lire les données enregistrées dans un ficher csv
    write_file=read_write_file_instance.lire_fichier_csv("episodes.csv")
    for episode in write_file:
        print(episode)
    print(f"*************************SQL***********************")
    #SQL
    #Insérer les données de la question Scrapping dans avec sqlite dans la base de donnée
    data_Base_instance=DataBases()
    data_Base_instance.inserer_data_Sqlite(serie_info)

    #Insérer les données de la question Scrapping dans avec Scalingo 
    data_Base_instance.inserer_data_Squalingo(serie_info)
    print(f"*************************ALGORITHME***********************")
    #ALGORITHMES
    #Calculer le nombre d'épisodes diffusés par chaque chaine de télivision en Octobre
    algorithme_instance=Algorithme()
    algorithme_instance.nbr_episode_par_categorie("episode","chaine_Diffusion")
    #Calculer le nombre d'épisodes diffusés par chaque pays n en Octobre
    algorithme_instance.nbr_episode_par_categorie("episode","pays_Origine")
    #Indiquer les 10 mots les plus présents dans les nom des séries
    noms_series = algorithme_instance.extraire_noms_series()
    mots_plus_presents_10 = algorithme_instance.mots_plus_presents(noms_series)
    for mot in mots_plus_presents_10:
        print(f"Mot : {mot[0]}")

    print(f"*************************SCRAPPING2***********************")
    #Le deuxième scrapping 
    scrapping_instance=Scrapping2() 
    #Récupération de la durée de l'épisode à partir de l'url récupéré 
    duration_list=scrapping_instance.recupererDuration("tvN",serie_info)
    #Stocker les données de la durée dans une base de donnée sqlite 
    data_Base_instance.inserer_Sql_duration_sqlite(duration_list)
    #Stocker les données de la durée dans une base de donnée squalingo
    data_Base_instance.inserer_Sql_duration_scalingo(duration_list)
    print(f"*************************ALGORITHME2***********************")
    #ALGORITHME 2
    #Récupérer la chaine TV QUI DIFFUSE lES EPISODES pendant le plus grand nombre de jours consécutifs sur le mois d'OCTOBRE 
    algorithme_instance.recupereChaineDeDiffusion(serie_info) 


if __name__ == "__main__":
    main()
