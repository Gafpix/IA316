# Recommender System Project

Welcome on our AI316 Recommender System project page.

This work was done by Maxence Monfort and Maxime Bourliatoux.

## Our code for the three environments

You will find our code in the directory /Notebooks. For each environment we have build a recommender system in its corresponding Notebook.

## Our API for the environment 1

### Access

- Available online here http://54.229.199.104/
- Available locally with docker: (localhost:5002/)
```
cd api
docker-compose up --build
```

### Usage

We have made 5 routes:
- /  (=homepage)
- train/
- predict/
- train_ui/
- predict_ui/

NB: The routes train_ui/ and predict_ui/ are the same as train/ and predict/ but return html files, for a easier usage.


#### Inputs

The route train/ takes as input a POST request with JSON data containing the folowing parameters: 
```
[nb_users, nb_items, user_history, item_history, rating_history]
```
(This JSON is typically the result of a reset request on the environnement1 API)

NB: If there is no data provided, the system will make a request to the reset/ route of the Environnement 1 API. 


The route predict/ takes two GET parameters as input: user_id and item_id.
```
predict?user_id=0&item_id=0
```


#### Outputs
The route train/ returns a string with the training time:
```
Training finished in 2.916 seconds!
```

The route predict/ returns a json with a rating:
```
{"rating":2.5387697219848633}
```
