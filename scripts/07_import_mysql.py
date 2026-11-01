
from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.types import (
    VARCHAR,
    Integer,
    BigInteger,
    DateTime,
    Date,
    DECIMAL
)

# 1. 设置项目数据路径 / Set project data path
project_dir = Path(__file__).resolve().parent.parent

csv_file = (
    project_dir
    / "data"
    / "processed"
    / "cleaned_sales.csv"
)

# 2. 读取清洗后的数据 / Load cleaned sales data
df = pd.read_csv(
    csv_file,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string"
    },
    parse_dates=["InvoiceDate"]
)

# 3. 规范日期与客户编号 / Standardize dates and customer IDs
df["OrderDate"] = pd.to_datetime(
    df["OrderDate"]
).dt.date

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"],
    errors="coerce"
).astype("Int64")

print("数据读取成功 / Dataset loaded")
print("待导入记录数 / Rows to import:", len(df))

# 4. 安全输入数据库密码 / Securely enter database password
password = getpass(
    "请输入 MySQL 密码 / MySQL Password: "
)

# 5. 配置 MySQL 连接 / Configure MySQL connection
database_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="127.0.0.1",
    port=3306,
    database="ecommerce_analysis"
)

engine = create_engine(
    database_url,
    pool_pre_ping=True
)

# 6. 定义数据库字段类型 / Define SQL column types
column_types = {
    "InvoiceNo": VARCHAR(20),
    "StockCode": VARCHAR(30),
    "Description": VARCHAR(255),
    "Quantity": Integer(),
    "InvoiceDate": DateTime(),
    "UnitPrice": DECIMAL(12, 4),
    "CustomerID": BigInteger(),
    "Country": VARCHAR(100),
    "Revenue": DECIMAL(18, 4),
    "OrderDate": Date()
}

# 7. 批量导入 MySQL / Import data into MySQL in batches
print("\n开始导入数据 / Starting MySQL import")

with engine.begin() as connection:
    df.to_sql(
        name="sales",
        con=connection,
        if_exists="fail",
        index=False,
        chunksize=2000,
        dtype=column_types
    )

# 8. 验证导入记录数 / Verify imported row count
with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM sales")
    ).scalar_one()

print("\n数据库验证 / Database Verification")
print("CSV 记录数 / CSV Rows:", len(df))
print("MySQL 记录数 / MySQL Rows:", result)

# 9. 检查数据完整性 / Validate data integrity
if result == len(df):
    print("数据导入成功 / Import successful")
else:
    print("记录数不一致 / Row count mismatch")

# 10. 释放数据库连接 / Dispose database engine
engine.dispose()
