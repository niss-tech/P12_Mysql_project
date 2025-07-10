from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))
    company_name = Column(String(255))
    date_created = Column(Date, nullable=False)
    last_contacted = Column(Date)
    
    sales_contact_id = Column(Integer, ForeignKey("user.id"), index=True)
    sales_contact = relationship("User", back_populates="clients")

    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")
