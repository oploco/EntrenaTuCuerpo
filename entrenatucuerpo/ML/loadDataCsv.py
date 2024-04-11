import requests
import csv
from pathlib import Path

CRYPTOS = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana', 'XRP', 'Lido Staked Ether', 'USDC', 'Dogecoin', 'Cardano',
           'Avalanche', 'Shiba Inu']


def obtener_datos_desde_api():
    url_api = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    respuesta = requests.get(url_api)
    datos_json = respuesta.json()
    return datos_json


def guardar_en_csv_Bitcoin(datos, nombre_archivo):
    fileName = nombre_archivo
    fileObj = Path(fileName)
    if (fileObj.is_file()):
        precio = [datos['current_price']]
        fechault = [datos['last_updated']]

        lectura = [datos['current_price'], datos['last_updated']]

        with open(nombre_archivo, 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(lectura)
    else:
        with open(nombre_archivo, 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(['Precio', 'fecha'])


if __name__ == "__main__":
    datos_desde_api = obtener_datos_desde_api()

    for crypto in CRYPTOS:
        nombre_archivo_csv_Bitcoin = "FilesCryptos/" + crypto + ".csv"

        for elemento in datos_desde_api:
            for clave, valor in elemento.items():
                if valor == crypto:
                    print(elemento['current_price'])
                    guardar_en_csv_Bitcoin(elemento, nombre_archivo_csv_Bitcoin)
                    break