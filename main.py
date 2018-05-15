import requests
import os
import db
from bs4 import BeautifulSoup

# Constantes
LIMITE_PAGINAS = 10
REPORTS_POR_PAGINA = 30
PAGINA_INICIAL = 0


# Url dos dados juntos com os atributos
def define_url(attrs):
    return "http://ufostalker.com:8080/mostRecentEvents?page=" + str(attrs["page"]) + "&size=" + str(attrs["page_size"])

def busca_reports():
    indice = PAGINA_INICIAL
    while (indice < LIMITE_PAGINAS):
        print("Buscando observações com mídias na página:" + str(indice + 1) + " - site ufostalker.com")
        response = requests.get(define_url({"page":indice,"page_size":REPORTS_POR_PAGINA}))
        conteudo = response.json()["content"] 
        reports = db.coleta_reports(conteudo)
        db.grava_reports(conn,reports)
        indice = indice + 1

def mostra_status_de_busca():
    for row in conn.execute('SELECT count(*) FROM ufo_reports'):
        print("Foram encontradas" + str(row).replace(',','') + " observações com mídia(Fotos ou vídeos)")

if __name__ == "__main__":

    # Cria conecao com banco de dados sqlite
    conn = db.cria_conexao_sqlite(os.path.dirname(os.path.realpath(__file__)) + '/ufo_sighting.db')
    db.cria_tabela_reports(conn)

    # Busca apenas um caso para verificando que o site está online
    response = requests.get(define_url({"page":0,"page_size":1}))

    # Erro ?
    if response.status_code != 200:
        print("Erro ao acessar informações")

    # Faz busca de todos as observações
    else:
        total_paginas = response.json()["totalPages"] | 0
        busca_reports()
        mostra_status_de_busca()
        
        # Fecha conexão
        conn.close()

