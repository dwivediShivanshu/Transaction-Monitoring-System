from pydantic import BaseModel

class Transaction(BaseModel):
    """
    Represents a transaction record with the following fields:
    - user_id: Unique identifier for the user
    - timestamp: Date and time of the transaction
    - merchant_name: Name of the merchant where the transaction occurred
    - amount: Amount of the transaction
    """
    user_id: int
    timestamp: str
    merchant_name: str
    amount: float

class FraudDetectionResult(BaseModel):
    """
    Represents the result of fraud detection.
    """
    is_fraud: bool
    rule_stats: dict[str, int]
