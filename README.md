# Primer App

## About
The aim of this application is to provide the backend for processing payments. In this particular
case the only processor I'm going to use is Braintree. This will be purely used as a sample
application.

### Assumptions and understanding of the problem

- This project was developed in a machine using macOS Catalina
- These instructions assume you are working on a unix based system.
- Since the API required is too small, the application will be done with Flask
- Because of `Note: for context, in order for Primer to facilitate recurring transactions across a range of processors, and to centrally capture and store payment information - tokenisation and storage of raw payment information sits with us.`, I've decided to store and manage all customer and payment information in the backend app.
- Even though at the moment the only processor used is Braintree, the current implementation will allow to incorporate other processors in the future, being able to manage multiple of them at the same time.
- To reduce scope and because there are no explicit requirements, a few things were simplified:
  - PPI data like customer information are store in the DB with the rest of the data.

### Requirements

Make sure that you have the following installed on your machine:

- Python 3.8.5 (version in `.python-version` file)
- I strongly recommend that you setup a virtual environment for this project
- Postgres is used as DB, in case you are using MacOS > 10, make sure that you have the correct openssl flags exported in your terminal, otherwise you will run into trouble with the binaries for `psycopg2`. For example:
```bash
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"
export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
```
- Docker will be running all dependencies from the project including the DB. For Mac user please read [documentation](https://docs.docker.com/docker-for-mac/)

#### Installing python

You can use your system python, but if you want to use multiple python versions on your machine, use [pyenv](https://github.com/pyenv/pyenv). If you are using it, the python version will be detected automatically inside the project's folder.

#### Installing dependencies

Like I said before, I strongly recommend using a virtual environment for this project, for this run the following:

```bash
make virtualenv
```

Activate the virtual environment
```bash
. venv/bin/activate
```

Install all the dependencies:
```bash
make install
```

If you want to exit the virtual env:
```bash
deactivate
```

#### Postgres

##### Running the DB
Like I mentioned before the DB will be running in a docker container so the application doesn't need to interact with your system. If you have postgres running locally make sure you change the port in the docker container. Here we will assume that you don't need to:

```bash
docker run --name primer_test -e POSTGRES_USER=primer -e POSTGRES_PASSWORD=primer -e POSTGRES_DB=primer_test -p 5434:5432 -d postgres:12.1
```

Also I run 2 different docker container at the same time, one for test and one for development. Make sure all your envs are point accordingly
##### Migrate

```bash
make migrate
```

For rollback:
```bash
make rollback
```

No need to migrate test, all this will be taken care for you automatically.

#### Running tests

Is really important at this point that you have a DB running so you can point the test to. The previous point gives you an example of how to do it. Now you need to set up your testing environment.

##### Setup .test.env

Modify the values accordingly
```bash
cp .sample.env .test.env
```

Once this is done and all env variables are changed to the correct values. Run:
```bash
make test
```

If you have reached this point without errors, congratulations you can start the application.


#### Running the app

For running the app:
```bash
python app.py api
```
Anything else will show you an error message.

## Missings

