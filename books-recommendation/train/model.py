from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import sys
import numpy as np
import tensorflow as tf
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from tensorflow.keras.models import Model


n_users = 53424
n_items = 10000

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tf-data-dir',
                      type=str,
                      default='/tmp/data/ratings.csv',
                      help='GCS path or local path of training data.')
    parser.add_argument('--tf-model-dir',
                      type=str,
                      default='/tmp/model/',
                      help='GCS path or local directory.')
    parser.add_argument('--tf-export-dir',
                      type=str,
                      default='/tmp/export/',
                      help='GCS path or local directory to export model')
    

    parser.add_argument('--tf-train-steps',
                        type=int,
                        default=100,
                        help='The number of training steps to perform.')
    parser.add_argument('--tf-embedding-size',
                        type=int,
                        default=10,
                        help='The embedding size.')

    parser.add_argument('--tf-batch-size',
                        type=int,
                        default=1024,
                        help='The number of batch size during training')
    
    args = parser.parse_args()
    return args

def parser(item_id, user_id, rating):
    x = {
        'User-Input': user_id,
        'Item-Input': item_id
     }
    
    y = rating
    return x,y    


def train_input_fn(csv_path, batch_size=1024, buffer_size=1024):
    dataset = (
        tf.data.experimental.CsvDataset(
            filenames=csv_path,
            record_defaults=[tf.int32, tf.int32, tf.int32],
            select_cols=[0, 1, 2],
            field_delim=",",
            header=True)
        .map(parser)
        .shuffle(buffer_size=buffer_size)
        .batch(batch_size)
        .prefetch(batch_size)
    )
    iterator = dataset.make_one_shot_iterator()
    batch_feats, batch_labels = iterator.get_next()
    return batch_feats, batch_labels

def eval_input_fn(csv_path, batch_size=1000):
    dataset = (
        tf.data.experimental.CsvDataset(
            filenames=csv_path,
            record_defaults=[tf.int32, tf.int32, tf.int32],
            select_cols=[0, 1, 2],
            field_delim=",",
            header=True)
        .map(parser)
        .batch(batch_size)
    )
    iterator = dataset.make_one_shot_iterator()
    batch_feats, batch_labels = iterator.get_next()
    return batch_feats, batch_labels


def get_estimator(args):
    # creating book embedding path
    item_input = Input(shape=[1], name="Item-Input")
    item_embedding = Embedding(n_items+1, args.tf_embedding_size, name="Item-Embedding")(item_input)
    item_vec = Flatten(name="Flatten-Items")(item_embedding)

    # creating user embedding path
    user_input = Input(shape=[1], name="User-Input")
    user_embedding = Embedding(n_users+1, args.tf_embedding_size, name="User-Embedding")(user_input)
    user_vec = Flatten(name="Flatten-Users")(user_embedding)

    # concatenate features
    conc = Concatenate()([item_vec, user_vec])

    # add fully-connected-layers
    fc1 = Dense(128, activation='relu')(conc)
    fc2 = Dense(32, activation='relu')(fc1)
    out = Dense(1)(fc2)

    # Create model and compile it
    model = Model([user_input, item_input], out)
    model.compile('adam', 'mean_squared_error')
    model.summary()
    return tf.keras.estimator.model_to_estimator(keras_model=model,model_dir=args.tf_model_dir)


def main(_):
    tf.logging.set_verbosity(tf.logging.INFO)
    args = parse_arguments()

    tf_config = os.environ.get('TF_CONFIG', '{}')
    tf.logging.info("TF_CONFIG %s", tf_config)
    tf_config_json = json.loads(tf_config)
    cluster = tf_config_json.get('cluster')
    job_name = tf_config_json.get('task', {}).get('type')
    task_index = tf_config_json.get('task', {}).get('index')
    tf.logging.info("cluster=%s job_name=%s task_index=%s", cluster, job_name,
                    task_index)

    is_chief = False
    if not job_name or job_name.lower() in ["chief", "master"]:
        is_chief = True
        tf.logging.info("Will export model")
    else:
        tf.logging.info("Will not export model")


    train_spec = tf.estimator.TrainSpec(input_fn = lambda: train_input_fn(args.tf_data_dir, batch_size=args.tf_batch_size, buffer_size=args.tf_batch_size), max_steps=args.tf_train_steps)
    eval_spec = tf.estimator.EvalSpec(input_fn = lambda: eval_input_fn(args.tf_data_dir, batch_size=args.tf_batch_size) ,steps=1,throttle_secs=1,
                                      start_delay_secs=1 )

    # estimator 
    estimator = get_estimator(args)
    print("Train and evaluate")
    tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
    print("Training done")

    # exporting model
    if is_chief:
        # setup feature specification for serving
        feature_spec = {
            'User-Input' : tf.FixedLenFeature(shape=[1], dtype=np.float32),
            'Item-Input' : tf.FixedLenFeature(shape=[1], dtype=np.float32)
        }
        print("Export saved model")
        serving_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)
        export_dir = estimator.export_savedmodel(args.tf_export_dir, 
                                       serving_input_receiver_fn=serving_fn)

        print("Done exporting the model")

    
if __name__ == '__main__':
    tf.app.run()