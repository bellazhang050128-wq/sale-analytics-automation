import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base = Path(".").resolve()
df = pd.read_csv(base / "sales_100.csv")

product_revenue = df.groupby("product_line")["total"].sum().reset_index()
product_revenue = product_revenue.sort_values(by="total")

plt.barh(product_revenue["product_line"], product_revenue["total"])
plt.title("Total Revenue by Product Line")
plt.xlabel("Revenue")
plt.ylabel("Product Line")
plt.tight_layout()

plt.savefig("product_revenue_chart.png")
plt.show()

print("[SUCCESS] 商品品类图已生成：product_revenue_chart.png")
