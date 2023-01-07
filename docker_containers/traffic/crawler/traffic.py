import pandas as pd
from datetime import datetime
from opendata import pgbind

# Realiza Web Scraping na página da CET
def cet_realtime_data():
    url_cet = 'http://cetsp1.cetsp.com.br/monitransmapa/IMG4/eixos.asp'

    tables = pd.read_html(url_cet)
    df = tables[0]
    df.columns = ['eixo','sentido','lentidao','porcentagem','tendencia']
    df.drop(columns='tendencia', inplace=True)

    return df

# Limpa a coluna "Eixo"
def process_eixo(df):
    processed = df['eixo'].str.split(" - ", expand=True)
    df["eixo_codigo"] = processed[0]
    df["eixo_nome"] = processed[1]
    df.drop(columns=["eixo"], inplace=True)

    return df

def process_lentidao(df):
    df['lentidao'] = df['lentidao']/10

    return df

# Limpa a coluna "Porcentagem"
def process_porcentagem(df):
    processed = df['porcentagem'].str.split(expand=True)
    df['porcentagem'] = processed[0]
    df['porcentagem'] = df['porcentagem'].apply(lambda x: x.replace(',', '.'))
    df['porcentagem'] = df['porcentagem'].astype("float")

    return df

def insert_timestamp(df):
    timestamp = datetime.now()
    df["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return df

if __name__ == '__main__':
    data = cet_realtime_data()
    data = process_eixo(data)
    data = process_lentidao(data)
    data = process_porcentagem(data)
    data = insert_timestamp(data)

    data = data[['timestamp', 'eixo_codigo','eixo_nome', 'sentido','lentidao','porcentagem']]

    features = data.to_dict(orient="records")
    print(features)

    # for feature in features:
    #     sql = pgbind.build_sql_query(feature, "traffic")
    #     print(sql)

    #     pgbind.insert_into_db(feature, "traffic")