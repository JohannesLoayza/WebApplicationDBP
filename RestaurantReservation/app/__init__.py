from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/projectdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5444/dockerdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@0.0.0.0:3306/mysqldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import views, models