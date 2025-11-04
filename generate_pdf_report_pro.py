from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

base = Path(".").resolve()
pdf_path = base / "sales_report_pro.pdf"
csv_path = base / "sales_100.csv"

# 读数据
df = pd.read_csv(csv_path)

# 动态洞察
city_total = df.groupby("city")["total"].sum().sort_values(ascending=False)
top_city, top_city_val = city_total.index[0], float(city_total.iloc[0])

pl_total = df.groupby("product_line")["total"].sum().sort_values(ascending=False)
top_pl, top_pl_val = pl_total.index[0], float(pl_total.iloc[0])

gender_sum = df.groupby("gender")["total"].sum().sort_values(ascending=False)
top_gender, top_gender_val = gender_sum.index[0], float(gender_sum.iloc[0])
gender_share = top_gender_val / df["total"].sum()

pay_sum = df.groupby("payment")["total"].sum().sort_values(ascending=False)
top_pay, top_pay_val = pay_sum.index[0], float(pay_sum.iloc[0])

# 关键指标表（KPI）
kpi_data = [
    ["Metric", "Value"],
    ["Top City (Revenue)", f"{top_city}  |  {top_city_val:,.2f}"],
    ["Top Product Line",   f"{top_pl}  |  {top_pl_val:,.2f}"],
    ["Top Gender",         f"{top_gender}  |  {top_gender_val:,.2f} ({gender_share:.1%})"],
    ["Top Payment",        f"{top_pay}  |  {top_pay_val:,.2f}"],
    ["Total Revenue",      f"{df['total'].sum():,.2f}"],
    ["Total Rows",         f"{len(df)}"],
]

# 创建 PDF
c = canvas.Canvas(str(pdf_path), pagesize=letter)
w, h = letter

# 封面标题
c.setFont("Helvetica-Bold", 22)
c.drawString(70, h-80, "Sales Data Analysis Report")
c.setFont("Helvetica", 12)
c.drawString(70, h-105, "Source: sales_100.csv")
c.drawString(70, h-120, "Includes dynamic insights, KPI table, and charts")

# KPI 表格
table = Table(kpi_data, colWidths=[160, 360])
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.black),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("FONTNAME",   (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",   (0,0), (-1,-1), 10),
    ("ALIGN",      (0,0), (-1,-1), "LEFT"),
]))
# 把表绘制到页面
table.wrapOn(c, 70, h-300)
table.drawOn(c, 70, h-340)

# 洞察段落
y = h-370
c.setFont("Helvetica-Bold", 13)
c.drawString(70, y, "Highlights")
c.setFont("Helvetica", 11)
y -= 18
c.drawString(70, y, f"• Top city: {top_city} ({top_city_val:,.2f})")
y -= 14
c.drawString(70, y, f"• Best product line: {top_pl} ({top_pl_val:,.2f})")
y -= 14
c.drawString(70, y, f"• Leading gender: {top_gender} ({top_gender_val:,.2f}, {gender_share:.1%} of total)")
y -= 14
c.drawString(70, y, f"• Most revenue by payment: {top_pay} ({top_pay_val:,.2f})")

# 新页：插入四张图
c.showPage()
c.setFont("Helvetica-Bold", 16)
c.drawString(70, h-60, "Charts")

images = [
    ("city_revenue_chart.png",    "Total Revenue by City"),
    ("product_revenue_chart.png", "Total Revenue by Product Line"),
    ("gender_revenue_chart.png",  "Total Revenue by Gender"),
    ("payment_revenue_chart.png", "Total Revenue by Payment Method"),
]

y = h-100
for path, caption in images:
    img = base / path
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, y, caption)
    y -= 12
    if img.exists():
        # 宽 470、高 170 的占位
        c.drawImage(str(img), 70, y-170, width=470, height=170, preserveAspectRatio=True, anchor='n')
        y -= 190
    else:
        c.setFont("Helvetica", 11)
        c.drawString(70, y-12, f"(Missing image: {path})")
        y -= 40

c.showPage()
c.save()
print(f"[SUCCESS] PDF generated: {pdf_path}")
