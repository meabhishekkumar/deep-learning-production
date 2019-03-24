import requests

import tensorflow as tf
import json
import base64
import pandas as pd
import numpy as np

max_item_id = 1682 
user_id = 1
rating_dataset = pd.read_csv("data/ratings.csv")
book_dataset = pd.read_csv("data/books.csv")
dataset = pd.merge(rating_dataset, book_dataset, how='left',left_on='book_id', right_on='id')

def encode_input():
    user_to_predict = 1 
    item_data = np.array(list(set(dataset.id)))
    user_to_predict = 1  # let's predict for first user
    user_data = np.array([user_to_predict for i in range(len(item_data))]) # repeating the user_id to the times of each unique item
    
    inputs = pd.DataFrame({
    'User-Input': user_data,
    'Item-Input': item_data
    })


    examples = []
    
    for index, row in inputs.iterrows():
        feature = {}
        for col, value in row.iteritems():
            feature[col] = tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
        example = tf.train.Example(
            features=tf.train.Features(
                feature=feature
            )
        )
        b64_value = base64.b64encode(example.SerializeToString()).decode("utf-8")
        examples.append({"examples": {"b64": b64_value}})
    return examples





model_url = "http://localhost:8501/v1/models/test:predict"
headers = {'content-type': 'application/json'}
json_data = {"instances": encode_input()}
request_data = json.dumps(json_data)
response = requests.post(
      url=model_url, headers=headers, data=request_data)
#print(response.text)
all_predictions = np.array(json.loads(response.text)["predictions"]).flatten()
recommended_items = (-all_predictions).argsort()[:10]
print(recommended_items)
print(-np.sort(-all_predictions)[:10])