docker build -t test -f Dockerfile.model .


docker run -it --rm test /opt/model.py --tf-train-steps=300 --tf-embedding-size=20