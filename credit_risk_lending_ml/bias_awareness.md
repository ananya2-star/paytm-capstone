
# Bias Awareness and Human Oversight

## Potential Proxy Bias

The credit-risk model does not directly include protected characteristics such as gender or location. However, some of the variables used by the model could act as indirect proxies for characteristics that may be correlated with socioeconomic or demographic groups. For example, employment_type may be associated with different socioeconomic circumstances or geographic labour-market patterns. Monthly income can also reflect unequal access to employment opportunities and may correlate with location or other demographic characteristics. Similarly, credit_bureau_score can reflect differences in access to formal credit and therefore may disadvantage applicants who are new to credit or have limited credit histories.

The thin-file population requires particular attention. Applicants with missing credit bureau scores should not automatically be treated as higher-risk simply because they have less traditional credit history. The model deliberately uses UPI inflow and other alternative signals so that applicants can still be assessed when bureau information is unavailable, but this does not eliminate the possibility of indirect bias.

## Human Oversight and Governance

Before deployment, model performance should be monitored across relevant applicant segments, including thin-file status and employment type. Approval and decline rates, default rates, false-positive rates, and model performance should be reviewed periodically to identify potentially unfair outcomes.

A concrete safeguard should be introduced: **a human reviewer should double-check any thin-file applicant who receives a decline recommendation before the decision becomes final.** Borderline or unusually high-risk decisions should also be eligible for human review. Model thresholds should be reviewed periodically, and the model should not be deployed permanently without ongoing fairness, performance, and outcome monitoring.

Human oversight is therefore an important control alongside the model rather than a replacement for the model.
