from flask import Flask, request, jsonify
from time import sleep
import pandas as pd
import numpy as np

from tensorflow.keras.layers import Input, Embedding, Flatten, Dot
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping

old_env = 'http://52.47.62.31/'
new_env = 'http://35.180.254.42/'
app = Flask(__name__)
USER_ID = '9G08LOYFU88BJ8GHNRU3'

env = old_env

"""Requête"""
r = request.get(url=env+'reset', params= {'user_id':USER_ID})
sleep(0.05)
data = r.json()
nb_items = data['nb_items']
nb_users = data['nb_users']
next_item = data['next_item']
next_user = data['next_user']
item_history = data['item_history']
user_history = data['user_history']
rating_history = data['rating_history']

ratings = pd.DataFrame(data={'user_id':user_history, 'item_id':item_history, 'rating': rating_history})

"""Définition du modèle"""
user_id_input = Input(shape=[1],name='user')
item_id_input = Input(shape=[1], name='item')

embedding_size = 5
user_embedding = Embedding(output_dim=embedding_size, input_dim=nb_users + 1,
                        input_length=1, name='user_embedding')(user_id_input)

item_embedding = Embedding(output_dim=embedding_size, input_dim=nb_items + 1,
                        input_length=1, name='item_embedding')(item_id_input)

user_vecs = Flatten()(user_embedding)
item_vecs = Flatten()(item_embedding)

y = Dot(axes=1)([user_vecs, item_vecs])

model = Model(inputs=[user_id_input, item_id_input], outputs=y)
model.compile(optimizer='adam', loss='MSE')
early_stopping = EarlyStopping(monitor='val_loss', patience=2)
model.fit([ratings['user_id'], ratings['item_id']], ratings['rating'],
                    batch_size=64, epochs=20, validation_split=0.1,
                    shuffle=True, callbacks=[early_stopping])

model.predict([[1], [2]])[0,0]

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/predict", methods=['GET'])
def predict():
    global model
    user_id = request.args.get('user_id')
    item_id = request.args.get('item_id')
    user_id = int(user_id)
    item_id = int(item_id)
    predicted_score = model.predict([[user_id], [item_id]])[0,0]
    d = {'predicted score': float(predicted_score)}
    return jsonify(d)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
