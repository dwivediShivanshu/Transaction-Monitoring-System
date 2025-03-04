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

### 5. Geographically Impossible Transactions
**Rule**: Flag transactions with the same user ID occurring in different physical locations within a timeframe that makes travel between them impossible

**Why**: If the transaction data includes or can be linked to location information, this rule can detect when the same card is used in geographically distant locations within an unreasonably short timeframe (e.g., transactions in New York and Los Angeles within 3 hours).

## Usage
[Add usage instructions here]

## Installation
[Add installation instructions here]
