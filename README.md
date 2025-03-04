# Transaction Fraud Monitoring System

## Project Overview
This system analyzes transaction data to detect potentially fraudulent activities. The system processes CSV files containing transaction records with the following fields:
- User ID
- Timestamp
- Merchant Name
- Amount

## Input Requirements
- CSV file format
- Maximum 10,000 rows
- Required columns: user_id, timestamp, merchant_name, amount

## Fraud Detection Rules

### 1. Velocity Check Rule
**Rule**: Flag users with more than X transactions within Y minutes (e.g., 5+ transactions in 30 minutes)

**Why**: Legitimate users typically don't make numerous transactions in rapid succession. Fraudsters often test stolen cards with multiple small purchases in quick succession to verify card validity before making larger purchases.

### 2. Unusual Time-of-Day Activity
**Rule**: Flag transactions occurring at unusual hours compared to the user's historical pattern

**Why**: Account takeovers often happen when the legitimate user is likely asleep. If a user typically transacts between 8 AM and 10 PM but suddenly has transactions at 3 AM, this could indicate unauthorized access.

### 3. Merchant Category Anomaly Detection
**Rule**: Flag transactions with merchants in categories the user has never or rarely transacted with before

**Why**: Sudden activity with new merchant categories may indicate account compromise, especially if combined with other risk factors. Fraudsters often don't know the spending habits of the victim.

### 4. Amount Pattern Deviation
**Rule**: Flag transactions that deviate significantly from a user's typical spending amount pattern

**Why**: Unusually large transactions or a pattern of incrementally increasing transaction amounts can indicate fraud. Criminals often start with small "test" transactions before attempting larger ones.

### 5. Unusual Merchant Activity
**Rule**: Flag transactions where a user has a sudden increase in spending at a specific merchant or category compared to their historical spending patterns.

**Why**: If a user typically spends a small amount at a particular merchant but suddenly makes a large purchase, it could indicate potential fraud. Fraudsters often make larger purchases at familiar merchants to avoid detection, especially if they have compromised a legitimate user's account. For example, if a user typically spends $10 at Starbucks for a morning coffee but suddenly makes a $1000 purchase, it could indicate potential fraud.


## Usage
**Install poetry**
curl -sSL https://install.python-poetry.org | python3 -

**Verify poetry installation**
poetry --version

**Install dependencies**
poetry lock
poetry install

**Run the application**
poetry run python app/main.py



