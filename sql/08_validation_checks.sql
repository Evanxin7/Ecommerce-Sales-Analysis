-- 1. 选择项目数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 统计客户订单次数 / Calculate customer order counts
WITH customer_orders AS (
    SELECT
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS order_count
    FROM sales
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
),

-- 3. 汇总待验证指标 / Collect validation metrics
validation_metrics AS (
    SELECT
        (SELECT COUNT(*) FROM sales) AS total_rows,

        (SELECT COUNT(DISTINCT InvoiceNo)
         FROM sales) AS total_orders,

        (SELECT ROUND(SUM(Revenue), 2)
         FROM sales) AS total_revenue,

        (SELECT COUNT(*)
         FROM customer_orders) AS total_customers,

        (SELECT COUNT(*)
         FROM customer_orders
         WHERE order_count >= 2) AS repeat_customers,

        (SELECT SUM(customer_count)
         FROM rfm_segment_summary) AS rfm_customers
)

-- 4. 自动检查业务指标 / Validate business metrics
SELECT
    total_rows,
    total_orders,
    total_revenue,
    total_customers,
    repeat_customers,
    rfm_customers,

    CASE
        WHEN total_rows = 524878
         AND total_orders = 19960
         AND total_revenue = 10642110.80
         AND total_customers = 4338
         AND repeat_customers = 2845
         AND rfm_customers = 4338
        THEN 'PASS'
        ELSE 'CHECK'
    END AS validation_status

FROM validation_metrics;
