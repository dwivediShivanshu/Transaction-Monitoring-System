from fastapi import APIRouter, Depends
from app.models.model import Transaction
from app.protocol import FraudDetectionService, Rule
from app.getters import get_runtime_rules, get_fraud_detection_service
from typing import List
router = APIRouter()

@router.get("/")
async def test_route():
    return "Hello World"

@router.post("/generate-report")
async def generate_report(
    fraud_detection_service: FraudDetectionService = Depends(get_fraud_detection_service),
    runtime_rules: List[Rule] = Depends(get_runtime_rules)
):

    csv_path = "./app/data/user_transactions.csv"
    output_file = "./app/data/output.csv"
    report_file = "./app/data/report.json"
    fraud_detection_service.analyze_data(csv_path, output_file, report_file)
    suspicious = fraud_detection_service.get_suspicious_transactions()
    if len(suspicious) > 0:
        print("\nSample of flagged transactions:")
        print(suspicious[['userId', 'timestamp', 'merchantName', 'amount', 'flag_reasons']].head(10))
    else:
        print("No suspicious transactions detected.")
    
    return "Report generated successfully."

@router.post("/fraud-check")
async def fraud_check(transaction: Transaction,
                       fraud_detection_service: FraudDetectionService = Depends(get_fraud_detection_service),
                       runtime_rules: List[Rule] = Depends(get_runtime_rules)):
    return fraud_detection_service.detect_fraud(transaction, runtime_rules)
