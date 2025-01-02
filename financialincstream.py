df = pd.read_csv(dataset_path, header=None)
df = pd.read_csv(dataset_path, header=None)
# -*- coding: utf-8 -*-
"""financialincSTREAm.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iC_a2VZ4GhOhPXJ8A1zboZuQ7vOp1oQj
"""


import pandas as pd
dataset_url = "https://drive.google.com/file/d/1MDZ8rsTEW8ETdiUXwdBKM9HW-Re92VAX/view?usp=sharing" 
df = pd.read_csv(dataset_path, header=None)



print(df.describe())
print('§§§§§§§§§§§')
print(df.isnull().sum())
print('§§§§§§§§§§§')
print(df.info())

df.head()

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib



# Drop unnecessary columns

# Encode categorical features
categorical_columns = [
    "country",
    "location_type", # Removed 'bank_account' from this list
    "cellphone_access",
    "gender_of_respondent",
    "relationship_with_head",
    "marital_status",
    "education_level",
    "job_type",
]
target_column = "bank_account"  # Assuming this is the target variable

# Encoding the target variable
le = LabelEncoder()
df[target_column] = le.fit_transform(df[target_column])

# Define feature matrix (X) and target vector (y)
X = df.drop(columns=[target_column])
y = df[target_column]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing for categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
    ],
    remainder="passthrough",  # Pass through numerical columns
)

# Define the Random Forest model
rf = RandomForestClassifier(random_state=42)

# Set up a pipeline
pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", rf)])

# Set up GridSearchCV parameters
param_grid = {
    "classifier__n_estimators": [100, 200, 300],
    "classifier__max_depth": [10, 20, None],
    "classifier__min_samples_split": [2, 5, 10],
}
grid_search = GridSearchCV(
    pipeline, param_grid, cv=3, scoring="accuracy", verbose=3, n_jobs=-1
)

# Fit the model
grid_search.fit(X_train, y_train)

# Evaluate the model
y_pred = grid_search.best_estimator_.predict(X_test)
print("Best Parameters:", grid_search.best_params_)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model for Streamlit
joblib.dump(grid_search.best_estimator_, "rf_model.pkl")
print("Model saved as rf_model.pkl")



# Commented out IPython magic to ensure Python compatibility.
# %%writefile streamlit_app.py
# import streamlit as st
# import pandas as pd
# import joblib
# 
# # Load the trained model
# model = joblib.load("rf_model.pkl")
# 
# # Title of the Streamlit App
# st.title("Bank Account Prediction App")
# 
# # Input fields for the user to provide data
# st.header("Provide the following details:")
# 
# country = st.selectbox("Country", ["Kenya", "Rwanda", "Tanzania", "Uganda"])
# year = st.selectbox("Year", [2016, 2017, 2018])
# location_type = st.selectbox("Location Type", ["Rural", "Urban"])
# cellphone_access = st.selectbox("Cellphone Access", ["Yes", "No"])
# household_size = st.number_input("Household Size", min_value=1, max_value=30, step=1)
# age_of_respondent = st.number_input("Age of Respondent", min_value=16, max_value=100, step=1)
# gender_of_respondent = st.selectbox("Gender", ["Male", "Female"])
# marital_status = st.selectbox("Marital Status", ["Married/Living together", "Divorced/Separated", "Widowed", "Single/Never Married"])
# education_level = st.selectbox("Education Level", [
#     "No formal education", "Primary education", "Secondary education",
#     "Vocational/Specialised training", "Tertiary education", "Other/Dont know/RTA"
# ])
# job_type = st.selectbox("Job Type", [
#     "Farming and Fishing", "Self employed", "Formally employed Government",
#     "Formally employed Private", "Informally employed", "Remittance Dependent",
#     "Government Dependent", "Other Income", "No Income", "Dont Know/Refuse to answer"
# ])
# 
# # Button to predict
# if st.button("Predict"):
#     # Prepare the input data
#     input_data = pd.DataFrame({
#         "country": [country],
#         "year": [year],
#         "location_type": [location_type],
#         "cellphone_access": [cellphone_access],
#         "household_size": [household_size],
#         "age_of_respondent": [age_of_respondent],
#         "gender_of_respondent": [gender_of_respondent],
#         "marital_status": [marital_status],
#         "education_level": [education_level],
#         "job_type": [job_type],
#     })
# 
#     # Make predictions
#     prediction = model.predict(input_data)
#     st.write("Prediction:", "Yes" if prediction[0] == 1 else "No")
#
