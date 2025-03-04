import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import os
import json
from app.config import config
from config import RuleConfig
from protocol import Rule
from app.models.transaction import Transaction, FraudDetectionResult

class RuleBasedFraudMonitoringService:
    """Service layer for monitoring and flagging suspicious transactions."""
    
    def __init__(self, config: Optional[RuleConfig] = None,
                        rules: Optional[List[Rule]] = None):
        """Initialize the monitoring service with configuration."""
        self.config = config or RuleConfig()
        self.user_profiles = {}
        self.transactions = None
        self.rules = rules
    

    def analyze_data(self, csv_path: str, output_file: str, report_file: str) -> None:
        """
        Analyze the data and return a boolean value indicating if the data is valid.
        Args:
            csv_path: Path to the CSV file containing transaction data
            output_file: Path to the output file containing the results
            report_file: Path to the report file containing the summary report
        """
        self.load_data(csv_path)
        self.run_all_rules()
        self.export_results(output_file)
        self.export_summary_report(report_file)
    
    def load_data(self, csv_path: str) -> bool:
        """
        Load transaction data from CSV file.
        
        Args:
            csv_path: Path to the CSV file containing transaction data
            
        Returns:
            bool: True if loading was successful, False otherwise
        """
        try:
            self.transactions = pd.read_csv(csv_path)
            required_columns = ['userId', 'timestamp', 'merchantName', 'amount']
            try:
                self.transactions['timestamp'] = pd.to_datetime(self.transactions['timestamp'])
            except Exception as e:
                self.logger.error(f"Error parsing timestamps: {e}")
                return False
            self.transactions = self.transactions.sort_values(['userId', 'timestamp'])
            self.transactions['is_suspicious'] = False
            self.transactions['flag_reasons'] = ""
            return True
            
        except Exception as e:
            return False
    
    def build_user_profiles(self) -> None:
        """Build profiles for each user based on their transaction history."""
        self.user_profiles = {}
        
        grouped = self.transactions.groupby('userId')
        
        for userId, user_txns in grouped:
            if len(user_txns) < self.config.min_user_history:
                continue
                
            active_hours = user_txns['timestamp'].dt.hour.value_counts().to_dict()
            common_merchants = {k: v for k, v in user_txns['merchantName'].value_counts().to_dict().items() if v >= 2}
            amount_mean = user_txns['amount'].mean()
            amount_std = user_txns['amount'].std() if len(user_txns) > 1 else amount_mean / 2
            merchant_wise_amount_mean = user_txns.groupby('merchantName')['amount'].mean().to_dict()
            merchant_wise_amount_std = user_txns.groupby('merchantName')['amount'].std().to_dict()
            self.user_profiles[userId] = {
                'active_hours': active_hours,
                'common_merchants': common_merchants,
                'merchant_wise_amount_mean': merchant_wise_amount_mean,
                'merchant_wise_amount_std': merchant_wise_amount_std,
                'amount_mean': amount_mean,
                'amount_std': amount_std,
                'min_amount': user_txns['amount'].min(),
                'max_amount': user_txns['amount'].max(),
                'transaction_count': len(user_txns)
            }
            
    def run_all_rules(self, rules: List[Rule] = None) -> Dict[str, int]:
        """
        Apply all fraud detection rules and return statistics.
        Args:
            rules: List[Rule]
        Returns:
            Dict[str, int]: Dictionary with rule names as keys and flagged counts as values
        """
        if self.transactions is None:
            return {}
        
        if self.rules is None:
            raise ValueError("Rules are not set")
            
        self.build_user_profiles()
        
        rule_stats = {}
        for rule in rules or self.rules:
            rule_stats[rule.__class__.__name__] = rule.apply(self.transactions, self.user_profiles)
        
        total_flagged = len(self.transactions[self.transactions['is_suspicious']])
        total_transactions = len(self.transactions)
        return rule_stats
    
    def get_suspicious_transactions(self) -> pd.DataFrame:
        """
        Return only the suspicious transactions.
        
        Returns:
            pd.DataFrame: DataFrame containing only suspicious transactions
        """
        if self.transactions is None:
            return pd.DataFrame()
            
        return self.transactions[self.transactions['is_suspicious']]
    
    def export_results(self, output_path: str) -> bool:
        """
        Export the full dataset with suspicious flags.
        
        Args:
            output_path: Path where to save the results CSV
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        if self.transactions is None:
            return False
            
        try:
            self.transactions.to_csv(output_path, index=False)
            return True
        except Exception as e:
            return False
    
    def export_summary_report(self, output_path: str) -> bool:
        """
        Export a summary report of the analysis in JSON format.
        
        Args:
            output_path: Path where to save the summary report
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        if self.transactions is None:
            return False
            
        try:
            # Get suspicious transactions
            suspicious = self.transactions[self.transactions['is_suspicious']]
            
            # Calculate statistics
            rule_counts = {}
            for reason_str in suspicious['flag_reasons'].dropna():
                reasons = reason_str.split('; ')
                for reason in reasons:
                    rule_type = reason.split(':')[0].strip()
                    rule_counts[rule_type] = rule_counts.get(rule_type, 0) + 1
            
            # User statistics
            total_users = self.transactions['userId'].nunique()
            users_with_flags = suspicious['userId'].nunique()
            
            # Prepare summary report
            summary = {
                "total_transactions": len(self.transactions),
                "suspicious_transactions": len(suspicious),
                "suspicious_percentage": (len(suspicious) / len(self.transactions)) * 100,
                "total_users": total_users,
                "users_with_flags": users_with_flags,
                "users_with_flags_percentage": (users_with_flags / total_users) * 100,
                "rule_breakdown": rule_counts,
                "config": {
                    "velocity_window_minutes": self.config.velocity_window_minutes,
                    "velocity_threshold_count": self.config.velocity_threshold_count,
                    "time_anomaly_hour_tolerance": self.config.time_anomaly_hour_tolerance,
                    "merchant_anomaly_risk_threshold": self.config.merchant_anomaly_risk_threshold,
                    "amount_deviation_std_threshold": self.config.amount_deviation_std_threshold,
                },
                "timestamp": datetime.now().isoformat()
            }
            
            with open(output_path, 'w') as f:
                json.dump(summary, f, indent=4)    
            return True
        except Exception as e:
            return False
    
    def detect_fraud(self, transaction: Transaction, rules: List[Rule]) -> FraudDetectionResult:
        """
        Detect if transaction is fraud.
        Args:
            transaction: Transaction
            rules: List[Rule]
        Returns:
            FraudDetectionResult: FraudDetectionResult
        """

        transactions: pd.DataFrame = pd.DataFrame({
            'userId': [transaction.user_id],
            'timestamp': [transaction.timestamp],
            'merchantName': [transaction.merchant_name],
            'amount': [transaction.amount]
        })

        if transaction.user_id not in self.user_profiles:
            return FraudDetectionResult(
                is_fraud=False,
                rule_stats={}
            )
        
        rule_stats: dict[str, int] = {}
        for rule in rules:
            rule_stats[rule.__class__.__name__] = rule.apply(transactions, self.user_profiles)
        
        print(rule_stats)
        return FraudDetectionResult(
            is_fraud=any(rule_stats.values()),
            rule_stats=rule_stats
        )