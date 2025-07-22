
import streamlit as st
import pandas as pd
import numpy as np

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title='Employee Salary Prediction', layout='wide')

st.sidebar.header("User Input")

qualification = st.sidebar.selectbox(
    "Qualification",
    ["Choose an option", "Graduate", "Post-Graduate", "PhD"],
    index=0
)

age = st.sidebar.slider("Age", min_value=18, max_value=65, value=25)

name = st.sidebar.text_input("Name:", placeholder="Enter candidate name...")

job_role = st.sidebar.text_input("Job role:", placeholder="Enter job role...")

hour_per_week = st.sidebar.slider("Hours per week", 20, 80, 40)

experience = st.sidebar.slider("Years of experience", 0, 47, 5)

sidebar_predict = st.sidebar.button("Predict")

st.title("Employee Salary Prediction")

table_cols = ["Name", "Age", "Qualification", "Job Role", "Hours/Week", "Experience", "Predicted Salary"]
result_placeholder = st.empty()

def predict_salary(features):
    base = 20000 + features['experience'] * 1000 + features['age'] * 200 + features['hour_per_week'] * 40
    if features['qualification'] == "Post-Graduate":
        base += 8000
    if features['qualification'] == "PhD":
        base += 18000
    if "manager" in features['job_role'].lower():
        base += 10000
    if "data" in features['job_role'].lower():
        base += 8000
    return int(base // 100) * 100  

if sidebar_predict and qualification != "Choose an option":
    features = {
        "name": name,
        "age": age,
        "qualification": qualification,
        "job_role": job_role,
        "hour_per_week": hour_per_week,
        "experience": experience
    }
    pred_salary = predict_salary(features)
    df_display = pd.DataFrame([[
        features["name"], features["age"], features["qualification"],
        features["job_role"], features["hour_per_week"], features["experience"],
        f"${pred_salary:,.0f}"
    ]], columns=table_cols)
    result_placeholder.table(df_display)
elif sidebar_predict and qualification == "Choose an option":
    st.warning("Please select a valid qualification.")

st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Choose CSV file (columns: Name, Age, Qualification, Job Role, Hours/Week, Experience)", type=["csv"])
file_predict = st.button('Predict on File')

batch_graph_placeholder = st.empty()
batch_result_placeholder = st.empty()

if file_predict and uploaded_file is not None:
    df_in = pd.read_csv(uploaded_file)
    # Ensure column names match expectation
    required_cols = {"Name", "Age", "Qualification", "Job Role", "Hours/Week", "Experience"}
    if not required_cols.issubset(df_in.columns):
        st.error(f"Uploaded file missing one or more required columns: {required_cols}")
    else:
        results = []
        for _, row in df_in.iterrows():
            features = {
                "name": row.get("Name",""),
                "age": int(row.get("Age", 0)),
                "qualification": row.get("Qualification","Graduate"),
                "job_role": row.get("Job Role",""),
                "hour_per_week": int(row.get("Hours/Week", 0)),
                "experience": int(row.get("Experience", 0)),
            }
            pred_sal = predict_salary(features)
            results.append({
                "Name": features["name"],
                "Age": features["age"],
                "Qualification": features["qualification"],
                "Job Role": features["job_role"],
                "Hours/Week": features["hour_per_week"],
                "Experience": features["experience"],
                "Predicted Salary": pred_sal
            })
        df_out = pd.DataFrame(results)
        batch_result_placeholder.table(df_out)
        batch_graph_placeholder.line_chart(df_out[["Predicted Salary"]])

elif file_predict and uploaded_file is None:
    st.warning("Please upload a CSV file for batch prediction.")

st.markdown("""
*Instructions:*  
- Use the sidebar to enter employee details and predict a single salary.  
- To predict salaries for many people at once, upload a CSV with columns:  
  Name, Age, Qualification, Job Role, Hours/Week, Experience.
  Then click 'Predict on File'.  
- At right/below, you will see a graph and a table of predicted salaries.
""")
