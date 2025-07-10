from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False, index=True)
    support_contact_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)

    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="event")
    support_contact = relationship("User", back_populates="events")
