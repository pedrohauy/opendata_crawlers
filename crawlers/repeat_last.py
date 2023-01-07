from opendata import pgbind

if __name__ == '__main__':
    tables = ["covid", "economy", "holidays", "soccer", "stocks"]

    for table in tables:
        columns = pgbind.get_column_names(table)[1:]
        last = pgbind.get_last_record(table)[1:]
        features = dict(zip(columns,last))
        sql = pgbind.build_sql_query(features, table)

        pgbind.insert_into_db(features, table)