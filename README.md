# Sales Analytics & ML Automation (Python)

### ✅ Overview
This project builds a full automated analytics pipeline for sales data using Python.
It performs:
- Data cleaning & descriptive statistics  
- Revenue analysis by city, product line, payment method, and gender  
- Multi-sheet Excel report generation  
- Visualization (PNG charts)
- Logistic Regression model to classify high-spending orders
- PDF business report generation with insights and charts

### ✅ Tech Stack
- Python
- Pandas
- Scikit-learn
- Matplotlib
- OpenPyXL
- ReportLab

---

### ✅ Key Features

#### 📊 Business Analytics
| Analysis Type | Output |
|---------------|--------|
| Revenue by City | city_revenue_chart.png |
| Revenue by Product Line | product_revenue_chart.png |
| Revenue by Gender | gender_revenue_chart.png |
| Revenue by Payment | payment_revenue_chart.png |

All results exported to:
``sales_report.xlsx`` (5 sheets)

#### 🤖 Machine Learning
- Model: Logistic Regression
- Task: Predict whether an order is a **high spender**
- Test performance:
  - **Accuracy:** 0.92  
  - **Precision (High):** 0.917  
  - **Recall (High):** 0.917  
  - **ROC-AUC:** 0.968

ROC curve: `roc_curve.png`

Predictions exported to: `sales_with_predictions.csv`

---

### ✅ PDF Output
`sales_report_ai_version.pdf`
Includes:
- KPI table
- Model performance table
- Business insights
- 4 business charts
- ROC curve

---

### ✅ Folder Structure
