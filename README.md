# Final Project for CIDM6330

Pet Care Scheduling System is a system that assists a pet care provider in scheduling various customers and matching them with an available pet care service. 

## Requirements
* Install docker and python3 
* docker with docker-compose
* optional -  a local python3.8 virtualenv

## Creating a local virtualenv (optional)

```sh
python3.8 -m venv .venv && source .venv/bin/activate # or however you like to create virtualenvs

# for chapter 1
pip install pytest 

# for chapter 2
pip install pytest sqlalchemy

# for chapter 4+5
pip install -r requirements.txt

# for chapter 6+
pip install -r requirements.txt
pip install -e src/
```

## Building the containers
```sh
make build
make up
# or
make all # builds, brings containers up, runs tests
```

## Running the tests

```sh
make test
```

