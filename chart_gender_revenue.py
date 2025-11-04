import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base = Path(".").resolve()
df = pd.read_csv(base / "sales_100.csv")

gender_revenue = df.groupby("gender")["total"].sum().reset_index()

plt.bar(gender_revenue["gender"], gender_revenue["total"], color=["pink", "blue"])
plt.title("Total Revenue by Gender")
plt.xlabel("Gender")
plt.ylabel("Revenue")
plt.tight_layout()

plt.savefig("gender_revenue_chart.png")
plt.show()

print("[SUCCESS] 性别对比图已生成：gender_revenue_chart.png")
