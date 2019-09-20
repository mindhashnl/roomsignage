# Mindhash

## Installation
In order to make this project run make sure that you have the follow pre-requirements installed

- Python 3.7
- Pip

Now follow those steps to get everything working

1. Install requirements `pip3 install -r requirements.txt`
1. Start the database `docker-compose up -d db`
1. Setup the database `python3 manage.py migrate`
1. Add data to database `python3 manage.py seed`
1. Run the server `python3 manage.py runserver` (or `docker-compose up web`)

## Testing
1. Run tests `pytest --cov=mysign_app`
1. Run linter `flake8`