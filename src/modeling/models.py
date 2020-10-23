import os
from database.preparation import get_ratings_df
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import *
from tensorflow.keras import Model
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras import callbacks

os.chdir('/home/ilolio/PycharmProjects/Recommender_System-MovieLens/src/database')

datagen = get_ratings_df(rows=20_001_000)

df = pd.concat(list(datagen))

df['userId'] = pd.Categorical(df['userId'])
df['userId'] = df['userId'].cat.codes

df['movieId'] = pd.Categorical(df['movieId'])
df['movieId'] = df['movieId'].cat.codes

user_ids = df['userId'].values
movie_ids = df['movieId'].values
ratings = df['rating'].values

N = np.unique(user_ids).shape[0]
M = np.unique(movie_ids).shape[0]

# Embedding dimension
K = 5

u = Input((1,))
m = Input((1,))

u_emb = Embedding(N, K)(u)
m_emb = Embedding(M, K)(m)

u_emb = Flatten()(u_emb)
m_emb = Flatten()(m_emb)

x = Concatenate()([u_emb, m_emb])

x = Dense(1024, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(256, activation='relu')(x)
outputs = Dense(1)(x)

model = Model([u, m], outputs)

optimizer = keras.optimizers.Adam(lr=0.01)
model.compile(optimizer, 'mse', 'mae')

train_user, test_user, train_movie, test_movie, train_ratings, test_ratings = train_test_split(user_ids, movie_ids,
                                                                                               ratings, test_size=0.2,
                                                                                               shuffle=True)

ratings_mean = train_ratings.mean()
train_ratings -= ratings_mean
test_ratings -= ratings_mean

# Callbacks
fit_callbacks = [
    callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.1,
        patience=3,
        verbose=1,
        min_lr=0.000001,
    ),
    callbacks.ModelCheckpoint(
        'chechpoints/model_checkpoint.h5',
        monitor='val_loss',
        verbose=0,
        save_best_only=True,
    ),
]
history = model.fit([train_user, train_movie], train_ratings, batch_size=3072, epochs=18,
                    validation_data=([test_user, test_movie], test_ratings), callbacks=fit_callbacks)

plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')

model.save('10epochs_model.h5')
