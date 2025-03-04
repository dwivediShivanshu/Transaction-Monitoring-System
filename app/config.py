
class RuleConfig:
    """Configuration parameters for transaction monitoring rules."""
    # Velocity check parameters
    velocity_window_minutes: int = 30
    velocity_threshold_count: int = 3
    
    # Time anomaly parameters
    time_anomaly_hour_tolerance: int = 3
    
    # Merchant anomaly parameters
    merchant_anomaly_risk_threshold: float = 0.5
    
    # Amount deviation parameters
    amount_deviation_std_threshold: float = 2.5
    
    # General parameters
    min_user_history: int = 3  # Minimum transactions needed for user profiling


config = RuleConfig()