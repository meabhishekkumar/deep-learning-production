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
    }
  },
}
