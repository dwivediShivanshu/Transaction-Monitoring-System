from app.config import config
from app.sevices.rule_based_detection import RuleBasedFraudMonitoringService
from app.sevices.rules.rules import VelocityCheckRule, TimeAnomalyRule, MerchantAnomalyRule, AmountDeviationRule, UnusualMerchantActivityRule
from app.protocol import FraudDetectionService, Rule
from typing import List

rules = [
        VelocityCheckRule(),
        TimeAnomalyRule(),
        MerchantAnomalyRule(),
        AmountDeviationRule(),
        UnusualMerchantActivityRule()
    ]

fraud_detection_service = None

def get_fraud_detection_service() -> FraudDetectionService:
    """Get the fraud detection service."""
    global fraud_detection_service
    if fraud_detection_service is None:
        fraud_detection_service = RuleBasedFraudMonitoringService(config=config, rules=rules)
    return fraud_detection_service

def get_runtime_rules() -> List[Rule]:
    """Get the runtime rules."""
    return [
        AmountDeviationRule(),
        MerchantAnomalyRule(),
        TimeAnomalyRule(),
        UnusualMerchantActivityRule()
    ]

def get_all_rules() -> List[Rule]:
    """Get all rules."""
    return rules
