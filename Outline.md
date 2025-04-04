## **Machine Learning Analysis Outline for Hospital Violence in Maine**
**Objective**: Analyze the hospital violence dataset to identify patterns, risk factors, and potential predictive models for violence in healthcare facility.

### **Step 1: Pre-Processing**
#### **1.1 Data Segmentation**
- Group facilities into:  
  - Unknown Hospital #1 (WVP Data Collection - Phase 1), Unknown Hospital #2 (Workplace Violence Data Collection Tool January to October 2024) 
  - Northern Light Health
  - Unified MHA (Maine Hospital Association)

#### **1.2 Data Cleaning**
- Check for missing / null values (may keep if one column has too many 'N/A' fields)

### **1.3 Feature Engineering**
- **Temporal Features**:
- Extract `Day of Week` and `Month` from the `Event Date` field
- **Categorical Encoding**:
- Convert categorical variables into numerical representations (e.g.,`Severity`, `Facility Type`, `Occupational Category`)
- **Text Fields** (if time available):
- Clean `Primary Assault Description` (remove stopwords, lemmatize).
- Use TF-IDF for keyword extraction (e.g., "weapon", "threat").

### **Step 2: Exploratory Data Analysis (EDA)**
- baisc statistics and visulization (like piechart of `Type of Violence` in different hospical facilitates and histograms of accidents reported on date)
#### **2.1 Descriptive Statistics**
- **Basic Statistics**:
- `df.describe()` for numerical features (e.g., `Severity`).
- `df.value_counts()` for categorical (e.g., `Type of Violence`).
- **Basic Visualization**:
- Pie charts: % of `Type of Violence` per facility group.
- Histograms: Incident frequency by month/day.

#### **2.2 Univariate Analysis**
- **Key Plots**:
- Bar plots: Top 5 `Occupational Categories` affected.
- Box plots: `Severity` distribution by `Facility Type`.

#### **2.3 Multivariate Analysis**
- **Cross-Tabulation**:
- `Occupational Category` vs `Type of Violence` (normalize for %).
- **Correlation**:
- Heatmap of `Severity` vs. `Emotional Impact`.
- **Correlation Matrix**
- Visualize the correlation matrix to identify relationships between features

#### **2.4 EDA Insights**
- Is there a seasonal trend (e.g., higher assaults at *full moon*)?
- Are nurses in a specific unit more likely to experience physical violence?


### **Step 3: Machine Learning**
- **Classification**: Predict `Severity` (Low/Medium/High) or `Emotional Impact` (Binary: High/Low).
- Train-test split (80-20).
- **Classification Models**
- Logistic Regression
- Decision Trees
- Random Forest
- XGBoost (will consider if imbalanced data, will determine after data cleaning).

### **Step 4: Metric Evaluation**
- Classification: Accuracy, Precision, Recall, F1-score, AUC-ROC.

### **Step 5: Future Improvement**
1. Clustering (if time available)
- Group incidents by `Type of Violence` + `Contributing Factors`.
- **Clustering Models** (if finding hidden patterns in the dataset):
- Elbow Method
- K-Means
- Hierarchical Clustering
- **Clustering Metrics**:
- Profile clusters (e.g., "Cluster 1: Verbal abuse by patients in ED").

2. Tuning (if time available)

3. check canvas link

4. Text Processing (if time available)
- NLP techniques on `Primary Assault Description` to auto-tag incidents (e.g., TF-IDF, sentiment analysis)

5. Insights:
- Predict high-risk hospital environments and vulnerable occupational categories.
- Recommend preventive strategies based on identified risk factors.
- Suggest resource allocation improvements for better response actions.

### Reference: 
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10246850/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8962616/
- https://edition.pagesuite.com/popovers/dynamic_article_popover.aspx?artguid=621e2c49-cc12-4c9d-ae5a-256f585eb81e&appcode=BOSGLO&eguid=a36d36f8-c987-4b93-81a1-d378a73f20d7&pnum=106#