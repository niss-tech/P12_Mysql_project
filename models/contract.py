from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean, Numeric
from sqlalchemy.orm import relationship
from config.database import Base

class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    sales_contact_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    date_created = Column(Date, nullable=False)
    is_signed = Column(Boolean, default=False, nullable=False)

    client = relationship("Client", back_populates="contracts")
    sales_contact = relationship("User", back_populates="contracts")
    event = relationship("Event", back_populates="contract", uselist=False)
