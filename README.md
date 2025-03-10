# Loan Approval Prediction System

## Table of Contents
1. [Overview](#overview)
2. [Dataset](#dataset)
3. [Preprocessing](#preprocessing)
4. [Model Training](#model-training)
5. [Loan Prediction & Decision Explanation](#loan-prediction--decision-explanation)
6. [Multi-Language Support](#multi-language-support)
7. [Logging & Activity Tracking](#logging--activity-tracking)
8. [Dependencies](#dependencies)
9. [How to Run](#how-to-run)

---

## Overview
This project is a **Loan Approval Prediction System** that predicts whether a loan will be approved or rejected based on various financial and personal factors. The system also provides an explanation for the decision using key financial indicators.

## Dataset
- The dataset used is `Loan_Approval_Indian_Customers.csv`.
- It includes customer information such as **CIBIL Score, Bank Balance, Existing Loans, Employment Type, and Loan Amount Requested**.
- Certain sensitive columns like **Customer_ID, Name, Phone_Number, Email, Address, City, State, and Pincode** are excluded from model training.

## Preprocessing
- Categorical columns (`Gender`, `Existing_Loans`, `Income_Source`, `Employment_Type`, `Loan_Status`) are **label-encoded**.
- The dataset is split into training and testing sets (**80-20 split**).

## Model Training
- The model used is **Logistic Regression**.
- The trained model is saved as `loan_model.pkl`.
- Label encoders are saved separately as `label_encoders.pkl` for future use.

## Loan Prediction & Decision Explanation
- The system predicts whether a loan is **Approved** or **Rejected**.
- If rejected, reasons such as **low CIBIL score, low bank balance, existing loans, high requested loan amount, or unstable employment** are provided.
- If approved, positive indicators such as **high CIBIL score, sufficient bank balance, no existing loans, and stable employment** are highlighted.

## Multi-Language Support
- The system includes **multi-language support** for error messages and key decision explanations.
- Uses `translate_text()` function to display messages in different languages based on user selection.

## Logging & Activity Tracking
- Every loan check is logged using Python’s `logging` module.
- Logs include the **customer name and the loan approval result** for tracking purposes.

## Dependencies
Ensure you have the following libraries installed:
```bash
pip install pandas numpy scikit-learn joblib streamlit
```

## How to Run
1. **Train the Model:**
   ```bash
   python train_model.py
   ```
2. **Run the Web App:**
   ```bash
   streamlit run loan_app.py
   ```

This will launch the web interface where users can enter their financial details and check their loan approval status.

---
**🚀 Built for fast and accurate loan predictions!**

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests.

## 📜 License
This project is licensed under the **MIT License**.

---

## 👨‍💻 Author  
- **Your Name** - Siva Subramaniam R 
- GitHub: [@yourusername](https://github.com/Siva-Subramaniam-DS)  
- LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/r-siva-subramanaiam/)  

---

