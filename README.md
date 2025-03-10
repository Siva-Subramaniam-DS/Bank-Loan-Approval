# 🏦 Loan Approval System
```markdown

## 📌 Table of Contents
1. [📖 Introduction](#-introduction)
2. [🚀 Features](#-features)
3. [⚙️ Tech Stack](#️-tech-stack)
4. [📂 Project Structure](#-project-structure)
5. [🛠 Installation Guide](#-installation-guide)
6. [🚀 How to Run the Project](#-how-to-run-the-project)
7. [📝 Usage Guide](#-usage-guide)
8. [📊 Loan Approval Logic](#-loan-approval-logic)
9. [🔄 Logging & Background Jobs](#-logging--background-jobs)
10. [📌 API Endpoints (if applicable)](#-api-endpoints-if-applicable)
11. [🖥 UI Overview](#-ui-overview)
12. [📸 Screenshots](#-screenshots)
13. [📜 License](#-license)
14. [👨‍💻 Author](#-author)

---

## 📖 Introduction  
The **Loan Approval System** is a web-based application that automates loan approvals for banks and financial institutions. It fetches customer data from **MongoDB** and uses a **Machine Learning (ML) model** to predict whether a loan should be **Approved** or **Rejected**.  

Additionally, the system provides **detailed explanations** for each decision, helping both customers and financial officers understand the reasoning behind the loan status.

---

## 🚀 Features  
✅ **Customer Search**: Enter a name to fetch details from MongoDB.  
✅ **ML-Based Loan Approval**: Approves or rejects loans using a trained model.  
✅ **Decision Explanation**: Displays reasons for approval/rejection.  
✅ **Logging & Auditing**: Daily logs to track loan applications.  
✅ **Streamlit UI**: Simple and interactive interface.  
✅ **Automated Log Rotation**: Logs are saved daily at 6:00 PM.  

---

## ⚙️ Tech Stack  
| Component        | Technology Used |
|-----------------|----------------|
| 🖥 Frontend     | Streamlit (Python) |
| ⚙️ Backend     | Flask, Python |
| 📡 Database    | MongoDB |
| 🤖 ML Model    | Scikit-Learn (Joblib) |
| 📝 Logging     | Python Logging Module |
| ⏰ Scheduler   | APScheduler |

---

## 📂 Project Structure  
```
Loan-Approval-System/
│── logs/                      # Stores daily logs
│── models/
│   ├── loan_model.pkl         # Trained ML model
│   ├── label_encoders.pkl     # Encoders for categorical variables
│── app.py                     # Main Streamlit application
│── database.py                 # MongoDB connection
│── README.md                   # Project documentation
│── requirements.txt             # Required Python packages
│── utils.py                     # Helper functions
```

---

## 🛠 Installation Guide  
### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/Loan-Approval-System.git
cd Loan-Approval-System
```

### **Step 2: Create & Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Start MongoDB**  
Ensure MongoDB is installed and running:
```bash
mongod --dbpath <your-db-path>
```

---

## 🚀 How to Run the Project  
```bash
streamlit run app.py
```
The **Loan Approval System** will be available at:
```
http://localhost:8501/
```

---

## 📝 Usage Guide  
1. **Search for a Customer**  
   - Enter the customer’s **name**.  
   - The system fetches details from **MongoDB**.  

2. **Check Loan Approval**  
   - Click **Check Loan Status**.  
   - The **ML model** predicts **Approved** or **Rejected**.  
   - A **detailed explanation** is provided.  

3. **Logging & Auditing**  
   - User activity is logged in `logs/loan_activity_YYYY-MM-DD.log`.  

---

## 📊 Loan Approval Logic  
The **loan decision** is based on several factors:  

| Factor               | Impact on Loan Approval |
|----------------------|-----------------------|
| **Credit Score**     | Higher score = Higher chances of approval |
| **Income Stability** | Stable income = Higher chances |
| **Existing Loans**   | More than 2 loans = Higher rejection risk |
| **Employment Type**  | Salaried employees = Higher approval chances |
| **Loan Amount**      | High requested loan = Higher rejection risk |

---

## 🔄 Logging & Background Jobs  
- Logs **every loan request** in a daily log file.  
- **Rotates logs automatically** at 6:00 PM daily.  
- Uses **APScheduler** for scheduled logging.  

---

## 📌 API Endpoints (if applicable)  
| Method | Endpoint         | Description |
|--------|----------------|-------------|
| GET    | `/api/status`  | Fetch system status |
| POST   | `/api/loan`    | Submit loan application |
| GET    | `/api/logs`    | Fetch logs |

---

## 🖥 UI Overview  
The **Streamlit UI** consists of:  
✔ **Customer Search Bar**  
✔ **Loan Status Prediction**  
✔ **Decision Explanation**  

---

## 📸 Screenshots  
### ✅ Loan Approved  
![Loan Approved Screenshot](![Screenshot 2025-03-10 090313](https://github.com/user-attachments/assets/eebd4909-c73c-4fe8-a34d-d6c5393e607b)
)  

### ❌ Loan Rejected  
![Loan Rejected Screenshot](![Screenshot 2025-03-10 090329](https://github.com/user-attachments/assets/2143ad99-ba9c-4c45-9207-3508b3a209d7)
)  

---

## 📜 License  
This project is licensed under the **MIT License**.  

---

## 👨‍💻 Author  
- **Your Name**  
- GitHub: [@yourusername](https://github.com/Siva-Subramaniam-DS)  
- LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/r-siva-subramanaiam/)  

---
```

### ✅ **Why This README is Effective?**
✔ **Clear structure** with a **Table of Contents**  
✔ **Step-by-step Installation & Usage Guide**  
✔ **Technical Details** (ML Model, Logging, MongoDB)  
✔ **API Endpoints Table** (if needed)  
✔ **Screenshots for better clarity**  
✔ **Licensing & Author Information**  

Now, you can **copy-paste this into your `README.md`** and update **your name & links** accordingly! 🚀
