import yfinance as yf
from datetime import datetime, timedelta
from opendata import pgbind

def yahoo_data(date, ticker):
    today = date.date()
    last_week = today - timedelta(7)

    df = yf.download(ticker, start=last_week, end=today, progress=False)

    df.reset_index(inplace=True)
    columns = ["referencia", "abertura", "maximo", "minimo", "fechamento", "fechamento_ajustado", "volume"]
    df.columns = columns

    return df

def insert_change(df):
    df["variacao"] = df["fechamento"].pct_change()
    df["variacao"] = df["variacao"] * 100.0

    return df

def get_last_data(df):
    return df.tail(1)

# Converte dataframe em dicionário
def make_dict(df):
    dict_list = df.to_dict(orient="records")
    info = dict_list[0]

    return info

def format_time(data):
    data["referencia"] = data["referencia"].strftime("%Y-%m-%d")

    return data

def get_features(timestamp, data):
    features = {}
    features["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    for key, value in data.items():
        features[key] = value
    
    return features

if __name__ == '__main__':
    timestamp = datetime.now()

    data = yahoo_data(timestamp, "^BVSP")
    data = insert_change(data)
    data = get_last_data(data)
    info = make_dict(data)
    info = format_time(info)

    features = get_features(timestamp, info)
    print(features)

    sql = pgbind.build_sql_query(features, "stocks")
    print(sql)

    pgbind.insert_into_db(features, "stocks")