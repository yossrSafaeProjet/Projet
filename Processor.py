import requests
from bs4 import BeautifulSoup
#On a mit une variable limit parce que le sit eil contient plusieurs données du coup pour accéler l'execution parfois 
class Processor:
    def __init__(self,limit):
        self.limit=limit
    def recuprer(self,url):
        response = requests.get(url)
        count = 0
        series_list = []  # Liste pour stocker les informations de toutes les séries
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elements_calendrier = soup.find_all("span", class_="calendrier_episodes") 
            for element in elements_calendrier:
                serie_info = {}  # Dictionnaire pour stocker les informations de la série actuelle
                nom_serie = element.find_previous_sibling("span")
                
                if nom_serie:
                    pays_origine = None
                    img_tag = nom_serie.find_all_previous("img")[1]
                    
                    if img_tag:
                        pays_origine = img_tag.get("alt")
                        
                    lien_serie = nom_serie.find("a")
                    
                    if lien_serie:
                        try:
                            nom_serie_text = lien_serie.text
                            num_saison_episode = nom_serie.find("a", class_="liens").text
                            num_saison, num_episode = num_saison_episode.split(".")
                            
                            url = nom_serie.find_next("a", class_="liens")["href"]
                            rep = requests.get(f"https://www.spin-off.fr/{url}")
                            soup = BeautifulSoup(rep.content, 'html.parser')
                            
                            info_date_chaine = soup.find("div", class_="episode_infos_episode_chaine")
                            date_diffusion = info_date_chaine.text.split(" ")[2].split("\n")[0]
                            element_info = soup.find_all("span", class_="gras upper")[1].find("a", class_="nodecoration")
                            chaine_diffusion = element_info.text
                            
                            serie_info['Nom de la série'] = nom_serie_text
                            serie_info['Pays d\'origine'] = pays_origine
                            serie_info['Numéro de saison'] = num_saison
                            serie_info['Numéro de episode'] = num_episode
                            serie_info['Date de diffusion'] = date_diffusion
                            serie_info['Chaîne de diffusion'] = chaine_diffusion
                            serie_info['URL de la page de l\'épisode'] = url
                            series_list.append(serie_info)
                            count += 1
                            if count >= self.limit:
                                break 
                        except (TypeError, AttributeError):
                            pass 
        
        return series_list  