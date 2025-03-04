from app.config import config
from app.sevices.rule_based_detection import RuleBasedFraudMonitoringService
from app.sevices.rules.rules import VelocityCheckRule, TimeAnomalyRule, MerchantAnomalyRule, AmountDeviationRule
from app.protocol import FraudDetectionService, Rule
from typing import List

rules = [
        VelocityCheckRule(),
        TimeAnomalyRule(),
        MerchantAnomalyRule(),
        AmountDeviationRule()
    ]

def get_rule_based_fraud_monitoring_service() -> RuleBasedFraudMonitoringService:
    """Get the rule based fraud monitoring service."""
    return RuleBasedFraudMonitoringService(config=config, rules=rules)


def get_fraud_detection_service() -> FraudDetectionService:
    """Get the fraud detection service."""
    return RuleBasedFraudMonitoringService(config=config, rules=rules)

def get_runtime_rules() -> List[Rule]:
    """Get the runtime rules."""
    return [
        AmountDeviationRule(),
        MerchantAnomalyRule(),
        TimeAnomalyRule()
    ]
