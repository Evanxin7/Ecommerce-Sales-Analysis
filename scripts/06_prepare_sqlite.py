
from pathlib import Path
import sqlite3
import pandas as pd

# 1. 设置项目路径 / Set project paths
project_dir = Path(__file__).resolve().parent.parent

csv_file = project_dir / "data" / "processed" / "cleaned_sales.csv"
db_file = project_dir / "data" / "processed" / "retail.sqlite"

# 2. 读取清洗后的数据 / Load cleaned sales data
df = pd.read_csv(
    csv_file,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string"
    },
    parse_dates=["InvoiceDate"]
)

print("数据读取成功 / Dataset loaded")
print("记录数量 / Rows:", len(df))

# 3. 连接 SQLite 数据库 / Connect to SQLite database
with sqlite3.connect(db_file) as conn:

    # 4. 导入销售数据表 / Import sales data into SQL table
    df.to_sql(
        "sales",
        conn,
        if_exists="replace",
        index=False,
        chunksize=5000
    )

    # 5. 创建订单编号索引 / Create invoice number index
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_invoice "
        "ON sales (InvoiceNo)"
    )

    # 6. 验证数据库记录数 / Verify database row count
    result = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()

    print("\n数据库验证 / Database Verification")
    print("数据库记录数 / SQL Rows:", result[0])

print("\n数据库已创建 / Database created")
print(db_file)
