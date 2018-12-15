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

## Setup workspace

```bash
pipenv --two
pipeenv lock
```

### Setup Cassandra Cluster

for local dev:

```bash
# assume the following command is run from root directory and cluster nodes are within the same VM
docker swarm init

docker config create cassandra.yaml ./res/cassandra.yaml
docker service create --replicas 3 --name cassandra_cluster -d cassandra:3.11.3-mh

# to check running service
docker service ps cassandra

# to inspect service
docker service inspect --pretty cassandra
```

### Run the crawler

```bash
scrapy crawl craigbot -o craigslist_result.csv
```

[Note]
Commits are associated with GPG signing key

### Run the app

```bash
# on the root directory
export FLASK_ENV=development
flash run
```
