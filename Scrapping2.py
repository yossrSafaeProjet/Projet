import time
import requests
import Processor
from bs4 import BeautifulSoup
class Scrapping2:
    def __init__(self):
        pass

    def recupererDuration(self,chaîne_cible,serie_info):
        list_duration=[]
        for serie in serie_info:
            chaine_diffusion=serie.get("Chaîne de diffusion")
            if chaîne_cible==chaine_diffusion:
                nom_serie = serie.get('Nom de la série')
                num_episode = serie.get('Numéro de episode')
                url_episode=serie.get('URL de la page de l\'épisode')
                rep_episode = requests.get(f"https://www.spin-off.fr/{url_episode}")
                soup = BeautifulSoup(rep_episode.content, 'html.parser')
                time.sleep(3)  # Attendez 5 secondes

            # Récupérez la durée de l'épisode depuis la page de l'épisode
                duree_episode = soup.find("div", class_="episode_infos_episode_format").text
                #print (duree_episode)
                dic_duration = {
                    'Nom de la série': nom_serie,
                    'Numéro de episode': num_episode,
                    'La durée de l\'épisode': duree_episode
                }
                list_duration.append(dic_duration)
        
        return list_duration
    