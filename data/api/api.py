import requests
import os
from dotenv import load_dotenv
import json
import time
import csv

load_dotenv()
steam_api_key = os.getenv("steam_api_key")

# Links da API
GetAppListURL = 'https://api.steampowered.com/IStoreService/GetAppList/v1/'
GetAppListPARAMS ={
    'key': steam_api_key,
    'include_games': True,
    'include_dlc': True,
    'include_software': True,
    'include_videos': False,
    'include_hardware': False,
    'last_appid': '0',
    'max_results': '50000',
}

def get_appids():
    last_appid = 0
    arquivo = 'apps_data.csv'
    estado_arquivo = os.path.isfile(arquivo)
    session = requests.Session()

    while last_appid is not None:
        try:
            response = session.get(GetAppListURL, params=GetAppListPARAMS)
            response.raise_for_status()
            
            data = response.json()
            conteudo = data.get('response', {})
            apps = conteudo.get('apps', [])

            with open(arquivo, 'a', newline='', encoding='utf-8') as f:
                fieldnames = ['appid', 'name', 'last_modified', 'price_change_number']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not estado_arquivo:
                    writer.writeheader()
                    estado_arquivo = True
                writer.writerows(apps)

            last_appid = conteudo.get('last_appid')

            GetAppListPARAMS['last_appid'] = last_appid

            time.sleep(1)

        except Exception as e:
            print(f'Erro na request ({e})')
            break

def pegar_last_appid():
    arquivo = 'apps_data.csv'

    if not os.path.exists(arquivo):
        return 0

    with open(arquivo, 'r', encoding='utf-8') as f:
        leitor = list(csv.reader(f))
        if len(leitor) <= 1:
            return 0
        
        return leitor[-1][0]

def atualiza_appids():
    arquivo = 'apps_data.csv'
    session = requests.Session()

    last_appid = pegar_last_appid()
    GetAppListPARAMS['last_appid'] = last_appid

    try:
        response = session.get(GetAppListURL, params=GetAppListPARAMS)
        response.raise_for_status()

        data = response.json()
        conteudo = data.get('response', {})
        apps = conteudo.get('apps', [])

        with open(arquivo, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['appid', 'name', 'last_modified', 'price_change_number']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(apps)

    except Exception as e:
        print(f'Erro na request ({e})')


atualiza_appids()

print()
print('EXECUÇÃO FINALIZADA')