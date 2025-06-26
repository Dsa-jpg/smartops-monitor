from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    services = relationship("Service", back_populates="owner")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    status = Column(Integer, default=0)

    owner_id = Column(Integer, ForeignKey("users.id"))  
    owner = relationship("User", back_populates="services")  
    alerts = relationship("Alert", back_populates="service", cascade="all, delete-orphan")
    status_history = relationship("ServiceStatusHistory", back_populates="service", cascade="all, delete-orphan")

class ServiceStatusHistory(Base):
    __tablename__ = "service_status_history"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    status = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

    service = relationship("Service", back_populates="status_history")



class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    service_id = Column(Integer, ForeignKey("services.id",ondelete="CASCADE"), nullable=False)
    service = relationship("Service", back_populates="alerts")
