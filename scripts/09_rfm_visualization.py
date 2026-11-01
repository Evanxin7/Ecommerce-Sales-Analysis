from pathlib import Path
from getpass import getpass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 1. 设置项目路径 / Set project paths
project_dir = Path(__file__).resolve().parent.parent
figure_dir = project_dir / "reports" / "figures"
figure_dir.mkdir(parents=True, exist_ok=True)

# 2. 连接 MySQL 数据库 / Connect to MySQL
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

# 3. 读取客户分层视图 / Load customer segmentation view
query = text("""
    SELECT
        customer_segment,
        customer_count,
        customer_share_pct,
        total_spend
    FROM rfm_segment_summary
""")

try:
    with engine.connect() as connection:
        df = pd.read_sql_query(query, connection)
finally:
    engine.dispose()

# 4. 检查客户数量 / Validate customer count
total_customers = int(df["customer_count"].sum())

print("客户总数 / Total Customers:", total_customers)

if total_customers != 4338:
    raise ValueError("客户总数与此前分析结果不一致")

# 5. 计算消费贡献占比 / Calculate revenue contribution
df["customer_share_pct"] = df["customer_share_pct"].astype(float)
df["total_spend"] = df["total_spend"].astype(float)

df["revenue_share_pct"] = (
    df["total_spend"] / df["total_spend"].sum() * 100
)

df = df.sort_values("customer_count")

print("\n客户分层结果 / Customer Segmentation")
print(df.to_string(index=False))

# 6. 设置柱状图位置 / Prepare bar positions
positions = np.arange(len(df))
bar_height = 0.35

fig, ax = plt.subplots(figsize=(12, 7))

# 7. 绘制客户人数占比 / Plot customer share
bars_customers = ax.barh(
    positions - bar_height / 2,
    df["customer_share_pct"],
    height=bar_height,
    label="Customer Share",
    color="#3B82F6"
)

# 8. 绘制销售额贡献占比 / Plot revenue share
bars_revenue = ax.barh(
    positions + bar_height / 2,
    df["revenue_share_pct"],
    height=bar_height,
    label="Revenue Share",
    color="#F59E0B"
)

# 9. 设置图表格式 / Format chart
ax.set_yticks(positions)
ax.set_yticklabels(df["customer_segment"])

ax.set_title("RFM Customer Segmentation")
ax.set_xlabel("Share (%)")
ax.set_ylabel("Customer Segment")

ax.bar_label(bars_customers, fmt="%.1f%%", padding=3)
ax.bar_label(bars_revenue, fmt="%.1f%%", padding=3)

ax.set_xlim(
    0,
    max(
        df["customer_share_pct"].max(),
        df["revenue_share_pct"].max()
    ) * 1.2
)

ax.legend()
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()

# 10. 保存客户分层图表 / Save segmentation chart
figure_path = figure_dir / "rfm_segmentation.png"

plt.savefig(
    figure_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n图表已保存 / Chart saved")
print(figure_path)
