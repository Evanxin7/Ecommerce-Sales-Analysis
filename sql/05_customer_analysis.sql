-- 1. 选择电商分析数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 检查客户编号完整性 / Check customer ID completeness
SELECT
    COUNT(*) AS total_rows,

    SUM(
        CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END
    ) AS missing_customer_rows,

    SUM(
        CASE WHEN CustomerID IS NOT NULL THEN 1 ELSE 0 END
    ) AS identified_customer_rows

FROM sales;

-- 3. 汇总客户购买情况 / Aggregate customer purchase behavior
WITH customer_summary AS (
    SELECT
        CustomerID,

        COUNT(DISTINCT InvoiceNo) AS order_count,

        ROUND(SUM(Revenue), 2) AS total_spend,

        MIN(InvoiceDate) AS first_purchase,

        MAX(InvoiceDate) AS last_purchase

    FROM sales

    WHERE CustomerID IS NOT NULL

    GROUP BY CustomerID
)

-- 4. 计算客户复购指标 / Calculate repeat purchase metrics
SELECT
    COUNT(*) AS total_customers,

    SUM(
        CASE WHEN order_count >= 2 THEN 1 ELSE 0 END
    ) AS repeat_customers,

    ROUND(
        SUM(
            CASE WHEN order_count >= 2 THEN 1 ELSE 0 END
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_rate_pct,

    ROUND(AVG(order_count), 2) AS average_orders_per_customer,

    ROUND(AVG(total_spend), 2) AS average_customer_spend

FROM customer_summary;

-- 5. 汇总每位客户的消费指标 / Summarize individual customers
WITH customer_summary AS (
    SELECT
        CustomerID,

        COUNT(DISTINCT InvoiceNo) AS order_count,

        ROUND(SUM(Revenue), 2) AS total_spend,

        MIN(InvoiceDate) AS first_purchase,

        MAX(InvoiceDate) AS last_purchase

    FROM sales

    WHERE CustomerID IS NOT NULL

    GROUP BY CustomerID
)

-- 6. 查找消费金额最高的10位客户 / Find top 10 customers by spending
SELECT
    CustomerID,
    order_count,
    total_spend,

    ROUND(
        total_spend / NULLIF(order_count, 0),
        2
    ) AS average_order_value,

    first_purchase,
    last_purchase

FROM customer_summary

ORDER BY total_spend DESC, CustomerID ASC

LIMIT 10;
