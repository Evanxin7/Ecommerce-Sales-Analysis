-- 1. 选择项目数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 汇总每位客户的 RFM 指标 / Calculate customer RFM metrics
WITH customer_rfm AS (
    SELECT
        CustomerID,

        -- 计算最近购买间隔 / Calculate recency in days
        DATEDIFF(
            (
                SELECT DATE_ADD(
                    MAX(DATE(InvoiceDate)),
                    INTERVAL 1 DAY
                )
                FROM sales
            ),
            MAX(DATE(InvoiceDate))
        ) AS recency_days,

        -- 统计独立订单数量 / Count unique orders
        COUNT(DISTINCT InvoiceNo) AS frequency,

        -- 汇总客户消费金额 / Sum customer spending
        ROUND(SUM(Revenue), 2) AS monetary

    FROM sales
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
),

-- 3. 将客户划分为五个评分等级 / Assign five RFM score groups
rfm_scores AS (
    SELECT
        CustomerID,
        recency_days,
        frequency,
        monetary,

        -- 最近购买越近，R 分数越高 / More recent purchases score higher
        6 - NTILE(5) OVER (
            ORDER BY recency_days ASC, CustomerID
        ) AS r_score,

        -- 购买频率越高，F 分数越高 / Higher frequency scores higher
        NTILE(5) OVER (
            ORDER BY frequency ASC, CustomerID
        ) AS f_score,

        -- 消费金额越高，M 分数越高 / Higher spending scores higher
        NTILE(5) OVER (
            ORDER BY monetary ASC, CustomerID
        ) AS m_score

    FROM customer_rfm
)

-- 4. 查看高消费客户的 RFM 评分 / Review RFM scores of top-spending customers
SELECT
    CustomerID,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score

FROM rfm_scores

ORDER BY monetary DESC, CustomerID ASC

LIMIT 20;
