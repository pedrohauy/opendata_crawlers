import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE covid (
            covid_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            Country VARCHAR(255) NOT NULL,
            TotalCases INTEGER NOT NULL,
            NewCases INTEGER,
            TotalDeaths INTEGER NOT NULL,
            NewDeaths INTEGER,
            TotalRecovered INTEGER NOT NULL,
            NewRecovered INTEGER,
            ActiveCases INTEGER,
            CriticalCases INTEGER,
            CasesPerMillion INTEGER,
            DeathsPerMillion INTEGER,
            Tests INTEGER,
            TestsPerMillion INTEGER,
            Population INTEGER
        )
        """,
        """
        CREATE TABLE economy (
            economy_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            dolar REAL NOT NULL,
            referencia_dolar DATE NOT NULL,
            selic REAL NOT NULL,
            referencia_selic DATE NOT NULL,
            ipca REAL NOT NULL,
            referencia_ipca DATE NOT NULL,
            igpm REAL NOT NULL,
            referencia_igpm DATE NOT NULL,
            caged INTEGER NOT NULL,
            referencia_caged DATE NOT NULL,
            pnad REAL NOT NULL,
            referencia_pnad DATE NOT NULL
        )
        """,
        """
        CREATE TABLE holidays (
            holidays_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            is_holiday BOOLEAN NOT NULL
        )
        """,
        """
        CREATE TABLE soccer (
            soccer_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            sao_paulo BOOLEAN NOT NULL,
            corinthians BOOLEAN NOT NULL,
            palmeiras BOOLEAN NOT NULL,
            santos BOOLEAN NOT NULL
        )
        """,
        """
        CREATE TABLE stocks (
            stocks_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            referencia DATE NOT NULL,
            abertura INTEGER NOT NULL,
            maximo INTEGER NOT NULL,
            minimo INTEGER NOT NULL,
            fechamento INTEGER NOT NULL,
            fechamento_ajustado INTEGER NOT NULL,
            volume INTEGER NOT NULL,
            variacao REAL NOT NULL
        )
        """,
        """
        CREATE TABLE traffic (
            traffic_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            eixo_codigo INTEGER NOT NULL,
            eixo_nome VARCHAR(255) NOT NULL,
            sentido VARCHAR(255) NOT NULL,
            lentidao REAL NOT NULL,
            porcentagem REAL NOT NULL
        )
        """,
        """
        CREATE TABLE weather (
            weather_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            chuva REAL NOT NULL,
            temperatura REAL NOT NULL,
            umidade REAL NOT NULL,
            pressao REAL NOT NULL,
            vento REAL NOT NULL
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()