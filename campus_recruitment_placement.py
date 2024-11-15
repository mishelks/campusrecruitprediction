# -*- coding: utf-8 -*-
"""Campus_recruitment_placement.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19achP9P0b5CmhQBbDHoQ_t0NW_FBSjGS

CAMPUS RECRUITMENT PREDICTION

IMPORTING LIBRARIES
"""

# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("/content/train.csv")

# Display basic dataset information
print("Dataset Info:")
print(df.info())
print("\nDataset Description:")
print(df.describe())
print("\nFirst Few Rows:")
print(df.head())

"""Data Preprocessing"""

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Visualize distributions of numerical features
df.hist(figsize=(12, 10), bins=20)
plt.tight_layout()
plt.show()

# Correlation heatmap
# Select only numerical features for correlation calculation
numerical_df = df.select_dtypes(include=np.number)  # Select numerical columns
plt.figure(figsize=(10, 8))
sns.heatmap(numerical_df.corr(), annot=True, cmap="coolwarm")  # Use numerical_df
plt.title("Correlation Heatmap")
plt.show()

"""HANDLING MISSING VALUES"""

# Fill or drop missing values
df.fillna(method='ffill', inplace=True)
print(df.isnull().sum())

"""ENCODE CATEGORICAL VALUES"""

# Encode categorical variables
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])
df.head()

"""TRAIN TEST SPLIT"""

# Feature-target split
X = df.drop("status", axis=1)
y = df["status"]

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#shape
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

"""MODEL SELECTION"""

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Initialize models
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "XGBoost": XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
}

"""MODEL TRAINING"""

# Train and evaluate each model
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

results = {}
for name, model in models.items():
    # Train model
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy
    print(f"\n{name}:\nAccuracy: {accuracy:.4f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title(f"Confusion Matrix: {name}")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

"""HYPERPARAMETER TUNING"""

from sklearn.model_selection import GridSearchCV

# Example: Random Forest hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best model
best_rf_model = grid_search.best_estimator_
print("Best Parameters for Random Forest:", grid_search.best_params_)

"""MODEL EVALUATION"""

# Evaluate best Random Forest model
y_pred_best = best_rf_model.predict(X_test)
accuracy_best = accuracy_score(y_test, y_pred_best)
print(f"Best Random Forest Model Accuracy: {accuracy_best:.4f}")

# Confusion matrix and metrics
conf_matrix = confusion_matrix(y_test, y_pred_best)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix: Best Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Bar plot for accuracy comparison
plt.bar(results.keys(), results.values(), color=['blue', 'green', 'orange'])
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.show()

"""VOTING CLASSIFIER"""

from sklearn.ensemble import VotingClassifier

# Voting Classifier
voting_clf = VotingClassifier(estimators=[
    ('lr', models['Logistic Regression']),
    ('rf', models['Random Forest']),
    ('xgb', models['XGBoost'])
], voting='hard')

voting_clf.fit(X_train, y_train)

# Evaluate Voting Classifier
y_pred_voting = voting_clf.predict(X_test)
voting_accuracy = accuracy_score(y_test, y_pred_voting)
print(f"Voting Classifier Accuracy: {voting_accuracy:.4f}")

"""SAVING MODEL"""

import pickle

# Save the trained model
with open("campus_placement_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully.")

from sklearn.preprocessing import StandardScaler

# Assuming X_train contains your training data features
scaler = StandardScaler()
scaler.fit(X_train)  # Fit the scaler to the training data

# Save the scaler
with open("scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)

"""load and use model"""

# Load the scaler
with open("scaler.pkl", "rb") as file:
    loaded_scaler = pickle.load(file)

# Load the model
with open("campus_placement_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

import numpy as np


new_data = np.array([[70, 80, 75, 1, 0, 0,0,0,0,0,0,0,0,0]])



scaled_data = loaded_scaler.transform(new_data)  # Scale the new data

# Predict
prediction = loaded_model.predict(scaled_data)
print("Placement Prediction:", "Placed" if prediction[0] == 1 else "Not Placed")