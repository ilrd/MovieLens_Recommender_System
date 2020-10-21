import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import getpass
import os

os.chdir('/home/ilolio/PycharmProjects/Recommender_System-MovieLens/src/database')

username = input('Username: ')
password = getpass.getpass(prompt='Password: ')

engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@localhost/MovieLens")

query = "SELECT * FROM Ratings LIMIT 10000;"

print(f"Reading rating.csv...\n")
ratings_df = pd.read_sql(query, engine, chunksize=10000)
print(f"rating.csv successfully saved to ratings_df!\n")

next(ratings_df)
