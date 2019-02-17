from flask import Flask, request, jsonify
from time import sleep
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

@app.route('/train', methods=['GET'])
def train():
    global model, env, USER_ID

    nb_users = int(request.args.get('nb_users'))
    nb_items = int(request.args.get('nb_items'))
    item_history = ast.literal_eval(request.args.get('item_history'))
    user_history = ast.literal_eval(request.args.get('user_history'))
    rating_history = ast.literal_eval(request.args.get('rating_history'))

    model.train(nb_users, nb_items, user_history, item_history, rating_history)
    return 'Train finished'

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
    predicted_score = model.predict(user_id, item_id)
    d = {'predicted score': float(predicted_score)}
    return jsonify(d)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
