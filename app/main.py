from fastapi import FastAPI
from routers.routes import router
import uvicorn  
from sevices.rule_based_detection import RuleBasedFraudMonitoringService
from config import config
import pandas as pd
from getters import get_rule_based_fraud_monitoring_service
app = FastAPI()

app.include_router(router)

def main():
    import os
    transactions = pd.read_csv("./app/data/user_transactions.csv")
    print(transactions.head())

    csv_path = "./app/data//user_transactions.csv"
    output_file = "./app/data/output.csv"
    report_file = "./app/data/report.csv"

    # Rule based fraud detection
    rule_based_fraud_monitoring_service = get_rule_based_fraud_monitoring_service()
    rule_based_fraud_monitoring_service.analyze_data(csv_path, output_file, report_file)
    suspicious = rule_based_fraud_monitoring_service.get_suspicious_transactions()
    if len(suspicious) > 0:
        print("\nSample of flagged transactions:")
        print(suspicious[['userId', 'timestamp', 'merchantName', 'amount', 'flag_reasons']].head(10))
    else:
        print("No suspicious transactions detected.")

    print(rule_based_fraud_monitoring_service.user_profiles.get(1))

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()