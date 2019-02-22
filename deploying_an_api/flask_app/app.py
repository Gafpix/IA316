from flask import Flask, request, jsonify, render_template
from time import time
import requests
import pandas as pd
import numpy as np
import ast

from model import ModelAPI

env = 'http://52.47.62.31/'
app = Flask(__name__)
USER_ID = '9G08LOYFU88BJ8GHNRU3'


model = ModelAPI()


@app.route("/")
def hello():
    return render_template('home.html')


@app.route('/train', methods=['GET','POST'])
def train():
    global model, env, USER_ID
    data = request.get_json()
    if data == None:
        data = requests.get(url=env+'reset', params= {'user_id':USER_ID}).json()
    nb_users = int(data['nb_users'])
    nb_items = int(data['nb_items'])
    item_history = data['item_history']
    user_history = data['user_history']
    rating_history = data['rating_history']
    start = time()
    model.train(nb_users, nb_items, user_history, item_history, rating_history)
    end = time()
    return 'Training finished in {:.3f} seconds!'.format(end-start)


@app.route('/train_ui', methods=['GET','POST'])
def train_ui():
    global model, env, USER_ID
    data = request.get_json()
    if data == None:
        data = requests.get(url=env+'reset', params= {'user_id':USER_ID}).json()
    nb_users = int(data['nb_users'])
    nb_items = int(data['nb_items'])
    item_history = data['item_history']
    user_history = data['user_history']
    rating_history = data['rating_history']
    start = time()
    model.train(nb_users, nb_items, user_history, item_history, rating_history)
    end = time()
    res = '{:.3f}'.format(float(end-start))
    return render_template('train.html', time=res)


@app.route("/predict", methods=['GET'])
def predict():
    global model
    user_id = int(request.args.get('user_id'))
    item_id = int(request.args.get('item_id'))
    predicted_score = float(model.predict(user_id, item_id))
    d = {'rating': predicted_score}
    return jsonify(d)


@app.route("/predict_ui", methods=['GET'])
def predict_ui():
    global model
    user_id = int(request.args.get('user_id'))
    item_id = int(request.args.get('item_id'))
    predicted_score = float(model.predict(user_id, item_id))
    if predicted_score == -1:
        return render_template('result_error.html')
    return render_template('result.html', score=float(predicted_score), user_id=user_id, item_id=item_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
