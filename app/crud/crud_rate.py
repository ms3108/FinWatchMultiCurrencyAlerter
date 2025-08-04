from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db import models


def get_latest_rate(db: Session, base_currency: str, quote_currency: str) -> models.LatestRate | None:
    """
    Retrieves the most recent exchange rate for a given currency pair.
    """
    return db.query(models.LatestRate).filter(
        models.LatestRate.base_currency == base_currency,
        models.LatestRate.quote_currency == quote_currency
    ).first()


def get_rate_history(db: Session, base_currency: str, quote_currency: str, days: int) -> list[models.RateHistory]:
    """
    Retrieves the historical exchange rates for a pair for a given number of days.
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    return db.query(models.RateHistory).filter(
        models.RateHistory.base_currency == base_currency,
        models.RateHistory.quote_currency == quote_currency,
        models.RateHistory.timestamp >= start_date
    ).order_by(models.RateHistory.timestamp.desc()).all()


def upsert_latest_rate(db: Session, base_currency: str, quote_currency: str, rate: float):
    """
    Inserts a new latest rate or updates it if the currency pair already exists.
    This is an 'upsert' operation.
    """
    stmt = insert(models.LatestRate).values(
        base_currency=base_currency,
        quote_currency=quote_currency,
        rate=rate,
        last_updated=datetime.utcnow()
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['base_currency', 'quote_currency'],
        set_=dict(rate=rate, last_updated=datetime.utcnow())
    )
    db.execute(stmt)
    db.commit()


def create_rate_history(db: Session, base_currency: str, quote_currency: str, rate: float):
    """
    Creates a new entry in the rate history table.
    """
    db_rate_history = models.RateHistory(
        base_currency=base_currency,
        quote_currency=quote_currency,
        rate=rate,
        timestamp=datetime.utcnow()
    )
    db.add(db_rate_history)
    db.commit()
    db.refresh(db_rate_history)
    return db_rate_history
