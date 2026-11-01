
-- 1. 选择项目数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 创建客户分层视图 / Create customer segmentation view
CREATE OR REPLACE VIEW rfm_segment_summary AS

WITH customer_metrics AS (
    SELECT
        CustomerID,

        DATEDIFF(
            '2011-12-10',
            MAX(DATE(InvoiceDate))
        ) AS recency_days,

        COUNT(DISTINCT InvoiceNo) AS frequency,

        ROUND(SUM(Revenue), 2) AS monetary

    FROM sales
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
),

-- 3. 计算客户 RFM 分数 / Assign tie-aware RFM scores
rfm_scores AS (
    SELECT
        CustomerID,
        recency_days,
        frequency,
        monetary,

        LEAST(
            5,
            FLOOR(
                PERCENT_RANK() OVER (
                    ORDER BY recency_days DESC
                ) * 5
            ) + 1
        ) AS r_score,

        LEAST(
            5,
            FLOOR(
                PERCENT_RANK() OVER (
                    ORDER BY frequency ASC
                ) * 5
            ) + 1
        ) AS f_score,

        LEAST(
            5,
            FLOOR(
                PERCENT_RANK() OVER (
                    ORDER BY monetary ASC
                ) * 5
            ) + 1
        ) AS m_score

    FROM customer_metrics
),

-- 4. 根据客户行为进行分层 / Segment customers by behavior
rfm_segments AS (
    SELECT
        CustomerID,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,

        CASE
            WHEN r_score >= 4
                 AND f_score >= 4
                 AND m_score >= 4
                THEN 'High-value active'

            WHEN r_score <= 2
                 AND m_score >= 4
                THEN 'High-spend not recent'

            WHEN r_score >= 3
                 AND f_score >= 3
                THEN 'Active repeat'

            WHEN r_score >= 4
                 AND frequency = 1
                THEN 'Recent one-order'

            ELSE 'Other'
        END AS customer_segment

    FROM rfm_scores
)

-- 5. 汇总客户分层结果 / Summarize customer segments
SELECT
    customer_segment,

    COUNT(*) AS customer_count,

    ROUND(
        COUNT(*) * 100.0 /
        NULLIF((SELECT COUNT(*) FROM rfm_segments), 0),
        2
    ) AS customer_share_pct,

    ROUND(SUM(monetary), 2) AS total_spend,

    ROUND(AVG(monetary), 2) AS average_spend

FROM rfm_segments
GROUP BY customer_segment
ORDER BY customer_count DESC;
