from pathlib import Path
import pandas as pd

# 1. 设置数据路径 / Set dataset path
project_dir = Path(__file__).resolve().parent.parent
data_file = project_dir / "data" / "processed" / "cleaned_sales.csv"

# 2. 读取数据 / Load cleaned sales data
df = pd.read_csv(
    data_file,
    dtype={"InvoiceNo": "string", "StockCode": "string"}
)

# 3. 排除已识别的非商品项目 / Exclude known non-product codes
non_product_codes = {
    "POST", "DOT", "M", "AMAZONFEE",
    "BANK CHARGES", "B", "D", "CRUK", "C2"
}

product_df = df.loc[
    ~df["StockCode"].isin(non_product_codes)
].copy()

# 4. 找出金额最大的交易明细 / Identify largest transaction line
largest_index = product_df["Revenue"].idxmax()
largest_row = product_df.loc[largest_index]

print("最大交易明细 / Largest Transaction")
print(largest_row[
    ["InvoiceNo", "StockCode", "Description",
     "Quantity", "UnitPrice", "Revenue"]
].to_string())

# 5. 计算原始商品销售额排名 / Calculate original product ranking
original_ranking = (
    product_df.groupby("StockCode")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# 6. 暂时排除最大交易明细 / Temporarily exclude largest transaction
adjusted_df = product_df.drop(index=largest_index)

adjusted_ranking = (
    adjusted_df.groupby("StockCode")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# 7. 比较两种情况下的前五名 / Compare top five products
print("\n原始前五名 / Original Top Five")
print(original_ranking.head(5).to_string())

print("\n排除最大明细后的前五名 / Adjusted Top Five")
print(adjusted_ranking.head(5).to_string())

# 8. 检查最大交易对所属商品的影响 / Measure impact on its product
product_code = largest_row["StockCode"]
original_revenue = original_ranking.loc[product_code]
adjusted_revenue = adjusted_ranking.get(product_code, 0)

impact_percentage = largest_row["Revenue"] / original_revenue * 100

print("\n单笔交易影响 / Single Transaction Impact")
print("商品编码 / Stock Code:", product_code)
print(f"原始商品销售额 / Original Revenue: £{original_revenue:,.2f}")
print(f"调整后销售额 / Adjusted Revenue: £{adjusted_revenue:,.2f}")
print(f"最大明细贡献占比 / Contribution: {impact_percentage:.2f}%")

print("\n敏感性分析完成 / Sensitivity analysis completed")
