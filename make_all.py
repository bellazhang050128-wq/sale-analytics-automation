import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

base = Path(".").resolve()
csv = base / "sales_100.csv"

# 1) 读取
df = pd.read_csv(csv)

# 2) 图表 —— 城市
city_rev = df.groupby("city")["total"].sum().reset_index()
plt.bar(city_rev["city"], city_rev["total"])
plt.title("Total Revenue by City"); plt.xlabel("City"); plt.ylabel("Revenue"); plt.tight_layout()
plt.savefig("city_revenue_chart.png"); plt.close()

# 3) 图表 —— 产品线
pl_rev = df.groupby("product_line")["total"].sum().reset_index().sort_values(by="total")
plt.barh(pl_rev["product_line"], pl_rev["total"])
plt.title("Total Revenue by Product Line"); plt.xlabel("Revenue"); plt.ylabel("Product Line"); plt.tight_layout()
plt.savefig("product_revenue_chart.png"); plt.close()

# 4) 图表 —— 性别
gender_rev = df.groupby("gender")["total"].sum().reset_index()
plt.bar(gender_rev["gender"], gender_rev["total"])
plt.title("Total Revenue by Gender"); plt.xlabel("Gender"); plt.ylabel("Revenue"); plt.tight_layout()
plt.savefig("gender_revenue_chart.png"); plt.close()

# 5) 图表 —— 支付方式
pay_rev = df.groupby("payment")["total"].sum().reset_index()
plt.bar(pay_rev["payment"], pay_rev["total"])
plt.title("Total Revenue by Payment Method"); plt.xlabel("Payment"); plt.ylabel("Revenue"); plt.tight_layout()
plt.savefig("payment_revenue_chart.png"); plt.close()

# 6) 多 sheet Excel
city  = city_rev.sort_values("total", ascending=False)
product = df.groupby("product_line")[["total","quantity"]].sum().reset_index().sort_values("total", ascending=False)
gender = df.groupby("gender")[["total","quantity"]].sum().reset_index().sort_values("total", ascending=False)
payment = df.groupby("payment")[["total","quantity"]].sum().reset_index().sort_values("total", ascending=False)
top_products = df.sort_values("total", ascending=False).head(10)

with pd.ExcelWriter(base / "sales_report.xlsx", engine="openpyxl") as w:
    city.to_excel(w, "city", index=False)
    product.to_excel(w, "product", index=False)
    gender.to_excel(w, "gender", index=False)
    payment.to_excel(w, "payment", index=False)
    top_products.to_excel(w, "top_products", index=False)

# 7) PDF（简版，嵌图）
pdf_path = base / "sales_report.pdf"
c = canvas.Canvas(str(pdf_path), pagesize=letter)
w, h = letter
c.setFont("Helvetica-Bold", 20); c.drawString(70, h-80, "Sales Report (Auto Build)")
c.setFont("Helvetica", 12); c.drawString(70, h-105, "Charts and multi-sheet Excel exported")

y = h-140
for img in ["city_revenue_chart.png","product_revenue_chart.png","gender_revenue_chart.png","payment_revenue_chart.png"]:
    c.setFont("Helvetica-Bold", 12); c.drawString(70, y, img.replace("_"," ").replace(".png","").title())
    y -= 12
    p = base / img
    if p.exists():
        c.drawImage(str(p), 70, y-170, width=470, height=170, preserveAspectRatio=True, anchor='n')
        y -= 190
    else:
        c.setFont("Helvetica", 11); c.drawString(70, y-12, f"(Missing: {img})"); y -= 40

c.showPage(); c.save()
print("[SUCCESS] All artifacts updated: charts + sales_report.xlsx + sales_report.pdf")
