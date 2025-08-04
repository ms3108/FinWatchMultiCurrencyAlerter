import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import crud_rate


def ingest_rates_from_api(db: Session):
    """
    Fetches latest rates from the external API and updates the database.
    This function is intended to be called by a background scheduler.
    """
    api_key = settings.EXCHANGE_RATE_API_KEY
    base_currency = settings.DEFAULT_BASE_CURRENCY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"

    print(f"[{datetime.utcnow()}] INFO: Starting rate ingestion for base currency: {base_currency}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.utcnow()}] ERROR: Could not fetch data from external API. Reason: {e}")
        return

    data = response.json()

    if data.get("result") != "success":
        error_type = data.get("error-type", "unknown_error")
        print(f"[{datetime.utcnow()}] ERROR: External API returned an error: {error_type}")
        return

    rates = data.get("conversion_rates", {})
    if not rates:
        print(f"[{datetime.utcnow()}] WARNING: No conversion rates found in API response.")
        return

    processed_count = 0
    for quote_currency, rate in rates.items():
        try:
            # 1. Update the latest_rates table (UPSERT)
            crud_rate.upsert_latest_rate(
                db,
                base_currency=base_currency,
                quote_currency=quote_currency,
                rate=float(rate)
            )
            # 2. Add an entry to the rate_history table (INSERT)
            crud_rate.create_rate_history(
                db,
                base_currency=base_currency,
                quote_currency=quote_currency,
                rate=float(rate)
            )
            processed_count += 1
        except Exception as e:
            # Catching broad exception to ensure the loop continues
            print(f"[{datetime.utcnow()}] ERROR: Failed to process rate for {quote_currency}. Reason: {e}")

    print(f"[{datetime.utcnow()}] INFO: Rate ingestion complete. Processed {processed_count} currency pairs.")

# This import is needed to avoid a circular dependency if we run this file directly
# and to make the print statements work correctly.
from datetime import datetime
