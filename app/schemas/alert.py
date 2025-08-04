from datetime import datetime
from pydantic import BaseModel, Field

# Assuming the enums from models are the source of truth
# We can re-import them or redefine them here. For simplicity, let's redefine.
# In a larger app, you might share them from a common module.

class AlertCondition(str):
    ABOVE = "ABOVE"
    BELOW = "BELOW"

class AlertStatus(str):
    ACTIVE = "ACTIVE"
    TRIGGERED = "TRIGGERED"
    DISABLED = "DISABLED"


# Shared properties
class AlertBase(BaseModel):
    base_currency: str = Field(..., min_length=3, max_length=3)
    quote_currency: str = Field(..., min_length=3, max_length=3)
    target_rate: float = Field(..., gt=0)
    condition: str # In a real app, use the Enum: AlertCondition


# Properties to receive on alert creation
class AlertCreate(AlertBase):
    pass


# Properties stored in DB
class AlertInDBBase(AlertBase):
    id: int
    user_id: int
    status: str # In a real app, use the Enum: AlertStatus
    created_at: datetime
    triggered_at: datetime | None = None

    class Config:
        orm_mode = True


# Properties to return to client
class Alert(AlertInDBBase):
    pass
