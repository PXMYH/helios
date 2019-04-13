# helios

[![Build Status](https://travis-ci.org/PXMYH/helios.svg?branch=master)](https://travis-ci.org/PXMYH/helios)

Scrapy spider to crawl and fetch information about real estate information

This project uses pipenv for package/dependency and virtualenv management, to learn more about how to use [pipenv](https://pipenv.readthedocs.io/en/latest/)

Requirements:

## Setup

### workspace

```bash
brew install pipenv
pipenv --two
pipenv lock
pipenv install
```

### Setup attached resources

Redis cluster for local dev (Celery):

```bash
brew install redis
brew services start redis
```

Postgres cluster for local dev (Backend database):

```bash
brew install postgres
brew services start postgres
```

## Run app

run the following command from root directory

### run craiglist bot spider only

```bash
cd services/craigslist
scrapy crawl craigbot_all -o craigslist_result.csv
```

### run scheduled bot spider

```bash
cd services
export POSTGRES_DB_URI="postgres://postgres@localhost:5432/helios"; python bots.py
```

### run app with bot manual trigger

```bash
export FLASK_ENV=development
export POSTGRES_DB_URI="postgres://postgres@localhost:5432/helios"
FLASK_APP=app.py flask run --debugger
# to trigger the bot, run
curl http://localhost:5000
```

### run app with bot autostart

```bash
export POSTGRES_DB_URI="postgres://postgres@localhost:5432/helios"
python app.py

```

## Development

### Database

#### local development

```bash
# connect to database
psql postgres -U postgres
\c helios
# execute create_initial_schema.sql script

# To test postgres database CRUD operations
cd services/postgres
export POSTGRES_DB_URI="postgres://postgres@localhost:5432/helios"
python postgres.py
```

## Deployment

helios system is set up to be in continous deployment to Heroku platform at https://dashboard.heroku.com/apps/beast-helios tracking `master` branch

```bash
# deploy to Heroku, just check in/ merge into master branch

# restart app
heroku restart

# set/unset environment variables
heroku config:set <env_var>
heroku config:unset <env_var>

# check logs
heroku logs --tail
```

_Note_
Commits are associated with GPG signing key
