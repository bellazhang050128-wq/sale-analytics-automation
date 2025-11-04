import pandas as pd
from pathlib import Path

base = Path(".").resolve()
data_path = base / "sales_100.csv"

print("[INFO] 读取数据...")
df = pd.read_csv(data_path)

print("\n[DEBUG] 前5行数据：")
print(df.head())

print("\n✅ 数据维度（行数, 列数）：")
print(df.shape)

print("\n✅ 字段信息：")
print(df.info())

print("\n✅ 数值字段描述性统计：")
print(df.describe())

print("\n✅ 空值数量：")
print(df.isna().sum())

import pandas as pd
from pathlib import Path

base = Path(".").resolve()
data_path = base / "sales_100.csv"
df = pd.read_csv(data_path)

# ✅ 每个城市总销售额
city_revenue = df.groupby("city")["total"].sum().reset_index()

# ✅ 排序：谁最赚钱？
city_revenue_sorted = city_revenue.sort_values(by="total", ascending=False)

print("\n✅ 按城市总销售额排名：")
print(city_revenue_sorted)

# ✅ 导出报表
city_revenue_sorted.to_csv("city_revenue.csv", index=False)
print("\n[SUCCESS] 已导出 city_revenue.csv")
import pandas as pd
from pathlib import Path

base = Path(".").resolve()
data_path = base / "sales_100.csv"
df = pd.read_csv(data_path)

# ✅ 每个商品品类的总收入 & 总销量
product_summary = df.groupby("product_line")[["total", "quantity"]].sum().reset_index()

# ✅ 排序（按 total 从大到小）
product_sorted = product_summary.sort_values(by="total", ascending=False)

print("\n✅ 商品品类销售额 & 销量排名：")
print(product_sorted)

# ✅ 导出报表
product_sorted.to_csv("product_revenue.csv", index=False)
print("\n[SUCCESS] 已导出 product_revenue.csv")


import pandas as pd
from pathlib import Path

base = Path(".").resolve()
data_path = base / "sales_100.csv"
df = pd.read_csv(data_path)

# ✅ 每个性别的总收入 & 总销量 & 平均单价
gender_summary = df.groupby("gender")[["total", "quantity", "unit_price"]].agg({
    "total": "sum",
    "quantity": "sum",
    "unit_price": "mean"
}).reset_index()

# ✅ 排序让输出更清晰
gender_sorted = gender_summary.sort_values(by="total", ascending=False)

print("\n✅ 男女消费对比：")
print(gender_sorted)

# ✅ 导出报表
gender_sorted.to_csv("gender_revenue.csv", index=False)
print("\n[SUCCESS] 已导出 gender_revenue.csv")

import pandas as pd
from pathlib import Path

base = Path(".").resolve()
data_path = base / "sales_100.csv"
df = pd.read_csv(data_path)

# ✅ 每种支付方式的总收入 & 总销量
payment_summary = df.groupby("payment")[["total", "quantity"]].sum().reset_index()

# ✅ 排序按总收入
payment_sorted = payment_summary.sort_values(by="total", ascending=False)

print("\n✅ 支付方式销售表现：")
print(payment_sorted)

# ✅ 导出报表
payment_sorted.to_csv("payment_revenue.csv", index=False)
print("\n[SUCCESS] 已导出 payment_revenue.csv")

