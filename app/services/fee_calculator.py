import datetime

def calculate_conversion_fee(base_amount: float) -> tuple[float, float]:
    """
    Calculates the conversion fee based on the day of the week.
    A higher fee is applied on weekends.

    Args:
        base_amount: The amount of the base currency to be converted.

    Returns:
        A tuple containing the fee percentage and the calculated fee amount.
    """
    # In UTC, Monday is 0 and Sunday is 6.
    # We consider Saturday (5) and Sunday (6) as the weekend.
    is_weekend = datetime.datetime.utcnow().weekday() >= 5

    if is_weekend:
        fee_percentage = 1.0  # 1.0% weekend fee
    else:
        fee_percentage = 0.5  # 0.5% weekday fee

    fee_amount = (fee_percentage / 100) * base_amount
    return fee_percentage, fee_amount
