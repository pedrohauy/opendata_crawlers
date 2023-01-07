import requests
from datetime import datetime
from opendata import pgbind

# Retorna os dados meteorológicos do dia, da cidade de São Paulo, dado uma data (string: aaaa-mm-dd)
def inmet_daily_data(date):
    url_inmet = "https://apitempo.inmet.gov.br/estacao/"

    # Código A771 - Interlagos
    # Código A701 - Mirante de Santana
    url = url_inmet + date + "/" + date + "/" + "A701"
    response = requests.get(url)

    return response.json()

# Recebe os dados meteorológicos do dia e retorna os atributos de tempo de um determinado horario (int 0-23)
def inmet_hourly_data(data, hour):

    return data[hour]

# Retorna os atributos esperados
def get_features(timestamp, data):
    features = {}
    features["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    features["chuva"] = data["CHUVA"]
    features["temperatura"] = data["TEM_INS"]    
    features["umidade"] = data["UMD_INS"]
    features["pressao"] = data["PRE_INS"]
    features["vento"] = data["VEN_VEL"]

    return features

if __name__ == '__main__':
    timestamp = datetime.now()
    date = timestamp.date().strftime("%Y-%m-%d")
    hour = timestamp.time().hour

    sp_daily_data = inmet_daily_data(date)
    # print(sp_daily_data)
    # print(len(sp_daily_data))
    sp_hourly_data = inmet_hourly_data(sp_daily_data, hour)

    features = get_features(timestamp, sp_hourly_data)
    print(features)

    # sql = pgbind.build_sql_query(features, "weather")
    # print(sql)

    # pgbind.insert_into_db(features, "weather")