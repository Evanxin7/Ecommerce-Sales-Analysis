
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 1. 设置文件路径 / Set project file paths
project_dir = Path(__file__).resolve().parent.parent

data_file = project_dir / "data" / "processed" / "cleaned_sales.csv"
figure_dir = project_dir / "reports" / "figures"
table_dir = project_dir / "reports" / "tables"

figure_dir.mkdir(parents=True, exist_ok=True)
table_dir.mkdir(parents=True, exist_ok=True)

# 2. 读取清洗后的数据 / Load cleaned sales data
df = pd.read_csv(
    data_file,
    dtype={"StockCode": "string", "InvoiceNo": "string"}
)

print("数据读取成功 / Dataset loaded")
print("原始明细数量 / Input rows:", len(df))

# 3. 定义非商品项目编码 / Define non-product item codes
non_product_codes = {
    "POST",
    "DOT",
    "M",
    "AMAZONFEE",
    "BANK CHARGES",
    "B",
    "D",
    "CRUK",
    "C2"
}

# 4. 排除已识别的非商品项目 / Exclude identified non-product items
product_df = df.loc[
    ~df["StockCode"].isin(non_product_codes)
].copy()

print(
    "商品明细数量 / Product rows:",
    len(product_df)
)

print(
    "排除的非商品明细 / Excluded rows:",
    len(df) - len(product_df)
)

# 5. 按商品编码汇总销售额 / Aggregate revenue by product code
product_summary = (
    product_df.groupby("StockCode", as_index=False)
    .agg(
        Description=(
            "Description",
            lambda x: x.mode().iloc[0]
        ),
        Units=("Quantity", "sum"),
        Revenue=("Revenue", "sum")
    )
)

# 6. 选取销售额最高的10款商品 / Select top 10 products
top_products = (
    product_summary.sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
    .copy()
)

print("\n商品销售额排行榜 / Top 10 Products")
print(top_products.to_string(index=False))

# 7. 保存商品排行榜数据 / Export product ranking
output_file = table_dir / "top_10_products.csv"

top_products.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

# 8. 设置图表显示名称 / Prepare readable chart labels
chart_data = top_products.sort_values("Revenue").copy()

chart_data["Label"] = (
    chart_data["StockCode"].astype(str)
    + " | "
    + chart_data["Description"].str.slice(0, 32)
)

# 9. 绘制商品销售额排行榜 / Plot product revenue ranking
fig, ax = plt.subplots(figsize=(12, 7))

ax.barh(
    chart_data["Label"],
    chart_data["Revenue"],
    color="#4878A8"
)

ax.set_title("Top 10 Products by Revenue")
ax.set_xlabel("Revenue (GBP)")
ax.set_ylabel("Product")

ax.xaxis.set_major_formatter(
    FuncFormatter(lambda value, pos: f"£{value:,.0f}")
)

ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()

# 10. 保存排行榜图表 / Save product ranking chart
figure_path = figure_dir / "top_10_products.png"

plt.savefig(
    figure_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n排行榜已保存 / Ranking saved")
print(output_file)

print("\n图表已保存 / Chart saved")
print(figure_path)

print("\n商品分析完成 / Product analysis completed")
