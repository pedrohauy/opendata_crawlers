import psycopg2

def build_sql_query(features, table):
    keys = [key for key in features.keys()]
    key_string = ",".join(keys)
    placeholders = ["%s" for i in range(len(keys))]
    placeholders_string = ",".join(placeholders)

    sql = "INSERT INTO " + table + " (" + key_string + ") VALUES (" + placeholders_string + ")"

    return sql

def insert_into_db(features, table):
    conn = psycopg2.connect(
        host="localhost",
        database="opendata",
        user="pedro",
        password="uIcKholVeRvoMenE")

    cur = conn.cursor()

    sql = build_sql_query(features, table)
    values = tuple([value for value in features.values()])
    cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()

def get_last_record(table):
    conn = psycopg2.connect(
        host="localhost",
        database="opendata",
        user="pedro",
        password="uIcKholVeRvoMenE")

    cur = conn.cursor()

    sql = f"SELECT * FROM {table} ORDER BY {table}_id DESC LIMIT 1"
    cur.execute(sql)
    record = cur.fetchone()

    cur.close()
    conn.close()

    return record

def get_column_names(table):
    conn = psycopg2.connect(
        host="localhost",
        database="opendata",
        user="pedro",
        password="uIcKholVeRvoMenE")

    cur = conn.cursor()

    sql = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
    sql += "table_name = '{}';".format(table)
    cur.execute(sql)

    col_names = (cur.fetchall())
    columns = []
    for tup in col_names:
        columns += [tup[0]]

    cur.close()
    conn.close()

    return columns