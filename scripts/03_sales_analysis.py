from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. 设置项目文件路径 / Set project file paths
project_dir = Path(__file__).resolve().parent.parent

data_file = project_dir / "data" / "processed" / "cleaned_sales.csv"
figure_dir = project_dir / "reports" / "figures"

figure_dir.mkdir(parents=True, exist_ok=True)

# 2. 读取清洗后的数据 / Load cleaned sales data
df = pd.read_csv(
    data_file,
    dtype={"InvoiceNo": "string", "StockCode": "string"},
    parse_dates=["InvoiceDate"]
)

print("数据读取成功 / Dataset loaded")
print("交易明细数量 / Transaction rows:", len(df))

# 3. 计算总销售额 / Calculate total revenue
total_revenue = df["Revenue"].sum()

print("\n总销售额 / Total Revenue")
print(f"£{total_revenue:,.2f}")

# 4. 计算订单数量 / Count unique orders
total_orders = df["InvoiceNo"].nunique()

print("\n订单数量 / Total Orders")
print(f"{total_orders:,}")

# 5. 计算每笔订单的平均金额 / Calculate average order value
average_order_value = total_revenue / total_orders

print("\n平均订单金额 / Average Order Value")
print(f"£{average_order_value:,.2f}")

# 6. 分析销售额最高的商品 / Identify top products by revenue
top_products = (
    df.groupby(["StockCode", "Description"])["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n销售额最高的10款商品 / Top 10 Products")
print(top_products.to_string())

# 7. 按月份汇总销售额 / Aggregate monthly revenue
df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\n月度销售额 / Monthly Revenue")
print(monthly_revenue.to_string())

# 8. 创建月度销售趋势图 / Create monthly revenue chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue.index.astype(str),
    monthly_revenue.values,
    marker="o",
    linewidth=2
)

# 9. 设置图表格式 / Format chart labels
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

# 10. 保存图表 / Save revenue chart
figure_path = figure_dir / "monthly_revenue.png"

plt.savefig(figure_path, dpi=300, bbox_inches="tight")
plt.close()

print("\n图表已保存 / Chart saved")
print(figure_path)

print("\n销售分析完成 / Sales analysis completed")


# 11. 检查数据覆盖时间 / Check dataset date coverage
print("\n数据时间范围 / Date Coverage")
print("开始时间 / Start:", df["InvoiceDate"].min())
print("结束时间 / End:", df["InvoiceDate"].max())

# 12. 检查每个月的交易日期 / Check active trading days by month
monthly_coverage = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["InvoiceDate"]
    .agg(
        FirstDate="min",
        LastDate="max",
        ActiveDays=lambda x: x.dt.normalize().nunique()
    )
)

print("\n每月数据覆盖情况 / Monthly Coverage")
print(monthly_coverage.to_string())

# 13. 查找销售额最高的交易明细 / Identify largest transactions
largest_transactions = df.nlargest(10, "Revenue")[
    [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "Revenue"
    ]
]

print("\n销售额最高的10条明细 / Largest Transactions")
print(largest_transactions.to_string(index=False))
