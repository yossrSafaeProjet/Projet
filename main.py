# Avec la syntaxe from ... import ... on import un seul  objet
from retriever import Retriever
from processor import Processor
from alerter import Alerter

# Avec la syntaxe import .... on import tout le package
import datetime

# Avec la syntaxe from ... import * on importe tout  🚨🚨 a ne pas utiliser
# risque de conflit avec un autre objet (fonction, class, variable)
# qui aurait le même nom
# ici pas de risque : seulement une fonction nommée time_exec
from time_exec import *


def main():
    starting_time = datetime.datetime.now()

    url = "https://www.spin-off.fr/calendrier_des_series.html"

    retriever_instance = Retriever(url=url)
    ps = retriever_instance.get_page_source()

    processor_instance = Processor(text=ps)
    divs_crew_names = processor_instance.extract_crew_names()

    alerter = Alerter()
    alerter.alert("\n".join(divs_crew_names))

    ending_time = datetime.datetime.now()

    time_exec(starting_time, ending_time)


if __name__ == "__main__":
    main()
