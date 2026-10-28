
from pathlib import Path
import pandas as pd

# 1. 设置项目路径 / Set project paths
project_dir = Path(__file__).resolve().parent.parent

raw_file = project_dir / "data" / "raw" / "Online Retail.xlsx"
output_dir = project_dir / "data" / "processed"
output_file = output_dir / "cleaned_sales.csv"

# 2. 创建输出文件夹 / Create output directory
output_dir.mkdir(parents=True, exist_ok=True)

# 3. 读取原始数据 / Load raw transaction data
print("正在读取数据 / Loading dataset")

df = pd.read_excel(raw_file, engine="openpyxl")

print("原始记录数 / Original rows:", len(df))

# 4. 删除完全重复的记录 / Remove exact duplicate rows
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates().copy()

print("删除重复记录 / Duplicates removed:", duplicate_count)

# 5. 排除取消订单 / Exclude cancelled invoices
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

cancelled_count = cancelled.sum()
df = df.loc[~cancelled].copy()

print("排除取消订单明细 / Cancelled rows:", cancelled_count)

# 6. 排除非正数商品数量 / Exclude non-positive quantities
invalid_quantity = (df["Quantity"] <= 0).sum()

df = df.loc[df["Quantity"] > 0].copy()

print("排除异常数量 / Invalid quantities:", invalid_quantity)

# 7. 排除非正数商品价格 / Exclude non-positive prices
invalid_price = (df["UnitPrice"] <= 0).sum()

df = df.loc[df["UnitPrice"] > 0].copy()

print("排除异常价格 / Invalid prices:", invalid_price)

# 8. 排除缺少商品描述的记录 / Exclude missing product descriptions
missing_description = df["Description"].isna().sum()

df = df.dropna(subset=["Description"]).copy()

print(
    "排除缺失商品描述 / Missing descriptions:",
    missing_description
)

# 9. 标准化字段类型 / Standardize column types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Description"] = df["Description"].str.strip()

# 10. 计算交易明细销售额 / Calculate line-item revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# 11. 提取交易日期 / Extract transaction date
df["OrderDate"] = df["InvoiceDate"].dt.date

# 12. 检查清洗结果 / Validate cleaned data
print("\n清洗结果 / Cleaning Results")
print("清洗后记录数 / Cleaned rows:", len(df))
print("剩余缺失值 / Missing values:")
print(df.isna().sum())

print("\n销售额统计 / Revenue Statistics")
print(df["Revenue"].describe())

# 13. 保存清洗后的数据 / Export cleaned dataset
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\n数据已保存 / Dataset saved")
print(output_file)
