# Part 2 — Credit Risk & Lending ML

## Objective

This project develops a credit-risk and lending analytics workflow using synthetic applicant and transaction data.

The analysis covers exploratory data analysis, thin-file applicant handling, classification modelling, risk-based pricing, transaction anomaly detection, bias awareness, and model selection.

---

## How to Run

The project was developed and tested using Google Colab.

1. Open `Part2_Credit_Risk_Lending_ML.ipynb`.
2. Run the notebook cells from top to bottom.
3. The data-generation code creates the applicant and transaction datasets.
4. The preprocessing and exploratory analysis are performed.
5. Logistic Regression and Decision Tree models are trained on the same train/test split.
6. Model performance is compared using accuracy, precision, recall, F1-score, ROC-AUC, and the ROC curve.
7. Logistic Regression probabilities are used to create risk-based pricing tiers.
8. Isolation Forest is used to detect anomalous transaction behaviour.
9. Review `bias_awareness.md` for model-risk and human-oversight considerations.

A Python script version, `part2_credit_risk_ml.py`, is also included.

---

## Files

| File | Description |
|---|---|
| `generate_data.py` | Generates the synthetic applicant and transaction datasets |
| `credit_applicants.csv` | Credit-risk applicant dataset |
| `txn_behaviour.csv` | Transaction-behaviour dataset |
| `Part2_Credit_Risk_Lending_ML.ipynb` | Complete Part 2 analysis notebook |
| `part2_credit_risk_ml.py` | Standalone Python version of the analysis |
| `roc_curve.png` | ROC curve comparing the classification models |
| `risk_based_pricing.csv` | Risk-tier pricing results including observed default rates |
| `bias_awareness.md` | Bias-awareness and human-oversight note |
| `requirements.txt` | Python packages required for the analysis |

---

## Data Generation

The applicant dataset contains 400 applicants.

The transaction-behaviour dataset contains 265 transactions, including 15 deliberately seeded anomalous transactions identified by transaction IDs beginning with `BTXNA`.

The data-generation process uses a fixed random seed so that the analysis can be reproduced.

---

## Thin-File Applicant Handling

A thin-file applicant is identified when `credit_bureau_score` is missing.

The model does not simply drop these applicants. Instead, the missing credit-bureau score is imputed using the median calculated from the training data only.

The training-derived median is then applied to both the training and test sets. This prevents information from the test set from being used during model training.

Alternative information, including UPI monthly inflow, is also retained as a useful signal for applicants with limited traditional credit history.

---

## Classification Models

Two classification models are evaluated:

1. Logistic Regression
2. Decision Tree Classifier

Both models use the same stratified train/test split and the same preprocessing approach.

The Decision Tree uses:

`DecisionTreeClassifier(random_state=42)`

Model performance is evaluated using:

- Confusion matrix
- Accuracy
- Precision
- Recall
- F1-score
- ROC curve
- ROC-AUC

---

## Why Stratification Was Used

The train/test split is stratified using the `default` target variable.

This keeps the proportion of default and non-default applicants approximately consistent between the training and test datasets. This makes the comparison between the two models more reliable, particularly because the default class is smaller than the non-default class.

---

## Why One-Hot Encoding Was Used

`employment_type` is a categorical variable with no natural numerical order.

One-hot encoding was therefore used so that categories such as salaried, self-employed, and gig are represented separately without incorrectly implying that one employment type is numerically higher or lower than another.

---

## ROC Curve

The ROC curve compares the ability of Logistic Regression and the Decision Tree to distinguish between default and non-default applicants across different classification thresholds.

ROC-AUC is used as a summary measure of model discrimination.

The resulting chart is saved as:

`roc_curve.png`

---

## Risk-Based Pricing

Logistic Regression predicted default probabilities are used to divide applicants into four risk tiers.

The pricing table contains:

- Risk tier
- Number of applicants
- Average predicted default probability
- Actual observed default rate
- Illustrative interest-rate range

The actual observed default rate is calculated from the real default outcomes in the test data rather than from the model's predicted probabilities.

The observed default rates are then checked for monotonicity. Lower-risk tiers should generally have lower observed default rates than higher-risk tiers.

The final pricing table is saved as:

`risk_based_pricing.csv`

---

## Anomaly Detection

Isolation Forest is used to identify unusual transaction behaviour.

The model uses the following standardized numerical features:

- `txn_hour`
- `is_new_device`
- `txn_amount_inr`

The contamination rate is based on the 15 seeded anomalies out of 265 total transactions.

The model's predictions are compared against the known `BTXNA` seeded anomalies, and anomaly-detection recall is reported.

---

## Bias Awareness and Human Oversight

Although gender and location are not directly included in the dataset, variables such as `employment_type`, income, and `credit_bureau_score` could potentially act as indirect proxies for characteristics such as socioeconomic circumstances or geographic patterns.

For example, employment type and income may reflect differences in access to employment opportunities, while credit-bureau scores may disadvantage applicants with limited access to formal credit.

Because of this potential proxy bias, the model should not be deployed without ongoing monitoring.

A concrete governance control is recommended: a human reviewer should double-check any thin-file applicant who receives a decline recommendation before the decision becomes final.

Further monitoring should examine model performance and approval/decline outcomes across relevant applicant segments.

See `bias_awareness.md` for the full discussion.

---

## Final Model Recommendation

The final deployment recommendation is based on the actual model-performance results produced by the analysis.

The recommendation should specifically reference the final ROC-AUC and F1 values of both models and explain why the selected model is preferable for deployment.

---

## Reproducibility

The project uses a fixed random seed for data generation and modelling.

The complete analysis can be reproduced by running:

`Part2_Credit_Risk_Lending_ML.ipynb`

from beginning to end in Google Colab.

The standalone Python script is:

`part2_credit_risk_ml.py`
