import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

# 1. Load the dataset
df = pd.read_csv("8_9.4_all_number_except_semantic.csv")

# 2. Drop unused columns
drop_cols = ['care', 'role', 'factor', 'description']
df = df.drop(columns=drop_cols, errors='ignore')

# 3. Define feature columns and target column 
feature_cols = ['aggressor', 'violence type', 'location', 'general location', 'emotion']
target_col = 'severity'

# 4. Drop rows with missing target
df_model = df.dropna(subset=[target_col])

# 5. Fill missing values in features with the median 
df_model.loc[:, feature_cols] = df_model[feature_cols].fillna(df_model[feature_cols].median())

# 6. Split into features and target 
X = df_model[feature_cols]
y = df_model[target_col]

# 7. Normalize the features 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 8. Split into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)

# 9. Define machine learning models 
models = {
    'Decision Tree': DecisionTreeClassifier(),
    'SVM': SVC(),
    'GaussianNB': GaussianNB()
}

# 10. Train and evaluate each model 
metrics_summary = {
    'Model': [],
    'Accuracy': [],
    'F1-score': [],
    'Precision': []
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    metrics_summary['Model'].append(name)
    metrics_summary['Accuracy'].append(accuracy_score(y_test, y_pred))
    metrics_summary['F1-score'].append(report['weighted avg']['f1-score'])
    metrics_summary['Precision'].append(report['weighted avg']['precision'])

# 11. Plot the performance comparison
df_metrics = pd.DataFrame(metrics_summary)
df_metrics.set_index('Model', inplace=True)

df_metrics.plot(kind='bar', figsize=(10, 6))
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()
