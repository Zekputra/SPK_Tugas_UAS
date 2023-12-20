from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Smartphones(Base):
    __tablename__ = 'smartphones'
    id = Column(Integer, primary_key=True)
    product = Column(String(50))
    chipset = Column(String(50)) 
    ram = Column(String(50))
    rom = Column(String(50))
    layar = Column(String(50))
    harga = Column(String(50))

    def __repr__(self):
        return f"smartphones(id={self.id!r}, brand={self.brand!r}"
