import pandas as pd
from datetime import timedelta
from app.config import config

class VelocityCheckRule:
    """
    Rule 1: Flag users with too many transactions in a short time period.
    """

    def apply(self, transactions: pd.DataFrame, user_profiles: dict = None) -> int:
        """
            Args:
                transactions: pd.DataFrame
                user_profiles: dict
            Returns:
                int: Number of transactions flagged by this rule
        """
        window = timedelta(minutes=config.velocity_window_minutes)
        threshold = config.velocity_threshold_count
        flagged_count = 0
        for userId, user_data in transactions.groupby('userId'):
            user_txns = user_data.sort_values('timestamp')    
            for i, current_txn in user_txns.iterrows():
                current_time = current_txn['timestamp']
                
                window_start = current_time - window
                txns_in_window = user_txns[(user_txns['timestamp'] >= window_start) & 
                                          (user_txns['timestamp'] <= current_time)]
                count_in_window = len(txns_in_window)
                
                if count_in_window >= threshold:
                    transactions.at[i, 'is_suspicious'] = True
                    reason = f"Velocity: {count_in_window} txns in {config.velocity_window_minutes} mins"
                    if transactions.at[i, 'flag_reasons']:
                        transactions.at[i, 'flag_reasons'] += "; " + reason
                    else:
                        transactions.at[i, 'flag_reasons'] = reason
                    flagged_count += 1
        return flagged_count

class TimeAnomalyRule:
    """
    Rule 2: Flag transactions occurring at unusual hours for the user.
    """
    def apply(self, transactions: pd.DataFrame, user_profiles: dict = None) -> int:
        """
            Args:
                transactions: pd.DataFrame
                user_profiles: dict
            Returns:
                int: Number of transactions flagged by this rule
        """
        flagged_count = 0
        
        for i, txn in transactions.iterrows():
            userId = txn['userId']
            user_profile = user_profiles.get(userId)
            if not user_profile:
                continue
            
            txn_hour = txn['timestamp'].hour
            active_hours = user_profile['active_hours']
            
            if active_hours and txn_hour not in active_hours:
                is_unusual = True
                tolerance = config.time_anomaly_hour_tolerance
                
                for common_hour in active_hours.keys():
                    hour_diff = min(abs(txn_hour - common_hour), 
                                  24 - abs(txn_hour - common_hour))
                    if hour_diff <= tolerance:
                        is_unusual = False
                        break
                
                if is_unusual:
                    transactions.at[i, 'is_suspicious'] = True
                    reason = f"Time anomaly: Unusual hour {txn_hour}"
                    if transactions.at[i, 'flag_reasons']:
                        transactions.at[i, 'flag_reasons'] += "; " + reason
                    else:
                        transactions.at[i, 'flag_reasons'] = reason
                    flagged_count += 1
        
        return flagged_count

class MerchantAnomalyRule:
    """
    Rule 3: Flag transactions with merchants the user hasn't used before.
    """
    def apply(self, transactions: pd.DataFrame, user_profiles: dict = None) -> int:
        """
            Args:
                transactions: pd.DataFrame
                user_profiles: dict
            Returns:
                int: Number of transactions flagged by this rule
        """
        flagged_count = 0
        
        
        for i, txn in transactions.iterrows():
            userId = txn['userId']
            merchant = txn['merchantName']
            user_profile = user_profiles.get(userId)
            
            if not user_profile:
                continue
                
            common_merchants = user_profile['common_merchants']
            
            if merchant not in common_merchants:
                risk_score = config.merchant_anomaly_risk_threshold
                if risk_score > 0.3:
                    transactions.at[i, 'is_suspicious'] = True
                    reason = f"Merchant anomaly: New merchant {merchant}"
                    if transactions.at[i, 'flag_reasons']:
                        transactions.at[i, 'flag_reasons'] += "; " + reason
                    else:
                        transactions.at[i, 'flag_reasons'] = reason
                    flagged_count += 1
        
        return flagged_count

class AmountDeviationRule:
    """
    Rule 4: Flag transactions with amount significantly deviating from user pattern.
    """
    def apply(self, transactions: pd.DataFrame, user_profiles: dict = None) -> int:
        """
            Args:
                transactions: pd.DataFrame
                user_profiles: dict
            Returns:
                int: Number of transactions flagged by this rule
        """
        flagged_count = 0
        
        
        for i, txn in transactions.iterrows():
            userId = txn['userId']
            amount = txn['amount']
            user_profile = user_profiles.get(userId)
            
            if not user_profile:
                continue
                
            amount_mean = user_profile['amount_mean']
            amount_std = user_profile['amount_std']
            
            if amount_std > 0:
                z_score = abs(amount - amount_mean) / amount_std
                if z_score > config.amount_deviation_std_threshold:
                    transactions.at[i, 'is_suspicious'] = True
                    reason = f"Amount anomaly: ${amount} (z-score: {z_score:.2f})"
                    if transactions.at[i, 'flag_reasons']:
                        transactions.at[i, 'flag_reasons'] += "; " + reason
                    else:
                        transactions.at[i, 'flag_reasons'] = reason
                    flagged_count += 1
        
        return flagged_count