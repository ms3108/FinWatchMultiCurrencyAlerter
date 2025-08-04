from sqlalchemy.orm import Session
from datetime import datetime

from app.crud import crud_alert, crud_rate
from app.services.notification import send_trigger_email
from app.db.models import AlertCondition


def check_and_process_alerts(db: Session):
    """
    Checks all active alerts against the latest rates and triggers notifications.
    This function is intended to be called by a background scheduler.
    """
    print(f"[{datetime.utcnow()}] INFO: Starting alert processing job.")

    active_alerts = crud_alert.get_active_alerts(db)
    if not active_alerts:
        print(f"[{datetime.utcnow()}] INFO: No active alerts to process.")
        return

    triggered_count = 0
    for alert in active_alerts:
        try:
            # Fetch the latest rate for the alert's currency pair
            latest_rate = crud_rate.get_latest_rate(db, alert.base_currency, alert.quote_currency)

            if not latest_rate:
                # If no direct rate, try finding the inverse rate
                inverse_rate = crud_rate.get_latest_rate(db, alert.quote_currency, alert.base_currency)
                if inverse_rate:
                    current_market_rate = 1 / float(inverse_rate.rate)
                else:
                    # Skip this alert if no rate data is available
                    print(f"[{datetime.utcnow()}] WARNING: No rate found for {alert.base_currency}/{alert.quote_currency}. Skipping alert ID {alert.id}.")
                    continue
            else:
                current_market_rate = float(latest_rate.rate)

            target_rate = float(alert.target_rate)
            should_trigger = False

            # Check if the condition is met
            if alert.condition == AlertCondition.ABOVE and current_market_rate > target_rate:
                should_trigger = True
            elif alert.condition == AlertCondition.BELOW and current_market_rate < target_rate:
                should_trigger = True

            if should_trigger:
                print(f"[{datetime.utcnow()}] INFO: Triggering alert ID {alert.id} for user {alert.owner.email}.")

                # 1. Update the alert status in the database
                crud_alert.update_alert_status(db, alert_id=alert.id, status='TRIGGERED')

                # 2. Send the notification email (simulated)
                # We need to convert the SQLAlchemy model to a dict for the function
                alert_dict = {
                    "base_currency": alert.base_currency,
                    "quote_currency": alert.quote_currency,
                    "condition": alert.condition.value,
                    "target_rate": target_rate
                }
                send_trigger_email(
                    user_email=alert.owner.email,
                    alert=alert_dict,
                    current_rate=current_market_rate
                )
                triggered_count += 1

        except Exception as e:
            print(f"[{datetime.utcnow()}] ERROR: Failed to process alert ID {alert.id}. Reason: {e}")

    print(f"[{datetime.utcnow()}] INFO: Alert processing job finished. Triggered {triggered_count} alerts.")
