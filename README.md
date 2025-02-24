# bar-patron-tracking

# Prerequistes

The following tools need to be installed in order for the system to work:

- Python 13.2
- Docker
- Docker compose

# Setup Guide
## Create a Environment variable file
You can create a ".env" file in the root of your project directory.

![".env" file in the root](/images/env_loc.png)

In order for the system to run the following varibales must be set:


- POSTGRES_PASSWORD
- POSTGRES_USER
- POSTGRES_DB
- POSTGRES_HOST
- POSTGRES_PORT
- REDIS_HOST
- REDIS_PORT

### For example:
```
POSTGRES_PASSWORD=FAKE_PASSWORD!
POSTGRES_USER=root
POSTGRES_DB=bar_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
```
## Setup python virtual environment

[This guide](https://dev.to/naicigam28/python-virtual-environments-pl2) can be followed to create a virtual enviroment

Once setup and activated the run the following command in the root of the directory to install dependancies.

```pip install -r requirements.txt```
## Docker compose

Docker compose is used to orcastarate 3 containers:

- Postgress instance
- Redis instance
- The REST API

In order to bring up these containers this command is used

```docker compose up```

## Database setup

Alembic is used to manage the creation and versioning of the database. Once the postgres instance is up and running and the enviroment variables were correctly set this command can be used to deploy the latest version of the Database. 

Run this command in the project root directory

```alembic upgrade head```

## Check API

Once up and running via docker compose the api should be reachable at http://localhost:8080

The API root path should automatically route the swagger docs avaible at http://localhost:8080/docs