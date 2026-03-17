import requests
import os
from dotenv import load_dotenv
import json
import time
import csv
import logging

load_dotenv()
steam_api_key = os.getenv("steam_api_key")

# Configurações do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Links da API
APP_LIST_URL = 'https://api.steampowered.com/IStoreService/GetAppList/v1/'
APP_LIST_PARAMS = {
    'key': steam_api_key,
    'include_games': True,
    'include_dlc': True,
    'include_software': True,
    'include_videos': False,
    'include_hardware': False,
    'last_appid': '0',
    'max_results': '50000',
}

CURRENT_PLAYERS_URL = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/'
CURRENT_PLAYERS_PARAMS = {
    'appid': 0,
}

TOP_PLAYED_URL = 'https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/'

#########################################################
#                 Funções de AppID                      #
#########################################################
def get_appids():
    '''
    Acessa a API da steam e cadastra todos os AppIds
    '''
    bloco = 'get_appids'
    logging.info('Iniciando processo de obtenção de AppIds', )
    last_appid = 0
    arquivo = 'apps_data.csv'
    estado_arquivo = os.path.isfile(arquivo)
    session = requests.Session()

    logging.info("Buscando AppIds na Steam Web API")
    while last_appid is not None:
        try:
            response = session.get(APP_LIST_URL, params=APP_LIST_PARAMS)
            response.raise_for_status()
            
            data = response.json()
            conteudo = data.get('response', {})
            apps = conteudo.get('apps', [])
            logging.info(f"Jogo: {apps["appid"]}:{apps["name"]} recebido")

            with open(arquivo, 'a', newline='', encoding='utf-8') as f:
                fieldnames = ['appid', 'name', 'last_modified', 'price_change_number']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not estado_arquivo:
                    writer.writeheader()
                    estado_arquivo = True
                writer.writerows(apps)
                
            last_appid = conteudo.get('last_appid')

            APP_LIST_PARAMS['last_appid'] = last_appid

            time.sleep(1)

        except Exception as e:
            logging.error(f'Erro na request - {e} - Bloco: {bloco}')
            break

def pegar_last_appid():
    '''
    Acessa os AppIds e pega o último valor da lista
    '''
    arquivo = 'apps_data.csv'

    if not os.path.exists(arquivo):
        return 0

    with open(arquivo, 'r', encoding='utf-8') as f:
        leitor = list(csv.reader(f))
        if len(leitor) <= 1:
            return 0
        
        return leitor[-1][0]

def atualiza_appids():
    '''
    Atualiza a lista de AppIds a partir do último app na lista
    '''
    bloco = 'atualiza_appids'
    arquivo = 'apps_data.csv'
    session = requests.Session()
    estado_arquivo = os.path.isfile(arquivo)

    last_appid = pegar_last_appid()
    APP_LIST_PARAMS['last_appid'] = last_appid

    try:
        response = session.get(APP_LIST_URL, params=APP_LIST_PARAMS)
        response.raise_for_status()

        data = response.json()
        conteudo = data.get('response', {})
        apps = conteudo.get('apps', [])

        with open(arquivo, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['appid', 'name', 'last_modified', 'price_change_number']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(apps)

    except Exception as e:
        logging.error(f'Erro na request - {e} - Bloco: {bloco}')

#########################################################
#            Funções de contagem de players             #
#########################################################

def get_top_played():
    '''
    Busca os top 100 jogos com maior número de players simultâneos
    '''
    bloco = 'get_top_played'
    arquivo = 'concurrent_player_rank.csv'
    session = requests.Session()

    try:
        response = session.get(TOP_PLAYED_URL)
        response.raise_for_status()

        data = response.json()
        conteudo = data.get('response', {})
        apps = conteudo.get('ranks', [])
        for i in apps:
            print(i['appid'])
            nome = procurar_nome(i['appid'])
            print(nome)
            i['name'] = nome

        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['rank', 'appid', 'last_week_rank', 'peak_in_game', 'name']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(apps)

    except Exception as e:
        logging.error(f'Erro na request - {e} - Bloco: {bloco}')
        
#########################################################
#                 Funções auxiliares                    #
#########################################################

def carregar_ids(arquivo):
    '''
    Função auxiliar para carregar individualmente cada AppId

    :param arquivo: Local do arquivo
    '''
    with open(arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            yield linha['appid']

def procurar_nome(appid):
    arquivo = 'apps_data.csv'
    appid = str(appid)

    with open(arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            if linha['appid'] == appid:
                return linha['name']

if __name__ == '__main__':
    arquivo = 'apps_data.csv'
    estado_arquivo = os.path.isfile(arquivo)

    last_appid = pegar_last_appid()

    try:
        if estado_arquivo:
            try:
                atualiza_appids()
            except Exception as e:
                logging.error(f'Não foi possível atualizar a lista de AppIds - {e}')
        else:
            try:
                get_appids()
            except Exception as e:
                logging.error(f'Não foi possível criar a lista de AppIds - {e}')
    except Exception as e:
        logging.error(f'Não foi possível detectar o estado da lista de Appids - {e}')

    try:
        get_top_played()
    except Exception as e:
        logging.error(f'Não foi possível buscar a lista dos mais jogados {e}')

    new_last_appid = pegar_last_appid()

    if last_appid == new_last_appid:
        logging.info('Nenhuma atualização na lista de AppIds')
    else:
        logging.info('Lista de AppIds atualizada')

    logging.info('EXECUÇÃO FINALIZADA')