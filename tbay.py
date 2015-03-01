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
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid", backref="item")    
    
class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    #relationships
    items = relationship("Item", backref="owner")
    bids = relationship("Bid", backref="bidder")
    
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
    
    # moe auctions a baseball
    auction = Item()
    auction.name = "baseball"
    moe.items.append(auction)
    
    # larry places bids
    bid1 = Bid(price=100, item=auction)
    larry.bids.append(bid1)
    # curly places bids
    bid2 = Bid(price=120, item=auction)
    curly.bids.append(bid2)
    
    session.add_all([larry, moe, curly, auction, bid1, bid2])
    session.commit()
    
    bids = session.query(Bid).filter(Item.id == auction.id).order_by(Bid.price).all()
    winning_bid = bids.pop()
    print "The winner is {} with a bid of {}!".format(winning_bid.bidder.name, winning_bid.price)
    
if __name__ == "__main__":
    main()