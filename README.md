# Meeting assistant

A small calendar application allowing to book time slots based on availability

- test the frontend at localhost:4200
- test the backend at localhost:8000/docs

# Run the app with docker

- To run the app with docker compose: `docker compose up`

# How it workds

## Tables

The app uses two tables:

- availabilities which correspond to slots where recipient is available. These
  availabilities are modifiable in the backend
- reservations which correspond to slots where somebody booked. The reservations can not
  overlap and can only be booked if the full reservation time slot is available (it can
  overlap multiple availability slots but not cross an unavailable time)

# Development

Read this section if you plan to modify the app.

## Main differences with production

- Development is done without docker while Prod uses docker
- Prod uses postgres and dev uses sqlite
- Prod uses gunicorn to launch the app while development uses uvicorn
- Prod builds the frontend and uses nginx while development serves the frontend and
  forwards calls to /api to the backend

## Installation (unix)

- Create a virtual env: `python -m venv venv`
- Activate venv: `source venv/bin/activate`
- upgrade pip: `pip install --upgrade pip`
- Install dev requirements: `pip install -r requirements-dev.txt`
- Install the requirements: `pip install -r requirements.txt`
- In the backend folder, copy the .env.example file to .env: `cp .env.example .env`
  Note: `.env` file usually contains sensitive data, which is why it is not saved to source
  control. However, there is no sensitive data in this app so `.env` is just a copy of `.env.example` without modifications
- In the frontend folder, run `npm install` to install all the packages

## Database creation

Note: for simplicity, development uses a sqlite database.

- Go back to root folder
- to create an empty db, use `aerich init-db`: it will create the sqlite database and a
  migration folder used for upgrade/downgrade. If the migration folder is already here, run `aerich upgrade`

- Then launch the script in `backend/app/database_populate_fake_data.py` to populate the db with test data

- NOTE: if you don't care about migrations, you can alternatively run the script in
  backend/app/database_schemas instead of using aerich. It will create the db without
  the aerich table and without creating the migration folder.
- NOTE2: aerich generated migration file depends on yoor choice of db, it is not exactly
  the same for sqlite and postgres for example

- IMPORTANT: Be sure to move the created database inside the `backend` folder.

## Run the app

- If you have vscode, open the cmd palette with `ctrl P` then type `task + space` and choose `Dev mode: Run App`

- Alternatively, to run the backend:

  - go to the backend folder: `cd backend`
  - run uvicorn: `uvicorn app.main:app --reload`

- Alternatively, to run the frontend:
  - go to the frontend folder: `cd frontend`
  - run uvicorn: `npm start`

## Testing

- Launch the tests by running `pytest [-vv]`
- get the coverage by running `pytest --cov="." --cov-report html`, then open `index.html` in the `htmlcov` folder
- Note: tests are only done in the backend here, not in the frontend. They ensure that
  we can not populate the db with inconsistent records while using the api. Note that you can
  still mess up the db if you enter the data directly.

# Bonus: How can machine learning help you be more organized

- Each time a reservation is deleted, track it and get as many infos regarding this
  reservation as possible (country of sender, time slot, etc)
- Each reservation that is not deleted should be tracked as well
- Train a model to predict the probability of a reservation to be cancelled based on the
  time slot. Use TPOT to choose the best model easily.
- Use this information to adjust your availabilities => if a time slot is cancelled too
  often, you may want to remove it.
