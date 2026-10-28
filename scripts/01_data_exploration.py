from pathlib import Path
import pandas as pd

# 1. 定位原始数据文件 / Locate the raw dataset
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw" / "Online Retail.xlsx"

# 2. 读取 Excel 数据 / Load the Excel dataset
print("正在读取数据 / Loading dataset")
df = pd.read_excel(file_path, engine="openpyxl")

# 3. 查看数据规模 / Check dataset dimensions
print("\n数据规模 / Dataset Shape")
print("总行数 / Rows:", df.shape[0])
print("总列数 / Columns:", df.shape[1])

# 4. 查看前五条记录 / Preview the first five records
print("\n前五条记录 / First Five Rows")
print(df.head().to_string(index=False))

# 5. 查看字段名称 / Display column names
print("\n字段名称 / Column Names")
print(df.columns.tolist())

# 6. 检查缺失值 / Check missing values
print("\n缺失值统计 / Missing Values")
print(df.isnull().sum())

# 7. 检查重复记录 / Check duplicate records
print("\n重复记录 / Duplicate Records")
print("重复行数 / Duplicates:", df.duplicated().sum())

# 8. 检查取消订单 / Check cancelled invoices
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

print("\n取消订单 / Cancelled Invoices")
print("取消订单明细行数 / Cancelled Rows:", cancelled.sum())

# 9. 检查非正数商品数量 / Check non-positive quantities
print("\n商品数量检查 / Quantity Check")
print(
    "数量小于等于零 / Quantity <= 0:",
    (df["Quantity"] <= 0).sum()
)

# 10. 检查非正数商品价格 / Check non-positive prices
print("\n商品价格检查 / Price Check")
print(
    "价格小于等于零 / UnitPrice <= 0:",
    (df["UnitPrice"] <= 0).sum()
)

# 11. 查看数值统计信息 / Review numerical statistics
print("\n数值统计 / Numerical Statistics")
print(df[["Quantity", "UnitPrice"]].describe())

print("\n数据质量检查完成 / Data quality inspection completed")
