# Gab meeting assistant

A small calendar application allowing to book time slots based on my availability

# Development

Read this section if you plan to modify the app

## Installation (unix)

- Create a virtual env: `python -m venv venv`
- Activate venv: `source venv/bin/activate`
- upgrade pip: `pip install --upgrade pip`
- Install dev requirements: `pip install -r requirements-dev.txt`
- Install the requirements: `pip install -r requirements.txt`

## Run the app

- Run the backend:
  - go to the backend folder: `cd backend`
  - run uvicorn: `uvicorn app.main:app --reload`
  - alternatively if you have vscode: open the cmd palette with `ctrl P` then type `task + space` and choose `Dev mode: Run backend`

## Testing

- Launch the tests by running `pytest [-vv]`
- get the coverage by running `pytest --cov="." --cov-report html`, then open `index.html` in the html cov folder
