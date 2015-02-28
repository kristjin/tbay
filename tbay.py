from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
        
    #relationships
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid", uselist=False, backref="item")    
    
class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    #relationships
    items = relationship("Item", uselist=False, backref="owner")
    bids = relationship("Bid", uselist=False, backref="bidder")
    
class Bid(Base):
    __tablename__="bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    #relationships
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    



def main():
    Base.metadata.create_all(engine)
    
    larry = User(name="larry", password="curlyisgay")
    moe = User(name="moe", password="seenoevil")
    curly = User(name="curly", password="larryiscute")
    
    session.add_all([larry, moe, curly])
    # session.commit()
        
    # moe auctions a baseball
    auction = Item()
    auction.name = "baseball"
    auction.owner_id = moe.id
    session.add(auction)
    session.commit()
    # larry places bids
    
    # curly places bids
    
    

if __name__ == "__main__":
    main()