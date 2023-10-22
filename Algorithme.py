import sqlite3
class Algorithme:
    def __init__(self):
        pass
    #Une méthode pour les deux  premiers questions algorigmes 
    def nbr_episode_par_categorie(self,table_name,column_name):
        conn = sqlite3.connect('data/databases/database.db')
        cursor = conn.cursor()

        # Extraction de toutes les données de la table
        cursor.execute(f'SELECT date_Diffusion, {column_name} FROM {table_name}')
        resultats = cursor.fetchall()
        conn.close()

        episodes_par_categorie = {}

        for row in resultats:
            date_diffusion = row[0]
            categorie = row[1]

            jour, mois, annee = map(int, date_diffusion.split('/'))

            if mois == 10:
                if categorie in episodes_par_categorie:
                    episodes_par_categorie[categorie] += 1
                else:
                    episodes_par_categorie[categorie] = 1

        print(f"\nNombre d'épisodes diffusés en octobre par {column_name}:")
        for categorie, nombre in episodes_par_categorie.items():
            print(f"{column_name} : {categorie}, Nombre d'épisodes en octobre : {nombre}")

    """ nbr_episode_par_categorie("episode","pays_Origine")
    nbr_episode_par_categorie("episode","chaine_Diffusion") """

    def extraire_noms_series(self):
        conn = sqlite3.connect('data/databases/database.db')
        cur = conn.cursor()
        cur.execute("SELECT nom_Serie FROM episode")
        resultats = cur.fetchall()
        conn.close()
        return [resultat[0] for resultat in resultats]

    def mots_plus_presents(self,noms_series):
        mots_count = {}

        for nom_serie in noms_series:
            mots = nom_serie.split()
            #print(mots)
            for mot in mots:
                mot = mot.lower()
                if mot in mots_count:
                    mots_count[mot] += 1
                else:
                    mots_count[mot] = 1

        mots_count = dict(sorted(mots_count.items(), key=lambda item: item[1], reverse=True))
        return list(mots_count.items())[:10]
    def recupereChaineDeDiffusion(self,list_episodes):
        list_episodes.sort(key=lambda x: x['Date de diffusion'])
        chaîne_actuelle = ''
        diffusion_max = 0
        jours_consécutifs = 0

    # Parcourez les épisodes triés
        for épisode in list_episodes:
            if épisode['Chaîne de diffusion'] == chaîne_actuelle:
                jours_consécutifs += 1
            else:
                jours_consécutifs = 1
                chaîne_actuelle = épisode['Chaîne de diffusion']

        if jours_consécutifs > diffusion_max:
            diffusion_max = jours_consécutifs

# Affichez la chaîne avec la diffusion la plus longu
        print(f"La chaîne avec la diffusion la plus longue en octobre est {chaîne_actuelle} avec {diffusion_max} jours consécutifs.")

