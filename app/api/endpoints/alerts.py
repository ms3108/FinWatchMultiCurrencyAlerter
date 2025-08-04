from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db import models
from app.crud import crud_alert, crud_rate
from app.schemas import alert as alert_schema

router = APIRouter()


@router.post("/alerts", response_model=alert_schema.Alert, status_code=status.HTTP_201_CREATED)
def create_new_alert(
    alert_in: alert_schema.AlertCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create a new price alert. The system will monitor the rate for the
    specified currency pair and notify the user when the condition is met.
    """
    base_currency = alert_in.base_currency.upper()
    quote_currency = alert_in.quote_currency.upper()

    # Optional: Check if we have data for this currency pair before creating an alert
    rate = crud_rate.get_latest_rate(db, base_currency, quote_currency)
    if not rate:
        # Also check the inverse
        inverse_rate = crud_rate.get_latest_rate(db, quote_currency, base_currency)
        if not inverse_rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No exchange rate data found for {base_currency}/{quote_currency}. Cannot create alert."
            )

    alert = crud_alert.create_alert(db=db, alert=alert_in, user_id=current_user.id)
    return alert


@router.get("/alerts", response_model=list[alert_schema.Alert])
def get_user_alerts(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Retrieve all alerts created by the current user.
    """
    alerts = crud_alert.get_alerts_by_user(db=db, user_id=current_user.id)
    return alerts
