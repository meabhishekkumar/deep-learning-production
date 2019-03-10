import tensorflow as tf 
import numpy as np 
import os 
from datetime import datetime


### dataset : input and output
xs = np.array([-1,0,1,2,3,4], dtype=np.float)
ys = np.array([-3,-1,1,3,5,7], dtype=np.float)

### create simple model 
model = tf.keras.Sequential([tf.keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd',loss='mean_squared_error')

### train the model
model.fit(xs, ys, epochs=500)

### predict using model 
print(model.predict([10.0]))

### export the model
now = datetime.now() 
model_folder = now.strftime("%m%d%Y%H%M%S")
export_path = os.path.join(os.path.curdir,"output",model_folder)

with tf.keras.backend.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input_number': model.input},
        outputs={t.name:t for t in model.outputs})

