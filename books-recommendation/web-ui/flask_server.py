#!/usr/bin/env python3

import logging
import os
import requests
import tensorflow as tf
from flask import Flask, json, jsonify, render_template, request
import pandas as pd
import numpy as np
import os 
import argparse
import base64

app = Flask(__name__)

args = None
rating_dataset = pd.read_csv(os.path.join(os.path.curdir,"data","ratings.csv"))
book_dataset = pd.read_csv(os.path.join(os.path.curdir,"data","books.csv"))
dataset = pd.merge(rating_dataset, book_dataset, how='left',left_on='book_id', right_on='id')


def encode_input(user_to_predict):

    
    item_data = np.array(list(set(dataset.id)))
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

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    result = request.form
    user_to_predict = int(result["user_id"])
    rec_count = int(result["rec_count"])
    headers = {'content-type': 'application/json'}
    json_data = {"instances": encode_input(user_to_predict)}
    request_data = json.dumps(json_data)
    ## model URL : http://book-recsys-service:8500/v1/models/book-recsys:predict
    response = requests.post(
          url=args.model_url, headers=headers, data=request_data)


    all_predictions = np.array(json.loads(response.text)["predictions"]).flatten()
    recommended_item_ids = (-all_predictions).argsort()[:rec_count]
    # recommended_item_ids = [1, 2, 3, 4, 5]

    bookes_rated = dict({ x[0]: x[1] for x in dataset[dataset.user_id == user_to_predict][["original_title","small_image_url"]].values})
    bookes_recommended = dict({ x[0]: x[1] for x in book_dataset[book_dataset['id'].isin(recommended_item_ids)][["original_title","small_image_url"]].values})

    
    return render_template("index.html", is_result=True, user_to_predict = user_to_predict,
                          bookes_rated = bookes_rated, 
                            bookes_recommended = bookes_recommended,
                            bookes_recommended_len = len(bookes_recommended))
  else:
    return render_template('index.html')



if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO,
                      format=('%(levelname)s|%(asctime)s'
                              '|%(pathname)s|%(lineno)d| %(message)s'),
                      datefmt='%Y-%m-%dT%H:%M:%S',
                      )
  logging.getLogger().setLevel(logging.INFO)
  logging.info("Starting flask.")
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--data_dir",
    default="",
    type=str)
  parser.add_argument(
    "--model_url",
    default="http://book-recsys-service:8500/v1/models/book-recsys:predict",
    type=str)
  parser.add_argument(
    "--port",
    default=9000,
    type=int)
  args = parser.parse_args()

  app.run(debug=True, host='0.0.0.0')
