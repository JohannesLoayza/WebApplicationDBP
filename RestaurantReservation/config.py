
import os

WTF_CSRF_ENABLED = False
SECRET_KEY = 'myrestaurantreservation'

#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5444/restaurantreservation'
#SQLALCHEMY_DATABASE_URI = 'postgresql:///restaurantreservation'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5444/dockerdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@0.0.0.0:3306/mysqldb'
SQLALCHEMY_TRACK_MODIFICATIONS = False