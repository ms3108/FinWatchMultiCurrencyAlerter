from datetime import datetime
from pydantic import BaseModel, Field, condecimal

# Note: Using condecimal for precision, but float is also fine for many cases.
# The blueprint uses float, so we will stick to that for the final response models
# but use Decimal for internal calculations where possible.

# Schema for the external API response (for internal parsing)
class ExternalRate(BaseModel):
    base: str
    rates: dict[str, float]

# Schema for the request body of the conversion endpoint
class ConversionRequest(BaseModel):
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)
    amount: float = Field(..., gt=0)

# Schema for the response of the conversion endpoint
class ConversionResponse(BaseModel):
    original_amount: float
    from_currency: str
    to_currency: str
    market_rate: float
    fee_percentage: float
    fee_amount: float
    effective_rate: float
    converted_amount: float
    timestamp: datetime

# Schema for the response for a single latest rate
class LatestRateResponse(BaseModel):
    base_currency: str
    quote_currency: str
    market_rate: float
    last_updated: datetime

# Schema for a single data point in the history
class RateHistoryPoint(BaseModel):
    timestamp: datetime
    rate: float

# Schema for the historical data response
class RateHistoryResponse(BaseModel):
    pair: str
    history: list[RateHistoryPoint]
