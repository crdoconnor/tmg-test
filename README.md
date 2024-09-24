# TMG test

To run:

* Check out repository
* Put OPENAI_API_KEY=<< openai key >>  in .env file
* make build
* make run

To test:

* make test


## Deploying in the cloud

* Create docker container which installs packages and runs uvicorn
* Push docker container to registry
* Create secret in secret storage in cloud
* Create service manifest (e.g. in kubernetes) which will run container as a service and inject the secret as an environment variable

## Testing

* Already has one test - end to end (might be flaky).
* Inject the LLM Runner as a dependency in fastapi, swap with fake to run dependency-less unit tests.
* For testing the LLM build up a test set of recipes and expected tags and evaluate response.
