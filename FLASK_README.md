# flask-api
An example flask rest API server.

To build production, type `make prod`.

To create the env for a new developer, run `make dev_env`.

# Instructions for runnign the app locally
### 1. Set environment variables
- `export PYTHONPATH=$PYTHONPATH:$(pwd)`
- For using MongoDB Atlas: 
  - `export CLOUD_MONGO=1`
  - `export  CLOUD_MONGO_USER=`
  - `export  CLOUD_MONGO_PW=`
### 2. To run the app
- `. ./local.sh`

### 3. For testing
- `make all_tests`