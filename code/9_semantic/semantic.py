import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import spacy
from bertopic import BERTopic

# Load datasets
df = pd.read_csv('0_all.csv')

######################## Pre-process ########################
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    # Check if text is NaN (float) or None
    if isinstance(text, float) or text is None:
        return ""
    
    doc = nlp(text.lower().strip())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

df["Assault_Description_Clean"] = df["Assault Description"].apply(preprocess)
df["Primary_Assault_Description_Clean"] = df["Primary Assault Description"].apply(preprocess)
df["Primary_Contributing_Factors_Clean"] = df["Primary Contributing Factors"].apply(preprocess)

######################## Topic Modeling (e.g., LDA, BERTopic) ########################
# Contributing Factor
topic_model = BERTopic()
topics, _ = topic_model.fit_transform(df["Primary_Contributing_Factors_Clean"])
topic_model.get_topic_info()  # View topics

# Assault Description
# Fill NA values with empty string and combine
df["Combined_Description"] = df["Primary_Assault_Description_Clean"].fillna('') + " " + df["Assault_Description_Clean"].fillna('')
df["Combined_Description"] = df["Combined_Description"].str.strip()
# Filter out empty strings if needed
non_empty_descriptions = df[df["Combined_Description"] != ""]["Combined_Description"]
# Fit the model
topic_model = BERTopic()
topics, _ = topic_model.fit_transform(non_empty_descriptions)
topic_model.get_topic_info()