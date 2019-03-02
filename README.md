# helios

[![Build Status](https://travis-ci.org/PXMYH/helios.svg?branch=master)](https://travis-ci.org/PXMYH/helios)

Scrapy spider to crawl and fetch information about real estate information

This project uses pipenv for package/dependency and virtualenv management, to learn more about how to use [pipenv](https://pipenv.readthedocs.io/en/latest/)

Requirements:

## Setup workspace

```bash
brew install pipenv
pipenv --two
pipenv lock
pipenv install
```

### Setup app attached resources

Redis cluster for local dev:

```bash
brew install redis
brew services start redis
```

Postgres cluster for local dev:

```bash
brew install postgres
brew services start postgres
```

### Run the app

```bash
# run craiglist bot spider only
cd services/craigslist
scrapy crawl craigbot_all -o craigslist_result.csv

# run scheduled bot spider
cd services
python bots.py

# run app
# on root directory
export FLASK_ENV=development
FLASK_APP=app.py flask run  --debugger

# run app with bot initiated at start up
python app.py
```

### Development

```bash
# set up database
# Local Dev
psql postgres -U postgres
\c helios
# execute create_initial_schema.sql script

# To test postgres database CRUD operations
cd services/postgres
python postgres.py
```

_Note_
Commits are associated with GPG signing key
