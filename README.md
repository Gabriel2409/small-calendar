# Gab meeting assistant

A small calendar application allowing to book time slots based on my availability

# Run the app with docker

- To run the app with docker compose: `docker compose up`

# Development

Read this section if you plan to modify the app

## Installation (unix)

- Create a virtual env: `python -m venv venv`
- Activate venv: `source venv/bin/activate`
- upgrade pip: `pip install --upgrade pip`
- Install dev requirements: `pip install -r requirements-dev.txt`
- Install the requirements: `pip install -r requirements.txt`
- In the backend folder, copy the .env.example file to .env: `cp .env.example .env`
  Note: `.env` file usually contains sensitive data, which is why it is not saved to source
  control. However, there is no sensitive data in this app so `.env` is just a copy of `.env.example` without modifications

## Database creation

Note: for simplicity, development uses a sqlite database.

- to create an empty db, use `aerich init-db`: it will create the sqlite database and a
  migration folder used for upgrade/downgrade. If the migration folder is already here, run `aerich upgrade`

- Then launch the script in `backend/app/database_populate_fake_data.py` to populate the db with test data

- NOTE: if you don't care about migrations, you can alternatively run the script in
  backend/app/database_schemas instead of using aerich. It will create the db without
  the aerich table and without creating the migration folder.
- NOTE2: aerich generated migration file depends on yoor choice of db, it is not exactly
  the same for sqlite and postgres for example

- Be sure to move the created database inside the `backend` folder.

## Run the app

- Run the backend:
  - go to the backend folder: `cd backend`
  - run uvicorn: `uvicorn app.main:app --reload`
  - alternatively if you have vscode: open the cmd palette with `ctrl P` then type `task + space` and choose `Dev mode: Run backend`

## Testing

- Launch the tests by running `pytest [-vv]`
- get the coverage by running `pytest --cov="." --cov-report html`, then open `index.html` in the html cov folder
