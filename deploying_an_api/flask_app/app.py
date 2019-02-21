from flask import Flask, request, jsonify
from time import time
import requests
import pandas as pd
import numpy as np
import ast

from model import ModelAPI

old_env = 'http://52.47.62.31/'
new_env = 'http://35.180.254.42/'
app = Flask(__name__)
USER_ID = '9G08LOYFU88BJ8GHNRU3'

env = old_env

model = ModelAPI()

@app.route('/train', methods=['POST'])
def train():
    global model, env, USER_ID
    data = request.get_json()
    nb_users = int(data['nb_users'])
    nb_items = int(data['nb_items'])
    item_history = data['item_history']
    user_history = data['user_history']
    rating_history = data['rating_history']
    start = time()
    model.train(nb_users, nb_items, user_history, item_history, rating_history)
    end = time()
    return 'Training finished in {:.3f} seconds!'.format(end-start)

@app.route("/")
def hello():
    return "Hello World!!"

@app.route("/predict", methods=['GET'])
def predict():
    global model
    user_id = int(request.args.get('user_id'))
    item_id = int(request.args.get('item_id'))
    predicted_score = float(model.predict(user_id, item_id))
    d = {'predicted score': predicted_score}
    return jsonify(d)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
