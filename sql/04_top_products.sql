-- 1. 选择项目数据库 / Select project database
USE ecommerce_analysis;

-- 2. 按区分大小写的商品编码汇总 / Aggregate by case-sensitive product codes
WITH product_sales AS (
    SELECT
        StockCode COLLATE utf8mb4_0900_bin AS product_code,

        MAX(Description) AS product_description,

        SUM(Quantity) AS total_units,

        COUNT(DISTINCT InvoiceNo) AS total_orders,

        ROUND(SUM(Revenue), 2) AS total_revenue

    FROM sales

    -- 3. 排除已知非商品项目 / Exclude known non-product items
    WHERE StockCode COLLATE utf8mb4_0900_bin NOT IN (
        'POST',
        'DOT',
        'M',
        'AMAZONFEE',
        'BANK CHARGES',
        'B',
        'D',
        'CRUK',
        'C2'
    )

    GROUP BY StockCode COLLATE utf8mb4_0900_bin
)

-- 4. 查询销售额最高的10款商品 / Retrieve top 10 products by revenue
SELECT
    product_code AS StockCode,
    product_description AS Description,
    total_units,
    total_orders,
    total_revenue

FROM product_sales

ORDER BY total_revenue DESC, product_code ASC

LIMIT 10;
