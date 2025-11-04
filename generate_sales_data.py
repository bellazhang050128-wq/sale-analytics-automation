import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import datetime, timedelta

# 数据字段可选内容
branches = ['A', 'B', 'C']
cities = ['Yangon', 'Mandalay', 'Naypyitaw']
customer_types = ['Member', 'Normal']
genders = ['Male', 'Female']
product_lines = [
    'Electronic accessories', 'Fashion accessories', 'Home and lifestyle',
    'Sports and travel', 'Health and beauty', 'Food and beverages'
]
payments = ['cash', 'credit card', 'e-wallet']

# 自动生成日期函数
def random_date():
    start = datetime(2019, 1, 1)
    end = datetime(2019, 3, 31)
    delta = end - start
    days = random.randint(0, delta.days)
    return (start + timedelta(days=days)).strftime("%Y-%m-%d")

# 生成100行数据
data = []
for _ in range(100):
    unit_price = round(random.uniform(5, 100), 2)
    quantity = random.randint(1, 10)
    total = round(unit_price * quantity, 2)

    row = {
        "invoice_id": f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}",
        "branch": random.choice(branches),
        "city": random.choice(cities),
        "customer_type": random.choice(customer_types),
        "gender": random.choice(genders),
        "product_line": random.choice(product_lines),
        "unit_price": unit_price,
        "quantity": quantity,
        "total": total,
        "date": random_date(),
        "payment": random.choice(payments)
    }
    data.append(row)

# 转为DataFrame
df = pd.DataFrame(data)

# 保存路径（当前目录）
base = Path(".").resolve()
output = base / "sales_100.csv"

df.to_csv(output, index=False)

print(f"[SUCCESS] 已生成 100 行销售数据：{output}")
print(df.head())
