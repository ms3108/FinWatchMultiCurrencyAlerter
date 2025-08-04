import time
import sys
import os

# This is a bit of a hack to make sure the app module is on the python path
# This is necessary because we are running this script directly, not as a module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.rate_ingestor import ingest_rates_from_api
from app.services.alert_checker import check_and_process_alerts


def rate_ingestion_job():
    """Job to ingest currency rates."""
    print("--- Running Rate Ingestion Job ---")
    db: Session = SessionLocal()
    try:
        ingest_rates_from_api(db)
    finally:
        db.close()
    print("--- Rate Ingestion Job Finished ---")


def alert_checking_job():
    """Job to check for alerts."""
    print("--- Running Alert Checking Job ---")
    db: Session = SessionLocal()
    try:
        check_and_process_alerts(db)
    finally:
        db.close()
    print("--- Alert Checking Job Finished ---")


if __name__ == "__main__":
    # In a real production app, you might use a different scheduler
    # that integrates better with your web server (e.g., BackgroundTasks in FastAPI, or Celery)
    # But for this project, a separate, blocking scheduler process is perfect.
    scheduler = BlockingScheduler()

    # Schedule the jobs
    scheduler.add_job(rate_ingestion_job, 'interval', minutes=5)
    scheduler.add_job(alert_checking_job, 'interval', minutes=1)

    print("=" * 30)
    print("🚀 Background Scheduler Started 🚀")
    print("Press Ctrl+C to exit.")
    print("=" * 30)

    # Run the jobs immediately on startup, then wait for the schedule
    rate_ingestion_job()
    alert_checking_job()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Background Scheduler Shutting Down 🛑")
        scheduler.shutdown()
        sys.exit(0)
