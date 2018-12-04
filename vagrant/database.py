# Python 2.7

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# for veggieBurger in veggieBurgers:
#   print 'id: {id}\nprice: {price}\nrestaurant name: {rname}'.format(id=veggieBurger.id, price=veggieBurger.price, rname=veggieBurger.restaurant.name)

urbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()