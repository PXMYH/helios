#!/usr/bin/env python

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

class Cassandra():

    def __init__(self):
        self.cluster = Cluster(['127.0.0.1'],
                          load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='US_EAST'),
                           port=9042)
        self.session = self.cluster.connect()

    def create_keyspace(self, keyspace_name):
        print ("[INFO] creating keyspace: {}".format(keyspace_name))
        self.session.set_keyspace(keyspace_name)

    def create_query(self):
        query = SimpleStatement(
    "INSERT INTO users (name, age) VALUES (%s, %s)",
    consistency_level=ConsistencyLevel.QUORUM)
        self.session.execute(query)

    def write(self, db):
        pass

    def read(self):
        pass

    def info(self):
        print ("Cassandra cluster debug information:")
        



if __name__ == "__main__":
    cassandra_instance = Cassandra()
    print ("initiating Canssadra DB connection and information dump")
