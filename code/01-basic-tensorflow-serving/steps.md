
### Train Model and Export the model binaries

```
python model.py
```

### Inspect the model

```
pip install tensorflow-serving-api
```

```
saved_model_cli show --dir output/* --all
```

### Pull the Tensorflow Serving Image

```
docker pull tensorflow/serving
```

### Run Tensorflow Server with our model 

```
docker run -it --rm -p 8501:8501  -v "$PWD"/output:/models/test -e MODEL_NAME=test tensorflow/serving

```

### Test the Predictions using Curl 

```
curl -d '{"instances": [{ "input_number" : [10.0] },{ "input_number" : [20.0] }]}' \
  -X POST http://localhost:8501/v1/models/test:predict
```

### Optimizing Models 

Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA

Building the TensorFlow Serving development image

```
docker build -t $USER/tensorflow-serving-devel -f Dockerfile.devel https://github.com/tensorflow/serving.git#:tensorflow_serving/tools/docker
```

build a new serving image with our optimized binary and call it $USER/tensorflow-serving

```
docker build -t $USER/tensorflow-serving \
--build-arg TF_SERVING_BUILD_IMAGE=$USER/tensorflow-serving-devel \ https://github.com/tensorflow/serving.git#:tensorflow_serving/tools/docker
```


## Nice Reads:

Further optimizing for the CPU :

- https://medium.com/tensorflow/serving-ml-quickly-with-tensorflow-serving-and-docker-7df7094aa008

