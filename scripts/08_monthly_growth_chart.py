
from pathlib import Path
from getpass import getpass

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 1. 设置项目路径 / Set project paths
project_dir = Path(__file__).resolve().parent.parent
figure_dir = project_dir / "reports" / "figures"

figure_dir.mkdir(parents=True, exist_ok=True)

# 2. 配置数据库连接 / Configure MySQL connection
password = getpass("请输入 MySQL 密码 / MySQL Password: ")

database_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="127.0.0.1",
    port=3306,
    database="ecommerce_analysis"
)

engine = create_engine(database_url)

# 3. 使用 SQL 计算月度环比 / Calculate monthly growth using SQL
query = text("""
WITH monthly_sales AS (
    SELECT
        EXTRACT(YEAR_MONTH FROM InvoiceDate) AS sales_month,
        SUM(Revenue) AS total_revenue
    FROM sales
    WHERE InvoiceDate >= '2011-01-01'
      AND InvoiceDate < '2011-12-01'
    GROUP BY EXTRACT(YEAR_MONTH FROM InvoiceDate)
),
monthly_comparison AS (
    SELECT
        sales_month,
        total_revenue,
        LAG(total_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_revenue
    FROM monthly_sales
)
SELECT
    sales_month,
    ROUND(
        (total_revenue - previous_revenue)
        / NULLIF(previous_revenue, 0) * 100,
        2
    ) AS mom_growth_pct
FROM monthly_comparison
ORDER BY sales_month
""")

# 4. 读取 SQL 查询结果 / Load SQL query results
with engine.connect() as connection:
    df = pd.read_sql_query(query, connection)

engine.dispose()

# 5. 处理日期与缺失值 / Prepare dates and missing values
df = df.dropna(subset=["mom_growth_pct"]).copy()

df["sales_month"] = pd.to_datetime(
    df["sales_month"].astype(str),
    format="%Y%m"
).dt.strftime("%Y-%m")

df["mom_growth_pct"] = df["mom_growth_pct"].astype(float)

print("月度环比数据 / Monthly Growth")
print(df.to_string(index=False))

# 6. 根据增长方向设置颜色 / Color bars by growth direction
colors = [
    "#3B82F6" if value >= 0 else "#EF4444"
    for value in df["mom_growth_pct"]
]

# 7. 绘制环比增长率柱状图 / Plot monthly growth chart
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    df["sales_month"],
    df["mom_growth_pct"],
    color=colors
)

# 8. 设置图表标题和坐标轴 / Format chart labels
ax.set_title("Monthly Revenue Growth Rate")
ax.set_xlabel("Month")
ax.set_ylabel("Month-over-Month Growth (%)")

ax.axhline(y=0, color="gray", linewidth=1)

ax.bar_label(
    bars,
    fmt="%.1f%%",
    padding=4,
    fontsize=9
)

ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)
ax.margins(y=0.2)

plt.xticks(rotation=45)
plt.tight_layout()

# 9. 保存图表 / Save monthly growth chart
figure_path = figure_dir / "monthly_growth.png"

plt.savefig(
    figure_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n图表已保存 / Chart saved")
print(figure_path)
