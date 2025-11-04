import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base = Path(".").resolve()
df = pd.read_csv(base / "sales_100.csv")

payment_revenue = df.groupby("payment")["total"].sum().reset_index()

plt.bar(payment_revenue["payment"], payment_revenue["total"])
plt.title("Total Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue")
plt.tight_layout()

plt.savefig("payment_revenue_chart.png")
plt.show()

print("[SUCCESS] 支付方式柱状图已生成：payment_revenue_chart.png")
