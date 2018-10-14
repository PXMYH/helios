# helios

Scrapy spider to crawl and fetch information about real estate information

This project uses pipenv for package/dependency and virtualenv management, to learn more about how to use [pipenv](https://pipenv.readthedocs.io/en/latest/)

Requirements:

* Cassandra cluster set up

  ```bash
  docker pull cassandra
  docker run --name helios_db -d cassandra:latest
  ```

* Cassandra driver installed

  `pipenv install cassandra-driver`

  - if you don't want to have Cython-based extensions then disable through flag
  `pip install cassandra-driver --no-cython`
