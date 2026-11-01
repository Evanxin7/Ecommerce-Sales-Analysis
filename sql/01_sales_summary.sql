
-- 1. 选择电商分析数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 统计交易明细数量 / Count transaction lines
SELECT
    COUNT(*) AS total_rows
FROM sales;

-- 3. 统计独立订单数量 / Count unique orders
SELECT
    COUNT(DISTINCT InvoiceNo) AS total_orders
FROM sales;

-- 4. 计算销售额 / Calculate total revenue
SELECT
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM sales;

-- 5. 计算平均订单金额 / Calculate average order value
SELECT
    ROUND(
        SUM(Revenue) / NULLIF(COUNT(DISTINCT InvoiceNo), 0),
        2
    ) AS average_order_value
FROM sales;

-- 6. 汇总核心业务指标 / Summarize key business metrics
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(
        SUM(Revenue) / NULLIF(COUNT(DISTINCT InvoiceNo), 0),
        2
    ) AS average_order_value
FROM sales;

