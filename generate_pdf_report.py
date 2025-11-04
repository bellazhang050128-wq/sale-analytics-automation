from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

# PDF 保存路径
base = Path(".").resolve()
pdf_path = base / "sales_report.pdf"

c = canvas.Canvas(str(pdf_path), pagesize=letter)
width, height = letter

# ------- 标题 -------
c.setFont("Helvetica-Bold", 20)
c.drawString(70, height - 80, "Sales Data Analysis Report")

c.setFont("Helvetica", 12)
c.drawString(70, height - 110, "Automatically generated from sales_100.csv")
c.drawString(70, height - 130, "Includes charts and business insights")

# ------- 插入图表 -------
images = [
    ("city_revenue_chart.png", "City Revenue Comparison"),
    ("product_revenue_chart.png", "Product Line Revenue"),
    ("gender_revenue_chart.png", "Gender Revenue Comparison"),
    ("payment_revenue_chart.png", "Payment Method Revenue"),
]

y = height - 180
for img_path, caption in images:
    img_file = base / img_path
    if img_file.exists():
        c.drawImage(str(img_file), 70, y - 160, width=450, height=150)
        c.drawString(70, y - 10, caption)
        y -= 200
    else:
        c.drawString(70, y, f"Missing image: {img_path}")
        y -= 40

# ------- 分析结论 -------
c.setFont("Helvetica-Bold", 14)
c.drawString(70, 120, "Insights:")
c.setFont("Helvetica", 12)
c.drawString(70, 100, "• Naypyitaw shows highest total revenue.")
c.drawString(70, 80, "• Food & Beverages is the best-performing product line.")
c.drawString(70, 60, "• Female customers spend more and buy more.");
c.drawString(70, 40, "• Credit card users contribute the most to sales.");

c.showPage()
c.save()

print(f"[SUCCESS] PDF 报告已生成：{pdf_path}")
