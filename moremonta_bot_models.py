from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from pyodbc import *

# Устанавливаем соединение с базой данных
connection_string = 'DRIVER={SQL Server};SERVER=TIMUR-HOME\SQLEXPRESS;DATABASE=Moremonta_bot;Trusted_Connection=yes;'
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")


# Создаем подключение к базе данных
#engine = create_engine(f'mssql+pyodbc://{UID_DB}:{PSWD_DB}@{SERVER}/{DATABASE}')

# Создаем базовую модель
Base = declarative_base()

# Определяем модели для каждой таблицы
class Brand(Base):
    __tablename__ = 'Brands'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime) 
    updated_at = Column(DateTime)

    # Определяем связь с таблицей Devices
    devices = relationship('Device', backref=backref('brand'))

class Device(Base):
    __tablename__ = 'Devices'
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey('Brands.id'))
    name = Column(String(100), nullable=False)
    picture = Column(String(2048))
    deleted_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class TypeUser(Base):
    __tablename__ = 'TypeUser'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Определяем связь с таблицей Users
    users = relationship('User', backref=backref('type_user'))

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer, ForeignKey('TypeUser.id'))
    telegram_id = Column(Integer, nullable=False)
    is_registered = Column(Boolean, nullable=False)
    name = Column(String(150))
    phone = Column(String(50))
    street = Column(String(100))

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)



from sqlalchemy.orm import sessionmaker
if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    brands = session.query(Base.Brands).all()
    for brand in brands:
        print(brand.name)




