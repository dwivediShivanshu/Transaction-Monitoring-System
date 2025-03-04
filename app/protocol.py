from typing import Protocol, List
import pandas as pd
from app.models.model import Transaction, FraudDetectionResult

class Rule(Protocol):
    def apply(self, transactions: pd.DataFrame, user_profile: dict = None) -> int:
        pass

class FraudDetectionService(Protocol):
    def detect_fraud(self, transaction: Transaction, rules: List[Rule]) -> FraudDetectionResult:
        pass
