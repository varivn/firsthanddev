import os
from sqlalchemy import Column, String, Integer, create_engine, ARRAY, ForeignKey, PickleType
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from dotenv import load_dotenv
from sqlalchemy.sql.expression import null

db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_ADMIN')
db_pass = os.getenv('DB_PASSWORD')

database_path = "postgresql://{}:{}@{}/{}".format(db_user, db_pass, db_host, db_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)

'''
Producers Model
'''
class Producer(db.Model):
    __tablename__ = 'producers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    products = Column(ARRAY(String), nullable=True)
    producer_sales = db.relationship('Sale', backref='producers', lazy='joined', cascade='all, delete')

    def __init__(self, name, country, products):
        self.name = name
        self.country = country
        self.products = products
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id':self.id,
            'name':self.name,
            'country':self.country,
            'products':self.products
        }

'''
Buyers Model
'''
class Buyer(db.Model):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comercialized_products = Column(ARRAY(String), nullable=True)
    buyer_sales = db.relationship('Sale', backref='buyers', lazy='joined', cascade='all, delete')

    def __init__(self, name, comercialized_products):
        self.name = name
        self.comercialized_products = comercialized_products        

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name':self.name,
            'comercialized_products':self.comercialized_products
        }
'''
Sales Model
'''
class Sale(db.Model):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    producer_id = Column(Integer, ForeignKey('producers.id'), nullable=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=True)
    # sale_detail = Column(PickleType, nullable=True)

    def __init__(self, producer_id, buyer_id):
        self.producer_id = producer_id
        self.buyer_id = buyer_id
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def format(self):
        return {
            'id':self.id,
            'producer_id':self.producer_id,
            'buyer_id':self.buyer_id
        }

