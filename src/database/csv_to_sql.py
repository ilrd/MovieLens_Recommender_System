import pandas as pd
import sqlalchemy
import getpass
import os

os.chdir('/home/ilolio/PycharmProjects/Recommender_System-MovieLens/src/database')

username = input('Username: ')
password = getpass.getpass(prompt='Password: ')

engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@localhost/MovieLens")

print(f"Reading rating.csv...\n")
ratings_df = pd.read_csv('../../data/raw/rating.csv')
print(f"rating.csv successfully saved to ratings_df!\n")

ratings_df['userId'] = pd.Categorical(ratings_df['userId'])
ratings_df['userId'] = ratings_df['userId'].cat.codes

ratings_df['movieId'] = pd.Categorical(ratings_df['movieId'])
ratings_df['movieId'] = ratings_df['movieId'].cat.codes

# Save to sql table
table = 'RatingsTest'
print(f"Saving ratings_df to sql table {table}...\n")
ratings_df.iloc[:100].to_sql(table, con=engine, index=False, chunksize=10000, if_exists='replace')
print("Saved!")
