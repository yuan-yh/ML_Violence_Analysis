# Predicting Workplace Violence in Maine Hospitals using Machine Learning and Text Mining

This project explores workplace violence reported at hospitals in Maine, aiming to identify influential factors and predict the severity of incidents using machine learning and natural language processing techniques.

Team Member: Yueheng Yuan, Muyang Cheng, Wenyi Ye

**Keywords:** healthcare, workplace violence, machine learning, NLP, BERTopic, XGBoost

## Overview

Healthcare workers face a disproportionate amount of workplace violence. To address this issue, I conducted a comprehensive analysis that combined structured and unstructured data, applied predictive modeling, and used topic modeling techniques to better understand patterns in violent incidents and inform hospital policies.

## Key Contributions

### Data Preprocessing
- Cleaned and transformed multiple datasets into a unified structure suitable for analysis.

### Exploratory Data Analysis
- Assessed basic statistics related to:
  - **Weather** and **temperature** at the time of incidents.
  - **Moon phases**, **time**, and **date** patterns.
  - **Perpetrators** and **victims** (e.g., patient-on-nurse violence).
  - **Type of violence** (e.g., verbal vs. physical).
- Identified nurses as the most frequently affected role — though partly due to their high representation in hospital staffing.
- Found that **emergency departments (ED/ER)** and **behavioral care (BC)** units experience the highest rates of violent events.

### Machine Learning Models
- Built predictive models to classify **violence severity** using:
  - **Decision Tree**
  - **Support Vector Machine (SVM)**
  - **Gaussian Naive Bayes (GaussianNB)**
- Evaluated model performance; initial best-performing model was **Decision Tree** with **69.5% accuracy**.

### Semantic Analysis & Advanced ML
- Applied **BERTopic** to extract semantic features from:
  - `Primary Assault Description`
  - `Assault Description`
- Identified meaningful topic clusters such as:
  - *Communication/cooperation/family failure*
  - *Harassment/legal accusation/fighting*
  - *Housing/homelessness/lack of support*
  - *Injurious behavior/self-harm/interference*
  - *Verbal assault/posture/aggression*

- Integrated topic features into machine learning pipeline.
- Chose **XGBoost** for its robustness with imbalanced datasets.
- Final model achieved **78% accuracy**, improving significantly over previous models.

### Key Insights
- Top contributing factors to violent events include:
  - Mental health challenges
  - Communication breakdowns
  - Housing insecurity
  - Staffing/resource limitations
- High-risk populations include:
  - Elderly or confused patients
  - Individuals with mental illness or compliance issues
- Most frequent settings for violence:
  - Emergency Rooms (ED/ER)
  - Behavioral Care (BC) units

## Policy Recommendations
Based on findings, suggested actions include:
- **De-escalation training** for frontline staff.
- **Deployment of mental health professionals** in high-risk units.
- **Improved staffing levels** and **resource allocation** to support high-pressure environments.

## 📈 Future Work
- Extend the analysis to assess **post-incident care needs**.
- Use longitudinal data to track impact of implemented policy changes.
- Explore real-time alert systems for high-risk conditions using NLP-triggered monitoring.
