# Recommender System Project
**Code à rendre le 24/02 avant 20h**

Welcome on our AI316 Recommender System project page. This work was done by Maxence Monfort and Maxime Bourliatoux.

## Our API for the environnement 1

### Access

- Available online here http://54.229.199.104/
- Available locally with docker: (localhost:5002/)
```
cd api
docker-compose up --build
```

### Usage

We have made 5 routes:
- /
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

## To do
- [ ] Deployer API sur une AWS
- [ ] Faire environnement 3 (Implicit Feedback)
- [ ] Clean les environements à rendre en code


-------



This project have to be done by team of 2.

Each week a new environment is released. 
Each environment simulate different aspect of user behavior. 
Your goal as an agent is to implement a recommender system that get the best performances on each environments.

## Environments
Each environment will be accessible through a different IP address. 
Next examples used 1.2.3.4 but make sure to use the good ones instead. 

Each environment is specific to a user session. 
Logging have been send to you by email. 

To be identified each request should contain your user_id

```http request
user_id=aaaa
``` 

### First Environment
This environment encode the classic explicit feedback setting with user, item and rating.

The first thing to do is to call the reset method.
It will initialize the environment and return a new sample of historical data

#### Reset
```http
http://35.180.46.68/reset?user_id=aaaa
```

- Restart the environment with new random values.
- Return historical data already temporally aligned.


#### Predict

Call 
```http
http://1.2.3.4/predict?user_id=aaaa&predicted_score=0.761
```

Return
```json
{"next_item":158,"next_user":25,"rating":1}
```

Require:
- user_id
- predicted_score (for previous (user, item))

Return:
- rating
- next_user
- next_item

Notice the lag here. Rating returned by the environment correspond to the previously send (user, item).

## Second environment
The second environment is a variation of the first one that include covariates in the inputs (a.k.a. content based).

Methods are the same but you receive also a vector of features.
- next_variables


## Third environment
The third environment generate implicit feedback.

IP: 35.180.178.243

### Reset
output:
- nb_users
- nb_items
- state_history
- reward_history
- action_history
- next_state

### Predict
input: 
- recommended_item (int. item position in previous state, not item_id) 

output:
- reward
- state


### Notes
State is a vector of features for k available items. Let denote j one of them.
- state[j][0] = user
- state[j][1] = item
- state[j][2] = price
- state[j][3:] = variables 


## Performance evaluation

### Explicit feedback environments
The performance metric will be mse over 1000 steps on 3 independent run.

### Implicit feedback environments
Those environment explicitly gives you the reward at each steps.

The performance metric will be the cumulative reward over 1000 steps on 3 independent run.


## Deploy your own API
On the first environment you're asked to develop an API that can be requested to get prediction.

We should be able to deploy this API by running only

```bash
docker compose up --build
```

Evaluation method is the same than before but we will send queries every 100ms.
Non responding request will count as +1000.

### train
input:
- nb_users
- nb_items
- user_history
- item_history
- rating_history

do the training in less than 1 minute.

### predict
input:
- user
- item

output:
- rating

can be called every 100ms.

