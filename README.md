# Paytm FinTech Analytics & AI Platform

## Project Structure

This project contains three connected parts:

* `payments_fraud_analytics`
* `credit_risk_lending_ml`
* `ai_advisory_blockchain`

## Part 1 — Payments & Fraud Analytics

### Setup

Install the required Python libraries using:

```bash
pip install pandas numpy matplotlib openpyxl
```

Alternatively, install the dependencies using the `requirements.txt` file inside the Part 1 folder.

### How to Run

1. Open the `payments_fraud_analytics` folder.
2. Run the seed-data generator:

```bash
python generate_data.py
```

3. This generates:

* `merchants.csv`
* `users.csv`
* `ledger.csv`
* `gateway_export.csv`

4. Open `merchant_workbook.xlsx` to review the spreadsheet analysis.

5. Run `Part1_Payments_Fraud_Analytics.ipynb`.

The notebook:

* creates `paytm_payments.db`
* loads the merchant, user, and transaction data
* runs all 9 SQL queries
* performs payment reconciliation
* calculates dashboard metrics
* generates the required dashboard charts and merchant-detail table

### Design Decisions

#### MDR Fee Assumptions

The HLOOKUP demonstration in the merchant workbook uses the following illustrative MDR-style fee assumptions:

* UPI: 0.02%
* Wallet: 0.05%
* Card: 1.5%
* Netbanking: 1%

These values are illustrative assumptions used only for the spreadsheet demonstration.

#### High-Value Merchant Day Rule

A transaction is classified as a **High-Value Merchant Day** when:

* the merchant's total transaction amount for that day exceeds INR 5,000, and
* the merchant's region is not East.

The classification is implemented using a nested `IF` and `AND` formula in the merchant workbook.

#### Dashboard Chart Choices

The headline layer uses scorecards to summarize total GMV, transaction success rate, reconciliation match rate, and chargeback ratio.

The trends layer uses a time-series chart to show daily GMV and daily chargeback activity over the 30-day period.

The breakdown layer uses bar charts to compare GMV across payment methods and merchant categories.

The details layer presents the top 10 merchants by transaction count and flags merchants whose chargeback ratio exceeds 1% for closer fraud monitoring.
