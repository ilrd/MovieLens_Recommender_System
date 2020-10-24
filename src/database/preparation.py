import pandas as pd
import sqlalchemy
import getpass


def get_ratings_df(rows=None):
    username = input('Username: ')
    password = getpass.getpass(prompt='Password: ')

    engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@localhost/MovieLens")
    if rows:
        query = f"SELECT * FROM Ratings LIMIT {rows};"
    else:
        query = "SELECT * FROM Ratings;"

    ratings_df = pd.read_sql(query, engine, chunksize=10000)

    return ratings_df
