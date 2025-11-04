import pandas as pd
from pathlib import Path

base = Path(".").resolve()
df = pd.read_csv(base / "sales_100.csv")

# -------- 分析结果生成 --------

# 按城市
city = df.groupby("city")["total"].sum().reset_index().sort_values(by="total", ascending=False)

# 按产品品类
product = df.groupby("product_line")[["total", "quantity"]].sum().reset_index().sort_values(by="total", ascending=False)

# 按性别
gender = df.groupby("gender")[["total", "quantity"]].sum().reset_index().sort_values(by="total", ascending=False)

# 按支付方式
payment = df.groupby("payment")[["total", "quantity"]].sum().reset_index().sort_values(by="total", ascending=False)

# Top 10 商品（按发票作为单品计）
top_products = df.sort_values(by="total", ascending=False).head(10)

# -------- 导出到多 sheet Excel --------

output_path = base / "sales_report.xlsx"
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    city.to_excel(writer, sheet_name="city", index=False)
    product.to_excel(writer, sheet_name="product", index=False)
    gender.to_excel(writer, sheet_name="gender", index=False)
    payment.to_excel(writer, sheet_name="payment", index=False)
    top_products.to_excel(writer, sheet_name="top_products", index=False)

print(f"[SUCCESS] 已生成完整报告：{output_path}")
