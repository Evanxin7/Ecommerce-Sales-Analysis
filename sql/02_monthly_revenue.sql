-- 1. 选择电商分析数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 按月份汇总销售指标 / Aggregate monthly sales metrics
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS sales_month,

    COUNT(DISTINCT InvoiceNo) AS total_orders,

    COUNT(DISTINCT DATE(InvoiceDate)) AS active_days,

    ROUND(SUM(Revenue), 2) AS total_revenue,

    ROUND(
        SUM(Revenue) /
        NULLIF(COUNT(DISTINCT DATE(InvoiceDate)), 0),
        2
    ) AS revenue_per_active_day,

    MIN(DATE(InvoiceDate)) AS first_transaction_date,

    MAX(DATE(InvoiceDate)) AS last_transaction_date

FROM sales

GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')

ORDER BY sales_month;
