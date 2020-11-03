import pandas as pd
import sqlalchemy


def get_ratings_df(rows=None):
    f = open('../../sql_credentials')
    username = f.readline()[:-1]
    password = f.readline()
    f.close()

    engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@localhost/MovieLens")
    if rows:
        query = f"SELECT * FROM Ratings LIMIT {rows};"
    else:
        query = "SELECT * FROM Ratings;"

    ratings_df = pd.read_sql(query, engine, chunksize=10000)

    return ratings_df
