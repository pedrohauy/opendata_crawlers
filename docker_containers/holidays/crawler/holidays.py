import pandas as pd
from datetime import datetime, time
from opendata import pgbind

# Monta URL de feriados bancários com o ano corrente
def get_url_anbima(date):
    url_anbima = 'https://www.anbima.com.br/feriados/fer_nacionais/YYYY.asp'

    year = date.year
    url_anbima = url_anbima.replace("YYYY", str(year))

    return url_anbima

# Realiza Web Scraping na página da ANBIMA
def anbima_data(date):
    url = get_url_anbima(date)
    tables = pd.read_html(url)
    df = tables[2]

    df = df[1:]
    df.columns = ['data', 'dia_semana', 'feriado']

    return df

# Converte a coluna "Data" para tipo datetime
def convert_to_datetime(df):
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%y")
    return df

# Verifica se a data indicada é um feriado
def check_holiday(df, date):
    holidays = list(df["data"])
    year = date.year

    # Feriados incluídos manualmente
    holidays.append(datetime(year,1,25)) # aniversário de SP
    holidays.append(datetime(year,7,9)) # revolução constitucionalista
    holidays.append(datetime(year,11,20)) # consciência negra

    holiday_dates = [day.date() for day in holidays]
    day_to_check = date.date()

    return True if day_to_check in holiday_dates else False

def get_features(timestamp, data):
    features = {}
    features["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    features["is_holiday"] = check_holiday(data, timestamp)

    return features

if __name__ == '__main__':
    timestamp = datetime.now()
    # now = datetime(2021,9,7)
    data = anbima_data(timestamp)
    data = convert_to_datetime(data)

    features = get_features(timestamp, data)
    print(features)

    # sql = pgbind.build_sql_query(features, "holidays")
    # print(sql)

    # pgbind.insert_into_db(features, "holidays")