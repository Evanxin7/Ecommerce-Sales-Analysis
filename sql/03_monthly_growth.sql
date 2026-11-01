
-- 1. 选择电商分析数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 汇总月度销售数据 / Aggregate monthly sales data
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(InvoiceDate, '%Y-%m') AS sales_month,
        COUNT(DISTINCT InvoiceNo) AS total_orders,
        COUNT(DISTINCT DATE(InvoiceDate)) AS active_days,
        SUM(Revenue) AS total_revenue
    FROM sales
    WHERE InvoiceDate >= '2011-01-01'
      AND InvoiceDate < '2011-12-01'
    GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
),

-- 3. 获取上个月销售额 / Retrieve previous month's revenue
monthly_comparison AS (
    SELECT
        sales_month,
        total_orders,
        active_days,
        total_revenue,
        LAG(total_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales
)

-- 4. 计算环比增长率 / Calculate month-over-month growth
SELECT
    sales_month,
    total_orders,
    active_days,

    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(
        previous_month_revenue, 2
    ) AS previous_month_revenue,

    ROUND(
        (
            total_revenue - previous_month_revenue
        ) / NULLIF(previous_month_revenue, 0) * 100,
        2
    ) AS mom_growth_pct

FROM monthly_comparison
ORDER BY sales_month;
