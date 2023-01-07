import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from opendata import pgbind

# Realiza Web Scraping na página do Worldometers
def worldometers_data():
    url_covid = "https://www.worldometers.info/coronavirus"

    response = requests.get(url_covid)

    return response

# Procura tabelas pela tag HTML <table>
def scrap_table(page):
    soup = BeautifulSoup(page.content, 'lxml')
    # Search for the table and extracting it
    table = soup.find('table', attrs={'id': 'main_table_countries_today'})

    # Object of the type: bs4.element.Tag
    return table

# Retorna lista com as linhas da tabela de países
def list_rows(table):
    rows = table.find_all("tr", attrs={"style": ""})

    data = []
    for i,item in enumerate(rows):    
        if i == 0:        
            data.append(item.text.strip().split("\n")[:16])        
        else:
            data.append(item.text.strip().split("\n")[:15])

    return data

# Converte lista em dataframe
def make_dataframe(data):
    columns = ["#","Country", "TotalCases", "NewCases",	"TotalDeaths",
                 "NewDeaths", "TotalRecovered", "NewRecovered", "ActiveCases", "CriticalCases",
                 "CasesPerMillion", "DeathsPerMillion", "Tests", "TestsPerMillion", "Population"]

    df = pd.DataFrame(data[2:], columns=columns)
    df.drop(columns="#", inplace=True)

    return df

def filter_country(df, country):
    filtered = df[df["Country"] == country]

    return filtered

# Converte dataframe em dicionário
def make_dict(df):
    dict_list = df.to_dict(orient="records")
    info = dict_list[0]

    return info

def get_features(data):
    timestamp = datetime.now()
    features = {}
    features["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    for key, value in make_dict(data).items():
        if key == "Country":
            features[key] = value
        else:
            if value != "":
                features[key] = int(value.replace(",",""))
            else:
                features[key] = None
    
    return features

if __name__ == '__main__':
    page = worldometers_data()
    table = scrap_table(page)
    raw_data = list_rows(table)
    df = make_dataframe(raw_data)
    df = filter_country(df, "Brazil")

    features = get_features(df)
    print(features)

    sql = pgbind.build_sql_query(features, "covid")
    print(sql)

    pgbind.insert_into_db(features, "covid")