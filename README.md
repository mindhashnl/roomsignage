# Room Signage

Master branch:
[![Build status](https://badge.buildkite.com/a6ccf7b9f3b6afcdf78f28452b51e4e704d50ed30248c57be8.svg?branch=master)](https://buildkite.com/mysign/mysign)

Develop branch:
[![Build status](https://badge.buildkite.com/a6ccf7b9f3b6afcdf78f28452b51e4e704d50ed30248c57be8.svg?branch=development)](https://buildkite.com/mysign/mysign)

## Installation
In order to make this project run make sure that you have the follow pre-requirements installed

- Python 3.7
- Pip
- Docker (or docker desktop for windows)
- docker-compose (already installed with docker desktop)

Now follow those steps to get everything working

1. Install requirements `pip3 install -r requirements.txt`
1. Start the database `cp .env.example .env`
1. Start the database `docker-compose up -d db`
1. Setup the database `python3 manage.py migrate`
1. Add data to database `python3 manage.py seed`
1. Run the server `python3 manage.py runserver` (or `docker-compose up web`)

## Testing
1. Run tests `pytest`
1. Run linter `flake8 .`
1. Run JS linter `eslint mysign_app`
1. Run HTML linter `jinjalint`

If you get import order errors run `isort`.
If you get JS linter errors run `eslint mysign_app --fix`

## License
This software is freely distributable under the terms of the
[MIT license](https://github.com/mindhashnl/roomsignage/blob/master/LICENSE).
