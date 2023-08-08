# PYFASTAPI

sample backend using pyfastapi, sqlalchemy, and alembic

## Preqrequisites
- python 3.11
- sqlite

## How to run
1. install dependencies `pip install -r requirements.txt`
2. copy `.env.example` to `.env` and change the values if needed
2. run the app `python main.py`
3. call the api endpoint `curl http://localhost:5000/persons`
4. open `http://localhost:5000/docs` to view then openapi docs

## Seed Data
1. run `alembic upgrade head`
2. sql schema and the data should be on `./sql_app.db`
3. refer to `alembic.ini` to change other configuration, it uses .env for the DB url

## Tests
1. make sure `alembic` is run once
2. run 'pytest'