from sqlalchemy.orm import Session

from app.db import models
from app.schemas import alert as alert_schema


def create_alert(db: Session, alert: alert_schema.AlertCreate, user_id: int) -> models.Alert:
    """
    Creates a new alert for a specific user.
    """
    db_alert = models.Alert(
        **alert.dict(),
        user_id=user_id,
        status='ACTIVE'  # Set default status upon creation
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alerts_by_user(db: Session, user_id: int) -> list[models.Alert]:
    """
    Retrieves all alerts associated with a specific user.
    """
    return db.query(models.Alert).filter(models.Alert.user_id == user_id).all()


def get_active_alerts(db: Session) -> list[models.Alert]:
    """
    Retrieves all alerts from the database that have an 'ACTIVE' status.
    This will be used by the background alert checker.
    """
    return db.query(models.Alert).filter(models.Alert.status == 'ACTIVE').all()


def update_alert_status(db: Session, alert_id: int, status: str) -> models.Alert:
    """
    Updates the status of a specific alert (e.g., to TRIGGERED).
    """
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if db_alert:
        db_alert.status = status
        if status == 'TRIGGERED':
            from datetime import datetime
            db_alert.triggered_at = datetime.utcnow()
        db.commit()
        db.refresh(db_alert)
    return db_alert
