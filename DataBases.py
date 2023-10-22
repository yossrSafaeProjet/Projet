import sqlite3
import psycopg2
import Processor
import Scrapping2
class DataBases:
    def __init__(self):
        pass
#Enregistrer les donneés dans un base de donnée sqlite
    def inserer_data_Sqlite(self,list_Series):
        # Connexion à la base de données (si elle n'existe pas, elle sera créée)
        conn=sqlite3.connect('data/databases/database.db')
        
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS episode (
            id SERIAL PRIMARY KEY,
            nom_Serie TEXT,
            pays_Origine TEXT,
            numeroSaison INTEGER,
            numero_Episode INTEGER,
            date_Diffusion TEXT,
            chaine_Diffusion TEXT,
            url_page_Episode TEXT
        )
        ''')
        # Validation des modifications
        conn.commit() 
        #Insertion
        for serie in list_Series:

            values = (
            serie['Nom de la série'],
            serie['Pays d\'origine'],
            serie['Numéro de saison'],
            serie['Numéro de episode'],
            serie['Date de diffusion'],
            serie['Chaîne de diffusion'],
            serie['URL de la page de l\'épisode']
        )
            cur.execute("INSERT INTO episode (nom_Serie, pays_Origine, numeroSaison, numero_Episode, date_Diffusion, chaine_Diffusion, url_page_Episode) VALUES (?, ?, ?, ?, ?, ?, ?)", values)
            """cur.execute("INSERT INTO episode (nom_Serie, pays_Origine,numero_Saison,numero_Episode,date_Diffusion,chaine_Diffusion,url_page_Episode) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        serie['Nom de la série'],
                        serie['Pays d'origine'],
                        serie['Numéro de saison'],
                        serie['Numéro de episode'],
                        serie['Date de diffusion'],
                        serie['Chaîne de diffusion'], 
                        serie['URL de la page de l épisode'])"""
        # Validation des modifications
        conn.commit()
        conn.close()

    #Enregistrer les donneés dans un base de donnée distante
    def inserer_data_Squalingo(self,list_Series):
        URL_DB = "postgres://python_4680:IsWS_MRHjHOwShJlJ8yv@python-4680.postgresql.a.osc-fr1.scalingo-dbs.com:33825/python_4680?sslmode=prefer"
        
        try:
            conn = psycopg2.connect(URL_DB)
            print("Connexion réussie")
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS episode (
                    id SERIAL PRIMARY KEY,
                    nom_Serie TEXT,
                    pays_Origine TEXT,
                    numero_Saison INTEGER,
                    numero_Episode INTEGER,
                    date_Diffusion TEXT,
                    chaine_Diffusion TEXT,
                    url_page_Episode TEXT
                )
            ''')
            conn.commit()
            
            for serie in list_Series:
                cur.execute("INSERT INTO episode (nom_Serie, pays_Origine, numero_Saison, numero_Episode, date_Diffusion, chaine_Diffusion, url_page_Episode) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (serie['Nom de la série'],
                            serie['Pays d\'origine'],
                            serie['Numéro de saison'],
                            serie['Numéro de episode'],
                            serie['Date de diffusion'],
                            serie['Chaîne de diffusion'], 
                            serie['URL de la page de l\'épisode']))
            
            # Validation des modifications
            conn.commit()
            cur.execute("Select * from episode")
            tables = cur.fetchall()
            for table in tables:
                print(table)
        except psycopg2.Error as e:
            print(e)
        finally:
            if conn:
                cur.close()
                conn.close()
                print("Connexion fermée")

    #serie_info = Processor.recuprer(50)
    #saveInDistantDataBase(serie_info)
    #inserer_Sql(serie_info)


    #Enregistrer les données de durée épisode dans une table duration localement avec sqlite 
    def inserer_Sql_duration_sqlite(self,list_duration):
        # Connexion à la base de données (si elle n'existe pas, elle sera créée)
        conn=sqlite3.connect('data/databases/database.db')
        # Création d'un curseur pour exécuter des commandes SQL
        cur = conn.cursor()

        # Définition du schéma de la table

        cur.execute('''
        CREATE TABLE IF NOT EXISTS duration (
            id SERIAL PRIMARY KEY,
            nom_Serie TEXT,
            duration Integer,
            numero_Episode INTEGER,
            id_episode INTEGER,
            FOREIGN KEY (id_episode) REFERENCES episode(id)
        )
        ''')
        for data in list_duration:
            nom_serie = data['Nom de la série']
            duration_text = data['La durée de l\'épisode']
            duration = int(''.join(filter(str.isdigit, duration_text)))

            numero_episode = data['Numéro de episode']
            
            cur.execute("SELECT id FROM episode WHERE nom_Serie = ? and numero_Episode = ?", (nom_serie, numero_episode))
            id_episode=cur.fetchone()[0]
            cur.execute("INSERT INTO duration (nom_Serie, duration, numero_Episode,id_episode) VALUES (?, ?, ?, ?)", (nom_serie, duration, numero_episode,id_episode))

        cur.execute("SELECT DISTINCT d.numero_Episode,d.nom_Serie,d.duration FROM duration d INNER JOIN episode e on d.id_episode=e.id where d.nom_serie=e.nom_Serie")
        liste=cur.fetchall()
        for l in liste:
            print(l)
        # Validation des modifications
        conn.commit() 
        #Insertion

        # Validation des modifications
        conn.close()
    #duration_list=Scrapping2.recuprerAAA("Fox")
    #inserer_Sql_duration(duration_list)

    #Enregistrer les données de durée épisode dans une table duration localement avec Scalingo

    def inserer_Sql_duration_scalingo(self,list_duration):
        URL_DB = "postgres://python_4680:IsWS_MRHjHOwShJlJ8yv@python-4680.postgresql.a.osc-fr1.scalingo-dbs.com:33825/python_4680?sslmode=prefer"
        
        try:
            conn = psycopg2.connect(URL_DB)
            print("Connexion réussie")
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS duration(
                    id SERIAL PRIMARY KEY,
                    nom_Serie TEXT,
                    duration INTEGER,
                    numero_Episode INTEGER,
                    id_episode INTEGER,
                    FOREIGN KEY (id_episode) REFERENCES episode(id)
                )
            ''')
            conn.commit()
            
            for data in list_duration:
                nom_serie = data['Nom de la série']
                duration_text = data['La durée de l\'épisode']
                duration = int(''.join(filter(str.isdigit, duration_text)))
                numero_episode = data['Numéro de episode']
                cur.execute("SELECT id FROM episode WHERE nom_Serie =%s and numero_Episode = %s", (nom_serie, numero_episode))
                id_episode=cur.fetchone()[0]
                cur.execute("INSERT INTO duration (nom_Serie, duration, numero_Episode,id_episode) VALUES (%s, %s, %s,%s)", (nom_serie, duration, numero_episode,id_episode))
            cur.execute("SELECT DISTINCT d.numero_Episode,d.nom_Serie,d.duration FROM duration d INNER JOIN episode e on d.id_episode=e.id where d.nom_serie=e.nom_Serie")
            liste=cur.fetchall()
            for l in liste:
                print(l)
            
            # Validation des modifications
            
            cur.execute("Select * from episode")
            tables = cur.fetchall()
            for table in tables:
                print(table)
        except psycopg2.Error as e:
            print(e)
        finally:
            if conn:
                cur.close()
                conn.close()
                print("Connexion fermée")





