from fastapi import APIRouter, Depends
from app.models.transaction import Transaction
from app.protocol import FraudDetectionService, Rule
from app.getters import get_fraud_detection_service, get_runtime_rules
from typing import List
router = APIRouter()

@router.get("/")
async def test_route():
    return "Hello World"

@router.post("/detect-fraud")
async def detect_fraud(transaction: Transaction,
                       fraud_detection_service: FraudDetectionService = Depends(get_fraud_detection_service),
                       runtime_rules: List[Rule] = Depends(get_runtime_rules)):
    return fraud_detection_service.detect_fraud(transaction, runtime_rules)
