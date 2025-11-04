 # advanced_regression_ols.py
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

base = Path(".").resolve()
df = pd.read_csv(base / "sales_100.csv")

# ---- 基础清洗 ----
df["date"] = pd.to_datetime(df["date"])
df["day_of_week"] = df["date"].dt.day_name()  # Monday...Sunday

# 因变量：销量
y_col = "quantity"

# 自变量：单价 + 一堆分类特征（做虚拟变量）
# C() 会自动做哑变量，baseline 由 statsmodels 自动选择
formula = (
    "quantity ~ unit_price "
    "+ C(product_line) + C(city) + C(customer_type) "
    "+ C(gender) + C(payment) + C(day_of_week)"
)

# ---- 拟合 OLS ----
model = smf.ols(formula=formula, data=df).fit()

# 输出摘要到终端
print(model.summary())

# 保存摘要到文件
summary_txt = base / "ols_summary.txt"
with open(summary_txt, "w") as f:
    f.write(model.summary().as_text())
print(f"[SUCCESS] OLS 摘要已保存：{summary_txt}")

# 系数表另存为 CSV，便于看影响方向/强度
coef_df = model.params.rename("coef").to_frame()
coef_df["p_value"] = model.pvalues
coef_df["conf_low"] = model.conf_int()[0]
coef_df["conf_high"] = model.conf_int()[1]
coef_path = base / "ols_coefficients.csv"
coef_df.to_csv(coef_path)
print(f"[SUCCESS] 系数表已导出：{coef_path}")

# ---- 简单诊断：残差图（线性/同方差性大致检查）----
df["_fitted"] = model.fittedvalues
df["_resid"] = model.resid

plt.scatter(df["_fitted"], df["_resid"])
plt.axhline(0, linestyle="--")
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted (OLS)")
plt.tight_layout()
plt.savefig("ols_residuals_vs_fitted.png")
plt.close()
print("[SUCCESS] 残差图：ols_residuals_vs_fitted.png 已生成")

# ---- 给一个“价格弹性”直觉：固定其它变量，画出 价格-销量 的回归线 ----
# 用分位点抽两条产品线/城市做可视化参考（只是直觉，不是严格可视）
subset = df.copy()
# 取一个最常见的组合（减少其它因子的干扰，仅作示例）
mode_pl = subset["product_line"].mode()[0]
mode_city = subset["city"].mode()[0]
mode_ct = subset["customer_type"].mode()[0]
mode_gender = subset["gender"].mode()[0]
mode_pay = subset["payment"].mode()[0]
mode_dow = subset["day_of_week"].mode()[0]

grid = pd.DataFrame({
    "unit_price": np.linspace(df["unit_price"].min(), df["unit_price"].max(), 50),
    "product_line": mode_pl,
    "city": mode_city,
    "customer_type": mode_ct,
    "gender": mode_gender,
    "payment": mode_pay,
    "day_of_week": mode_dow
})

grid["y_pred"] = model.predict(grid)

plt.plot(grid["unit_price"], grid["y_pred"])
plt.xlabel("Unit Price")
plt.ylabel("Predicted Quantity")
plt.title(f"Price → Quantity (holding others at mode)\n"
          f"{mode_city}, {mode_pl}, {mode_ct}, {mode_gender}, {mode_pay}, {mode_dow}")
plt.tight_layout()
plt.savefig("price_to_quantity_curve.png")
plt.close()
print("[SUCCESS] 价格-销量预测曲线：price_to_quantity_curve.png 已生成")
