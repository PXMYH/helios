import os
import sys
import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db_info = "postgres://postgres@localhost:5432/helios"
DATABASE_URI = os.getenv('POSTGRES_DB_URI')
# DATABASE_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD')
db_info = DATABASE_URI
print("postgres database uri: "+str(db_info))
db = create_engine(db_info)
base = declarative_base()
# establish session
Session = sessionmaker(db)
session = Session()


class Rental_Database(base):

    __tablename__ = 'craigslist'

    id = Column(BigInteger, primary_key=True)
    location = Column(String(255))
    bedroom = Column(SmallInteger, autoincrement=False)
    bathroom = Column(SmallInteger, autoincrement=False)
    den = Column(SmallInteger, autoincrement=False)
    price = Column(Integer)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    # create all tables defined
    base.metadata.create_all(db)

    def __init__(self, location, bedroom, bathroom, den, price, updated_at):
        ''' constructor '''
        self.location = location
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.den = den
        self.price = price
        self.updated_at = updated_at


class Rental(Rental_Database):
    def __init__(self, location, bedroom, bathroom, den, price, updated_at):
        print ("Initializing rental class ...")
        self.location = location
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.den = den
        self.price = price
        self.updated_at = updated_at
        self.rental_database_record = Rental_Database(
            self.location, self.bedroom, self.bathroom, self.den, self.price, self.updated_at)

    def save_record(self):
        session.add(self.rental_database_record)
        session.commit()
        print ("Record is saved successfully")

    def save_all_records(self, record_list):
        session.add_all(record_list)
        session.commit()
        print ("Saving all records successfully!")

    def get_records(self):
        print ("Getting records ...")
        rental_records = session.query(self.__class__)
        for rental_record in rental_records:
            print(rental_record.location)

    def update_record(self, key, value):
        print(
            "Updating record attribute: {0} with new value {1}".format(key, value))
        # map key to attributes
        # TODO: this is not efficient implementation, first draft
        if key == "location":
            self.rental_database_record.location = value
            session.commit()
        elif key == "bedroom":
            self.rental_database_record.bedroom = value
        elif key == "bathroom":
            self.rental_database_record.bathroom = value
        elif key == "den":
            self.rental_database_record.den = value
        elif key == "price":
            self.rental_database_record.price = value
        else:
            print("No attribute {0} found! No update operation takes place")
            return
        session.commit()

    def delete_record(self):
        print ("Deleting record ...")
        session.delete(self.rental_database_record)
        session.commit()


# # CRUD operations
# # Create
# rental_instance = Rental("Vancouver", "2", "2", "0", "600000", "1000302")
# rental_instance.save_record()

# # bulk create
# rental_instances = [Rental("Vancouver", "2", "2", "0", "600000", "1000302"), Rental(
#     "Vancouver", "2", "2", "0", "600001", "1000303")]

# # Read
# rental_instance.get_records()

# # Update
# rental_instance.update_record("location", "Toronto")

# # Delete
# rental_instance.delete_record()
