import pandas as pd
from datetime import datetime
from opendata import pgbind

# Monta URL no formato do Sistema Gerenciador de Séries Temporais do Banco Central
def get_url_bc(number):
    url_bc = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.NNNN/dados?formato=json"

    url_bc = url_bc.replace("NNNN", str(number))

    return url_bc

# Retorna a Série Temporal com os dados econômicos desejados
def bc_data(number):
    url = get_url_bc(number)
    df = pd.read_json(url)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

    return df

def get_last_data(df):
    return df.tail(1)

# Converte dataframe em dicionário
def make_dict(df):
    dict_list = df.to_dict(orient="records")
    info = dict_list[0]

    return info

def format_time(data):
    data["data"] = data["data"].strftime("%Y-%m-%d")

    return data

def aggregate_indicators(indicators):
    table = {}
    for indicator, number in indicators.items():
        df = bc_data(number)
        df = get_last_data(df)
        info = make_dict(df)
        info = format_time(info)
        table[indicator] = info["valor"]
        table["referencia_" + indicator] = info["data"]

    return table

def get_features(indicators):
    timestamp = datetime.now()
    features = {}
    features["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    for key, value in aggregate_indicators(indicators).items():
        features[key] = value
    
    return features

if __name__ == '__main__':
    indicators = {
        "dolar" : 1,
        "selic": 432,
        "ipca": 433,
        "igpm": 189,
        "caged": 28763,
        "pnad": 24369
    }

    features = get_features(indicators)
    print(features)

    # sql = pgbind.build_sql_query(features, "economy")
    # print(sql)

    # pgbind.insert_into_db(features, "economy")