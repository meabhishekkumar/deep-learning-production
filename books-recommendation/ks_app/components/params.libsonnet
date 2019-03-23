{
  global: {
    // User-defined global parameters; accessible to all component and environments, Ex:
    // replicas: 4,
  },
  components: {
    // Component-level parameters, defined initially from 'ks prototype use ...'
    // Each object below should correspond to a component in the components/ directory
    train: {
      batchSize: 100,
      envVariables: 'GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/user-gcp-sa.json',
      exportDir: '',
      image: '',
      modelDir: '',
      name: 'books-recommendation-train',
      numPs: 0,
      numWorkers: 0,
      secret: '',
      secretKeyRefs: '',
      trainSteps: 200,
    },
    "book-recsys-deploy-gcp": {
      defaultCpuImage: 'tensorflow/serving:1.11.1',
      defaultGpuImage: 'tensorflow/serving:1.11.1-gpu',
      deployHttpProxy: 'false',
      enablePrometheus: 'true',
      gcpCredentialSecretName: 'user-gcp-sa',
      httpProxyImage: '',
      injectIstio: 'false',
      modelBasePath: '',
      modelName: 'book-recsys',
      name: 'book-recsys-deploy-gcp',
      numGpus: '0',
      versionName: 'v1',
    },
    "book-recsys-service": {
      enablePrometheus: 'true',
      injectIstio: 'false',
      modelName: 'book-recsys',
      name: 'book-recsys-service',
      serviceType: 'ClusterIP',
      trafficRule: 'v1:100',
    },
    "tensorboard": {
      envVariables: 'GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/user-gcp-sa.json',
      image: "tensorflow/tensorflow:1.12.0",
      logDir: "gs://example/to/model/logdir",
      name: "tensorboard",
      secret: '',
      secretKeyRefs: '',
    },
    "web-ui": {
      containerPort: 5000,
      image: "",
      name: "web-ui",
      replicas: 1,
      servicePort: 80,
      type: "ClusterIP",
    },
  },
}
