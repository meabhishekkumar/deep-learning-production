#!/usr/bin/env python3

import logging
import os
import requests
import tensorflow as tf
from flask import Flask, json, jsonify, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# args = None
# encoder = None
# rating_dataset = pd.read_csv("data/ratings.csv")
# book_dataset = pd.read_csv("data/books.csv")
# dataset = pd.merge(rating_dataset, book_dataset, how='left',left_on='book_id', right_on='id')


# def encode_input(user_to_predict):
    
#     item_data = np.array(list(set(dataset.id)))
#     user_data = np.array([user_to_predict for i in range(len(item_data))]) # repeating the user_id to the times of each unique item
    
#     inputs = pd.DataFrame({
#     'User-Input': user_data,
#     'Item-Input': item_data
#     })


#     examples = []
    
#     for index, row in inputs.iterrows():
#         feature = {}
#         for col, value in row.iteritems():
#             feature[col] = tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
#         example = tf.train.Example(
#             features=tf.train.Features(
#                 feature=feature
#             )
#         )
#         b64_value = base64.b64encode(example.SerializeToString()).decode("utf-8")
#         examples.append({"examples": {"b64": b64_value}})
#     return examples




# handle requests to the server
@app.route("/")
def main():
  # get url parameters for HTML template
  name_arg = request.args.get('name', 'mnist')
  addr_arg = request.args.get('addr', 'mnist-service')
  port_arg = request.args.get('port', '9000')
  args = {"name": name_arg, "addr": addr_arg, "port": port_arg}
  logging.info("Request args: %s", args)


  # render results using HTML template
  return render_template('index.html')



if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO,
                      format=('%(levelname)s|%(asctime)s'
                              '|%(pathname)s|%(lineno)d| %(message)s'),
                      datefmt='%Y-%m-%dT%H:%M:%S',
                      )
  logging.getLogger().setLevel(logging.INFO)
  logging.info("Starting flask.")
  app.run(debug=True, host='0.0.0.0')
