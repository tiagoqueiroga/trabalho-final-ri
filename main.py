import requests
import sqlite3
import os
from bs4 import BeautifulSoup


def cria_conexao_sqlite(db_file):
    print("Criando banco de dados SQLite")
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        conn.close()

# Url dos dados juntos com os atributos
def define_url(attrs):
    return "http://ufostalker.com:8080/mostRecentEvents?page=" + str(attrs["page"]) + "&size=" + str(attrs["page_size"])

def busca_observacoes():
    print("Buscando casos de ovnis no site ufostalker.com")
    response = requests.get(define_url({"page":0,"page_size":1}))

    total_observacoes = response.json()["totalElements"] | 0
    total_paginas = response.json()["totalPages"] | 0
    total_observacoes = response.json()["totalElements"] | 0
    observacoes = response.json()["content"] 

    grava_observacoes_no_banco(observacoes)


def grava_observacoes_no_banco(observacoes):
    for observacao in observacoes:
        print(observacao)


if __name__ == "__main__":

    # Cria conecao com banco de dados sqlite
    cria_conexao_sqlite(os.path.dirname(os.path.realpath(__file__)) + '/observacoes.db')

    # Busca apenas um caso para verificando que o site está online
    response = requests.get(define_url({"page":0,"page_size":1}))

    if response.status_code != 200:
        print("Erro ao acessar informações")

    # Faz busca de todos as observações
    else:
        busca_observacoes()