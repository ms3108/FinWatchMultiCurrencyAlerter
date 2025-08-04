import datetime
import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, Numeric,
                        String, UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    alerts = relationship("Alert", back_populates="owner")


class LatestRate(Base):
    __tablename__ = "latest_rates"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(3), nullable=False)
    quote_currency = Column(String(3), nullable=False)
    rate = Column(Numeric(18, 8), nullable=False)
    last_updated = Column(DateTime, nullable=False, onupdate=datetime.datetime.utcnow)

    __table_args__ = (UniqueConstraint('base_currency', 'quote_currency', name='_base_quote_uc'),)


class RateHistory(Base):
    __tablename__ = "rate_history"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(3), nullable=False)
    quote_currency = Column(String(3), nullable=False)
    rate = Column(Numeric(18, 8), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True, default=datetime.datetime.utcnow)


class AlertCondition(str, enum.Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"


class AlertStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    TRIGGERED = "TRIGGERED"
    DISABLED = "DISABLED"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    base_currency = Column(String(3), nullable=False)
    quote_currency = Column(String(3), nullable=False)
    target_rate = Column(Numeric(18, 8), nullable=False)
    condition = Column(Enum(AlertCondition), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="alerts")
