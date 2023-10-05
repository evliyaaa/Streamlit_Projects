# -*- coding: utf-8 -*-
"""Seller_ChurnPrediction.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sKPkUQ2p4IUK7PuhIoFnm2KwnnHayYqV
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
pd.set_option('display.max_rows', None)
from datetime import datetime

sns.set(style="whitegrid")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)

#!pip install gdown

import gdown

file_id = '1RCyHNbDuAAc3yyBPCamRt8_CmT1GRXuV'

url = f'https://drive.google.com/uc?id={file_id}'

output_file = r'C:\Users\evliy\OneDrive\Desktop\Internship\All_Users.csv'

gdown.download(url, output_file, quiet=False)

df = pd.read_csv(output_file)

## Converting the datatype
df['Register Date'] = pd.to_datetime(df['Register Date'])
df['Suspended Date'] = pd.to_datetime(df['Suspended Date'])

df.head()

from datetime import datetime

current_date = datetime(2023, 8, 20)

df['Churned'] = df['Suspended Date'].notnull()

df.head(1)

df_3 = df.drop(["Seller ID", "Register Date", "Suspended Date", "Registration Source", "Status", "Cancellation Reason"], axis=1);

data1 = df_3[df_3['Churned']==1]
print("Churn olanlar-data1:"+ str(data1.shape))
data2 = df_3[df_3['Churned']==0]

print("Churn olmayanlar-data2:"+ str(data2.shape))

# Set the random seed for reproducibility
np.random.seed(42)

# Shuffle the rows of data1 and data2
data1_shuffled = data1.sample(frac=1, random_state=42)
data2_shuffled = data2.sample(frac=1, random_state=42)

# Choose rows from data1 where Total Income or Total Profit > 1
condition = (data1_shuffled['Total Income'] > 1) | (data1_shuffled['Total Profit'] > 1)
selected_data1 = data1_shuffled[condition]

# Randomly select 2370 samples from the selected_data1
random_indices = np.random.choice(selected_data1.index, size=2370, replace=False)
random_data1 = selected_data1.loc[random_indices]

# Combine randomly shuffled data1 with shuffled data2
shuffled_data = pd.concat([data2_shuffled, random_data1])

# Shuffle the rows of the final dataset
final_data = shuffled_data.sample(frac=1, random_state=42)

print("Final Dataset Shape:", final_data.shape)

#corr_matrix = final_data.corr()
#plt.figure(figsize=(10, 8))
#sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=.5);
#plt.show()

X = final_data.drop(columns=['Churned'], axis = 1)
y = final_data['Churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

## Gradient Boosting

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
from yellowbrick.classifier import ClassPredictionError
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.metrics import precision_recall_curve, PrecisionRecallDisplay, RocCurveDisplay, roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier(n_estimators = 100, learning_rate = 0.1, max_depth = 5,
                                   min_samples_leaf = 7, min_samples_split = 2, random_state=42)
model.fit(X_train, y_train)
#model.feature_importances_
#feats = pd.DataFrame(index=X.columns, data=model.feature_importances_, columns=['grad_importance'])
#grad_imp_feats = feats.sort_values("grad_importance")

def eval_metric(model, X_train, y_train, X_test, y_test):
    y_train_pred = model.predict(X_train)
    y_pred = model.predict(X_test)
    print("Test_Set")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print()
    print("Train_Set")
    print(confusion_matrix(y_train, y_train_pred))
    print(classification_report(y_train, y_train_pred))

eval_metric(model, X_train, y_train, X_test, y_test)

#visualizer = ClassPredictionError(model)
# Fit the training data to the visualizer
#visualizer.fit(X_train, y_train)
# Evaluate the model on the test data
#visualizer.score(X_test, y_test)
# Draw visualization
#visualizer.poof();

#RocCurveDisplay.from_estimator(model, X_test, y_test);

#!pip install streamlit
#!pip install ipython
#!pip install openpyxl
#!pip install streamlit_shap

import streamlit as st
from sklearn.ensemble import GradientBoostingClassifier
from PIL import Image
import pandas as pd
import shap
import streamlit_shap
from streamlit_shap import st_shap
from io import BytesIO
import base64
import openpyxl
# Load your trained model
#model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5,
                                   #min_samples_leaf=7, min_samples_split=2, random_state=42)
# Create a SHAP explainer for your model
#explainer = shap.Explainer(model)
#explainer = shap.Explainer(model, user_input)

# Streamlit app
# Main title with yellow highlighting
st.markdown("<h1 style='text-align: center; color: yellow;'>Churn Prediction App</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: right;'> Enter Features</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
# Display the image in the left column
with col1:
    #image = Image.open("Internship_DataScience/logo.jpg")
    # Display the image using Streamlit
    #st.image(image, width=320)
    #st.image(image, use_column_width=True)
    image_url = "https://github.com/evliyaaa/Internship_DataScience/raw/main/logo.jpg"
    #response = requests.get(image_url)
    #image = Image.open(BytesIO(response.content))
    st.image(image_url, use_column_width=True)

# Display the "Enter Features" title and text input elements in the right column
with col2:
    total_account = st.text_input("Total Account Count", "")
    total_products = st.text_input("Total Product Count", "")
    total_income = st.text_input("Total Income", "")
    total_profit = st.text_input("Total Profit", "")
    active_days = st.text_input("Active Days", "")
    
    if st.button("Predict Churn"):
        # Create a DataFrame from user inputs
        user_input = pd.DataFrame({'Total Account Count': [total_account],
                                   'Total Product Count': [total_products],
                                   'Total Income': [total_income],
                                   'Total Profit': [total_profit],
                                   'Active Days': [active_days]})

        # Convert input values to numeric (assuming they are numeric features)
        user_input = user_input.apply(pd.to_numeric, errors='coerce')

        # Validate that 'Total Account' and 'Active days' are greater than 0
        if (user_input['Total Account Count'].astype(float) <= 0).any() or (user_input['Active Days'].astype(float) <= 0).any():
            st.error("Total Account and Active days must be greater than 0.")
        else:
            prediction = model.predict(user_input)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(user_input)
            if prediction[0] == True:
                st.markdown("<span style='background-color:red; color:black; font-size:20px;'>Seller is predicted to churn</span>", unsafe_allow_html=True)
                st.subheader("Decision SHAP Plot Shows Importance of Features")
                if len(shap_values) > 0:
                    st_shap(shap.decision_plot(explainer.expected_value, shap_values[0,:], user_input.iloc[0,:], link='logit'), height=300, width=600)
                else:
                    st.warning("SHAP values for Class True are not available.")
            else:
                st.markdown("<span style='background-color:green; color:black; font-size:20px;'>Seller is predicted not to churn</span>",unsafe_allow_html=True)
                st.subheader("Decision SHAP Plot Shows Importance of Features")
                if len(shap_values) > 0:
                    st_shap(shap.decision_plot(explainer.expected_value, shap_values[0,:], user_input.iloc[0,:], link='logit'), height=300, width=600)
                else:
                    st.warning("SHAP values for Class False are not available.")
                 
# Show two sample values from your dataset, one with Churned=True and one with Churned=False
st.subheader("Selected Sample Rows")
selected_row_1 = df.iloc[2459]
selected_row_2 = df.iloc[6844]
# Display the selected rows horizontally
st.dataframe([selected_row_1, selected_row_2])

# Add a section to allow users to upload an Excel file
st.subheader("Upload Excel File for Batch Predictions")
uploaded_file = st.file_uploader("Upload Excel File (with 5 features)", type=["xlsx", "xls"])

if uploaded_file is not None:
    user_data = pd.read_excel(uploaded_file)

    expected_columns = ['Total Account Count', 'Total Product Count', 'Total Income', 'Total Profit', 'Active Days']
    
    if set(expected_columns).issubset(user_data.columns):
        if (user_data['Total Account Count'].astype(float) <= 0).any() or (user_data['Active Days'].astype(float) <= 0).any():
            st.error("Total Account and Active days must be greater than 0 in the uploaded file.")
        else:
            predictions = model.predict(user_data)
            predictions_df = pd.DataFrame({'Predictions': predictions})
            result_df = pd.concat([user_data, predictions_df], axis=1)
            st.subheader("Predictions")
            st.write(result_df)

            def get_table_download_link(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:  # Specify the engine
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                excel_data = output.getvalue()
                b64 = base64.b64encode(excel_data).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="churn_predictions.xlsx">Download Predictions as Excel</a>'
                return href

            # Display the download link
            st.markdown(get_table_download_link(result_df), unsafe_allow_html=True)
    else:
        st.error("Please upload an Excel file with the correct columns: Total Account Count, Total Product Count, Total Income, Total Profit, Active Days")
