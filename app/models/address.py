from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True) 
    city_locality = Column(String, nullable=False)
    state_province = Column(String, nullable=False) 
    postal_code = Column(String, nullable=False)   
    country_code = Column(String, nullable=False)   
    is_valid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())