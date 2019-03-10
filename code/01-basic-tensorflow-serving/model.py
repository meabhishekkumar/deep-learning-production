import tensorflow as tf 
import numpy as np 
import os 
from datetime import datetime
import shutil

tf.app.flags.DEFINE_integer('training_iteration', 500,'number of training iterations.')
FLAGS = tf.app.flags.FLAGS


def main(_):
    ### dataset : input and output
    xs = np.array([-1,0,1,2,3,4], dtype=np.float)
    ys = np.array([-3,-1,1,3,5,7], dtype=np.float)

    ### create simple model 
    model = tf.keras.Sequential([tf.keras.layers.Dense(units=1, input_shape=[1])])
    model.compile(optimizer='sgd',loss='mean_squared_error')

    ### train the model
    model.fit(xs, ys, epochs=FLAGS.training_iteration)
    print("trained the model")

    ### predict using model 
    print("predict using model")
    print(model.predict([10.0]))

    ### export the model
    now = datetime.now() 
    model_folder = now.strftime("%m%d%Y%H%M%S")
    # clean the output foler
    shutil.rmtree(os.path.join(os.path.curdir,"output"))
    # create output folder
    os.makedirs(os.path.join(os.path.curdir,"output"))
    # full export path
    export_path = os.path.join(os.path.curdir,"output",model_folder)

    # export the model
    with tf.keras.backend.get_session() as sess:
        tf.saved_model.simple_save(
            sess,
            export_path,
            inputs={'input_number': model.input},
            outputs={t.name:t for t in model.outputs})
    print("exported the model")
    pass
        
if __name__ == '__main__':
    tf.app.run()

