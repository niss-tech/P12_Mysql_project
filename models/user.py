from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from config.database import Base
import enum

class Department(enum.Enum):
    commercial = "commercial"
    gestion = "gestion"
    support = "support"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    department = Column(Enum(Department), nullable=False)

    #les relations
    clients = relationship("Client", back_populates="sales_contact")
    contracts = relationship("Contract", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")
