# advanced_logistic_high_spender.py
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

base = Path(".").resolve()
df = pd.read_csv(base / "sales_100.csv")
df["date"] = pd.to_datetime(df["date"])
df["day_of_week"] = df["date"].dt.day_name()

# 标签：是否大额订单（>= 中位数）
threshold = df["total"].median()
df["high_spender"] = (df["total"] >= threshold).astype(int)

# 特征
num_features = ["unit_price", "quantity"]
cat_features = ["product_line", "city", "customer_type", "gender", "payment", "day_of_week"]

X = df[num_features + cat_features]
y = df["high_spender"]

# 预处理：数值留原样，类别做 One-Hot
ct = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
        ("num", "passthrough", num_features),
    ]
)

# 逻辑回归（带一点正则，防过拟合）
clf = Pipeline(steps=[
    ("prep", ct),
    ("model", LogisticRegression(max_iter=1000))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]

print("[INFO] 分类报告（High Spender 预测）：")
print(classification_report(y_test, y_pred, digits=3))
print(f"[INFO] ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")
