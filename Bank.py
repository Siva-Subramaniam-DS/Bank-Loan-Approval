import streamlit as st
import pymongo
import pandas as pd
import joblib
import os
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from deep_translator import GoogleTranslator
import atexit

# ----------------- Set Page Config -----------------
st.set_page_config(page_title="Loan Approval System", page_icon="🏦", layout="wide")

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

# ----------------- Language Support -----------------
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Telugu": "te",
    "Kannada": "kn"
}

def translate_text(text, lang):
    """Translate text using deep-translator"""
    if lang == "en":  
        return text
    return GoogleTranslator(source="auto", target=lang).translate(text)

# ----------------- Streamlit UI -----------------
selected_lang = st.sidebar.selectbox("🌍 Choose Language", list(LANGUAGES.keys()))
lang_code = LANGUAGES[selected_lang]

st.markdown(f'<h2 style="text-align: center; color: #004aad;">🏦 {translate_text("Loan Approval System", lang_code)}</h2>', unsafe_allow_html=True)

# ----------------- Customer Search -----------------
customer_name = st.text_input(f"🔍 {translate_text('Enter Customer Name', lang_code)}")

if customer_name:
    customer = collection.find_one({"Name": customer_name}, {"_id": 0})

    if customer:
        st.write(f"### 📌 {translate_text('Customer Details', lang_code)}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**👤 {translate_text('Name', lang_code)}:** {customer['Name']}")
            st.markdown(f"**🎂 {translate_text('Age', lang_code)}:** {customer['Age']}")
            st.markdown(f"**🚻 {translate_text('Gender', lang_code)}:** {customer['Gender']}")
            st.markdown(f"**📞 {translate_text('Phone', lang_code)}:** {customer['Phone_Number']}")
            st.markdown(f"**📍 {translate_text('Address', lang_code)}:** {customer['City']}, {customer['State']} - {customer['Pincode']}")

        with col2:
            st.markdown(f"**🏦 {translate_text('Bank Balance', lang_code)}:** ₹{customer['Bank_Balance']}")
            st.markdown(f"**💳 {translate_text('CIBIL Score', lang_code)}:** {customer['CIBIL_Score']}")
            st.markdown(f"**📉 {translate_text('Existing Loans', lang_code)}:** {customer['Existing_Loans']}")
            st.markdown(f"**💰 {translate_text('Loan Amount Requested', lang_code)}:** ₹{customer['Loan_Amount_Requested']}")
            st.markdown(f"**📆 {translate_text('Loan Tenure', lang_code)}:** {customer['Loan_Tenure_Months']} months")

        # ----------------- Prepare Data for Prediction -----------------
        input_data = pd.DataFrame([customer])

        # Drop unnecessary columns
        input_data.drop(columns=["Customer_ID", "Name", "Phone_Number", "Email", "Address", "City", "State", "Pincode", "Loan_Status"], inplace=True, errors='ignore')

        # Encode categorical variables safely
        categorical_cols = ["Gender", "Income_Source", "Employment_Type"]
        for col in categorical_cols:
            if col in input_data.columns and col in label_encoders:
                try:
                    input_data[col] = label_encoders[col].transform([str(input_data[col].values[0])])
                except ValueError:
                    st.error(f"❌ {translate_text('Unknown category', lang_code)} '{input_data[col].values[0]}' {translate_text('for', lang_code)} {col}.")
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
        reasons.append(f"{translate_text('Low CIBIL Score', lang_code)} (💳 {customer['CIBIL_Score']} < 650)")
    if customer['Bank_Balance'] < 50000:
        reasons.append(f"{translate_text('Low Bank Balance', lang_code)} (💰 ₹{customer['Bank_Balance']} < ₹50,000)")
    if customer['Existing_Loans'] == "Yes":
        reasons.append(f"{translate_text('Has Existing Loans', lang_code)} (📉 {translate_text('Loan already active', lang_code)})")
    if customer['Loan_Amount_Requested'] > customer['Bank_Balance'] * 2:
        reasons.append(f"{translate_text('High Loan Amount Compared to Balance', lang_code)} (💵 ₹{customer['Loan_Amount_Requested']} > 2x ₹{customer['Bank_Balance']})")
    if customer['Employment_Type'] in ["Unemployed", "Contract"]:
        reasons.append(f"{translate_text('Unstable Employment', lang_code)} (💼 {translate_text(customer['Employment_Type'], lang_code)})")

    # Display Loan Status
    if loan_status == "Approved":
        st.success(f"✅ {translate_text('Loan Status:', lang_code)} {translate_text('Approved', lang_code)}")
        st.info(f"**✅ {translate_text('Reasons for Approval:', lang_code)}**")
        st.markdown(f"- **{translate_text('High CIBIL Score', lang_code)}**" if customer['CIBIL_Score'] >= 650 else "")
        st.markdown(f"- **{translate_text('Good Bank Balance', lang_code)}**" if customer['Bank_Balance'] >= 50000 else "")
        st.markdown(f"- **{translate_text('No Existing Loans', lang_code)}**" if customer['Existing_Loans'] == "No" else "")
        st.markdown(f"- **{translate_text('Stable Employment', lang_code)}**" if customer['Employment_Type'] not in ["Unemployed", "Contract"] else "")

    else:
        st.error(f"❌ {translate_text('Loan Status:', lang_code)} {translate_text('Rejected', lang_code)}")
        st.warning(f"**🚨 {translate_text('Reasons for Rejection:', lang_code)}**")
        for reason in reasons:
            st.markdown(f"- {reason}")

    # Log Activity
    logging.info(f"Checked loan status for {customer_name} - Result: {loan_status}")


# ----------------- Stop Scheduler on Exit -----------------
atexit.register(lambda: scheduler.shutdown())
