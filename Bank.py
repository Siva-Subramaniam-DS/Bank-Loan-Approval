import streamlit as st
import pymongo
import pandas as pd
import joblib
import os
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# ----------------- MongoDB Connection -----------------
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["LoanApprovalDB"]
collection = db["Customers"]

# ----------------- Load Model & Encoders -----------------
model_path = "loan_model.pkl"
encoders_path = "label_encoders.pkl"

if not os.path.exists(model_path) or not os.path.exists(encoders_path):
    st.error("❌ Missing model files. Please check your directory.")
    st.stop()

model = joblib.load(model_path)
label_encoders = joblib.load(encoders_path)

# Get model's expected features
expected_features = model.feature_names_in_

# ----------------- Logging Setup -----------------
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_filename = os.path.join(log_folder, "loan_activity.log")

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Function to rename logs at 6:00 PM
def save_log_file():
    now = datetime.datetime.now()
    new_filename = f"logs/loan_activity_{now.strftime('%Y-%m-%d')}.log"
    if os.path.exists(log_filename):
        os.rename(log_filename, new_filename)
        logging.info("Log file saved successfully.")

# Background Scheduler for Log Saving
scheduler = BackgroundScheduler()
scheduler.add_job(save_log_file, 'cron', hour=18, minute=0)
scheduler.start()

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Loan Approval System", page_icon="🏦", layout="wide")

st.markdown('<h2 style="text-align: center; color: #004aad;">🏦 Loan Approval System</h2>', unsafe_allow_html=True)

# ----------------- Customer Search -----------------
customer_name = st.text_input("🔍 Enter Customer Name")

if customer_name:
    customer = collection.find_one({"Name": customer_name}, {"_id": 0})
    
    if customer:
        st.write("### 📌 Customer Details")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**👤 Name:** {customer['Name']}")
            st.markdown(f"**🎂 Age:** {customer['Age']}")
            st.markdown(f"**🚻 Gender:** {customer['Gender']}")
            st.markdown(f"**📞 Phone:** {customer['Phone_Number']}")
            st.markdown(f"**📍 Address:** {customer['City']}, {customer['State']} - {customer['Pincode']}")

        with col2:
            st.markdown(f"**🏦 Bank Balance:** ₹{customer['Bank_Balance']}")
            st.markdown(f"**💳 CIBIL Score:** {customer['CIBIL_Score']}")
            st.markdown(f"**📉 Existing Loans:** {customer['Existing_Loans']}")
            st.markdown(f"**💰 Loan Amount Requested:** ₹{customer['Loan_Amount_Requested']}")
            st.markdown(f"**📆 Loan Tenure:** {customer['Loan_Tenure_Months']} months")

        # ----------------- Prepare Data for Prediction -----------------
        input_data = pd.DataFrame([customer])

        # Drop unnecessary columns
        input_data.drop(columns=["Customer_ID", "Name", "Phone_Number", "Email", 
                                 "Address", "City", "State", "Pincode", "Loan_Status"], 
                        inplace=True, errors='ignore')

        # Encode categorical variables safely
        categorical_cols = ["Gender", "Income_Source", "Employment_Type"]
        for col in categorical_cols:
            if col in input_data.columns and col in label_encoders:
                try:
                    input_data[col] = label_encoders[col].transform([str(input_data[col].values[0])])
                except ValueError:
                    st.error(f"❌ Unknown category '{input_data[col].values[0]}' for {col}.")
                    st.stop()
            else:
                input_data[col] = 0  # Default value if missing

        # Convert 'Existing_Loans' ("Yes"/"No") to binary (1/0)
        input_data["Existing_Loans"] = 1 if customer["Existing_Loans"] == "Yes" else 0

        # Ensure all expected features exist
        for col in expected_features:
            if col not in input_data.columns:
                input_data[col] = 0  

        # Reorder columns correctly
        input_data = input_data[expected_features]

        # ----------------- Predict Loan Status -----------------
        prediction = model.predict(input_data)[0]
        loan_status = "Approved" if prediction == 1 else "Rejected"

        # ----------------- Explain Loan Decision -----------------
        reasons = []
        if customer['CIBIL_Score'] < 650:
            reasons.append("Low CIBIL Score (💳 Less than 650)")
        if customer['Bank_Balance'] < 50000:
            reasons.append("Low Bank Balance (💰 Less than ₹50,000)")
        if customer['Existing_Loans'] == "Yes":
            reasons.append("Has Existing Loans (📉 Loan already active)")
        if customer['Loan_Amount_Requested'] > customer['Bank_Balance'] * 2:
            reasons.append("High Loan Amount Compared to Balance (💵 Requested > 2x Bank Balance)")
        if customer['Employment_Type'] in ["Unemployed", "Contract"]:
            reasons.append("Unstable Employment (💼 Not Full-time/Permanent Job)")

        # Display Loan Status
        if loan_status == "Approved":
            st.success(f"✅ Loan Status: {loan_status}")
            st.info("**✅ Reasons for Approval:**")
            st.markdown("- **High CIBIL Score** (📊 Above 650)" if customer['CIBIL_Score'] >= 650 else "")
            st.markdown("- **Good Bank Balance** (💰 More than ₹50,000)" if customer['Bank_Balance'] >= 50000 else "")
            st.markdown("- **No Existing Loans** (📉 No active loans)" if customer['Existing_Loans'] == "No" else "")
            st.markdown("- **Stable Employment** (💼 Permanent Job)" if customer['Employment_Type'] not in ["Unemployed", "Contract"] else "")

        else:
            st.error(f"❌ Loan Status: {loan_status}")
            st.warning("**🚨 Reasons for Rejection:**")
            for reason in reasons:
                st.markdown(f"- {reason}")

        # Log Activity
        logging.info(f"Checked loan status for {customer_name} - Result: {loan_status}")

    else:
        st.warning("⚠️ Customer not found.")

# ----------------- Stop Scheduler on Exit -----------------
import atexit
atexit.register(lambda: scheduler.shutdown())
