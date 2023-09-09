from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from config import *



def get_brand(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Brand).filter_by(id=id).first()

def get_all_brands():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Brand).all()

def find_brand(name):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Brand).filter_by(name=name).first()

def find_all_brands(name):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Brand).filter_by(name=name).all()


conn_str = f"mssql+pymssql://{UID_DB}:{PSWD_DB}@{SERVER}/{DATABASE}"
#conn_str = f"mssql+pymssql://user:124279123@localhost/SQLEXPRESS/Moremonta_bot"

engine = create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    is_registered = Column(Boolean, nullable=False)
    name = Column(String(150))
    phone = Column(String(12))
    street = Column(String(100))

    #user_type = relationship("TypeUser", back_populates="users")

class Brand(Base):
    __tablename__ = 'Brands'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    devices = relationship('Device', backref='brand')

class Device(Base):
    __tablename__ = 'Devices'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    brand_id = Column(Integer, ForeignKey('Brands.id'), nullable=False)
    device_type_id = Column(Integer, ForeignKey('TypeDevice.id'), nullable=False)
    master_prices = relationship('MasterPrice', backref='device')

class MasterPrice(Base):
    __tablename__ = 'MasterPrice'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('Devices.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('Services.id'), nullable=False)
    _service_name = None
    price = Column(Float(10, 0), nullable=False)
    _relevance = Column(Boolean, default=True)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    #service = relationship('Service', backref='master_prices')

class Service(Base):
    __tablename__ = 'Services'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    master_prices = relationship('MasterPrice', backref='service')

class TypeDevice(Base):
    __tablename__ = 'TypeDevice'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    devices = relationship('Device', backref='type_device')




class Order(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    master_prices_id = Column(Integer, ForeignKey('MasterPrice.id'), nullable=False)
    pickup_address = Column(String(150))
    price = Column(Float(10, 0), nullable=False)
    order_status_id = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    master_price = relationship('MasterPrice', backref='orders')
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, master_price={self.master_price.name}, price={self.price})>"
    
    @classmethod
    def get(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def getall(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find(cls, session, user_id):
        return session.query
