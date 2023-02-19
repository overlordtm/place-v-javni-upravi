import urllib3
import pandas as pd
import json
import html

BASE_URL = 'http://www.pportal.gov.si'

# Create a pool manager to handle multiple requests
http = urllib3.PoolManager()
http.headers['User-Agent'] = 'pju-fetch/0.1'


def fetch_payout_types() -> pd.DataFrame:
    COLS = ['Datum', 'Zaposleni (ure)', 'Zapolseni (placa)', 'Zaposleni', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'N', 'O'] 

    df = pd.DataFrame()
    r = http.request('GET', f'{BASE_URL}/tipimesec.txt')
    df = pd.DataFrame(json.loads(r.data.decode('iso-8859-2'))['aaData'], columns=COLS)

    df[['Mesec', 'Leto']] = df['Datum'].str.split('.', expand=True)
    df.drop('Datum', axis=1, inplace=True)
    # Convert the Month and Year columns to integers
    df['Mesec'] = df['Mesec'].astype(int)
    df['Leto'] = df['Leto'].astype(int)

    df.set_index(['Leto', 'Mesec'], inplace=True)
    df.sort_index(inplace=True)

    return df

def fetch_payout_subsum(year: int, month: int) -> pd.DataFrame:
    data = []

    for i in range(1, 24):
        r = http.request('GET',  f'{BASE_URL}/ISPAP_{year}/{month}_{year}/POD/{i}_POD_VSOTE_VRST{month}.txt')
        data.append(dict(list(map(lambda row: row.split(':'), r.data.decode('utf-8').splitlines()))))

    return pd.DataFrame.from_records(data, index='POD')

def fetch_payout_averages(year: int, month: int) -> pd.DataFrame:
    COLS = ['PODSKUPINA', 'PU', 'Naziv PU', 'Zaposlitve', 'Bruto placa', 'NA1', 'C', 'NA2', 'D', 'NA3', 'E', 'NA4', 'NA5','NA6', 'I', 'NA7', 'J', 'NA8', 'O', 'NA9']
    r = http.request('GET',  f'{BASE_URL}/ISPAP_{year}/{month}_{year}/PU/PU_POVPRECJE_{month}.txt')

    df = pd.DataFrame(json.loads(html.unescape(r.data.decode('iso-8859-2')))['aaData'], columns=COLS)

    return df

def fetch_payouts_by_position(year: int, month: int) -> pd.DataFrame:
    COLS = ["Podskupina", "Šifra PU", "Naziv PU", "Šifra DM", "Naziv DM" ,"Zaposlitve plača","Bruto plača","C","D","E","F","I","J","O"]
    r = http.request('GET',  f'{BASE_URL}/ISPAP_{year}/{month}_{year}/DM/DM_VSI_BRUTOPLACA{month}.txt')

    df = pd.DataFrame(json.loads(html.unescape(r.data.decode('iso-8859-2')))['aaData'], columns=COLS)
    return df