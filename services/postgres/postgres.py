import os
import sys
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_info = "postgres://postgres@localhost:5432"
db = create_engine(db_info)
base = declarative_base()

class Rental(base):
    __tablename__ = 'craigslist_real_estate'

    id = Column(Integer, primary_key=True)
    location = Column(String(255))
    bedroom = Column(Integer, autoincrement=False)
    bathroom = Column(Integer, autoincrement=False)
    den = Column(Integer, autoincrement=False)
    price = Column(Integer)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)
# Create 
vancouver_rental = Rental(location="Vancouver", bedroom="2", bathroom="2", den="0", price="600000", updated_at="1000302")  
session.add(vancouver_rental)  
session.commit()

# Read
rentals = session.query(Rental)  
for rental in rentals:  
    print(rental.location)

# Update
vancouver_rental.location = "Toronto"  
session.commit()

# Delete
session.delete(vancouver_rental)  
session.commit()


# if __name__ == "__main__":
#     print ("Initiating Postgres DB connection ...")
