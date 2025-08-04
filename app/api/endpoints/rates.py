from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_rate
from app.schemas import rate as rate_schema
from app.services.fee_calculator import calculate_conversion_fee

router = APIRouter()


@router.get("/rates", response_model=rate_schema.LatestRateResponse)
def get_latest_fx_rate(
    base: str = Query(..., min_length=3, max_length=3, description="Base currency code (e.g., USD)"),
    quote: str = Query(..., min_length=3, max_length=3, description="Quote currency code (e.g., EUR)"),
    db: Session = Depends(deps.get_db)
):
    """
    Get the latest exchange rate for a given currency pair.
    """
    rate = crud_rate.get_latest_rate(db, base_currency=base.upper(), quote_currency=quote.upper())
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found for this currency pair.")

    return rate_schema.LatestRateResponse(
        base_currency=rate.base_currency,
        quote_currency=rate.quote_currency,
        market_rate=float(rate.rate),
        last_updated=rate.last_updated
    )


@router.post("/convert", response_model=rate_schema.ConversionResponse)
def perform_conversion(
    request: rate_schema.ConversionRequest,
    db: Session = Depends(deps.get_db)
):
    """
    Perform a currency conversion, including a simulated fee.
    """
    from_currency = request.from_currency.upper()
    to_currency = request.to_currency.upper()

    rate = crud_rate.get_latest_rate(db, base_currency=from_currency, quote_currency=to_currency)
    if not rate:
        # Try inverse rate
        inverse_rate = crud_rate.get_latest_rate(db, base_currency=to_currency, quote_currency=from_currency)
        if not inverse_rate:
            raise HTTPException(status_code=404, detail="Rate not found for conversion for this currency pair.")
        market_rate = 1 / float(inverse_rate.rate)
    else:
        market_rate = float(rate.rate)

    fee_percentage, fee_amount = calculate_conversion_fee(request.amount)

    # As per blueprint: fee is calculated for display, but effective rate is used for conversion
    effective_rate = market_rate * (1 - fee_percentage / 100)
    converted_amount = request.amount * effective_rate

    return {
        "original_amount": request.amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "market_rate": market_rate,
        "fee_percentage": fee_percentage,
        "fee_amount": fee_amount,
        "effective_rate": effective_rate,
        "converted_amount": converted_amount,
        "timestamp": datetime.utcnow()
    }


@router.get("/rates/history", response_model=rate_schema.RateHistoryResponse)
def get_fx_rate_history(
    pair: str = Query(..., description="Currency pair in 'BASE-QUOTE' format (e.g., USD-EUR)"),
    days: int = Query(30, gt=0, le=365, description="Number of days for historical data"),
    db: Session = Depends(deps.get_db)
):
    """
    Get historical exchange rate data for a currency pair.
    """
    try:
        base, quote = pair.upper().split('-')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid pair format. Use 'BASE-QUOTE', e.g., 'USD-EUR'.")

    history_data = crud_rate.get_rate_history(db, base_currency=base, quote_currency=quote, days=days)

    if not history_data:
        raise HTTPException(status_code=404, detail="No historical data found for this pair in the given timeframe.")

    return {
        "pair": pair.upper(),
        "history": [
            {"timestamp": h.timestamp, "rate": float(h.rate)} for h in history_data
        ]
    }
