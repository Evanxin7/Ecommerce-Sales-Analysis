-- 1. 选择项目数据库 / Select analysis database
USE ecommerce_analysis;

-- 2. 检查缺失值与异常值 / Check missing and invalid values
SELECT
    COUNT(*) AS total_rows,

    SUM(
        CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END
    ) AS missing_customer_ids,

    SUM(
        CASE
            WHEN Description IS NULL
              OR TRIM(Description) = ''
            THEN 1 ELSE 0
        END
    ) AS missing_descriptions,

    SUM(
        CASE WHEN Quantity <= 0 THEN 1 ELSE 0 END
    ) AS invalid_quantities,

    SUM(
        CASE WHEN UnitPrice <= 0 THEN 1 ELSE 0 END
    ) AS invalid_prices,

    SUM(
        CASE
            WHEN Revenue IS NULL
              OR ABS(Revenue - Quantity * UnitPrice) > 0.01
            THEN 1 ELSE 0
        END
    ) AS revenue_mismatches,

    SUM(
        CASE
            WHEN OrderDate IS NULL
              OR DATE(InvoiceDate) <> OrderDate
            THEN 1 ELSE 0
        END
    ) AS date_mismatches,

    MIN(InvoiceDate) AS earliest_transaction,

    MAX(InvoiceDate) AS latest_transaction

FROM sales;

-- 3. 检查重复交易明细 / Check duplicate transaction rows
WITH duplicate_groups AS (
    SELECT
        COUNT(*) AS occurrence_count
    FROM sales
    GROUP BY
        InvoiceNo COLLATE utf8mb4_0900_bin,
        StockCode COLLATE utf8mb4_0900_bin,
        Description COLLATE utf8mb4_0900_bin,
        Quantity,
        InvoiceDate,
        UnitPrice,
        CustomerID,
        Country COLLATE utf8mb4_0900_bin
    HAVING COUNT(*) > 1
)

-- 4. 统计重复记录 / Summarize duplicate records
SELECT
    COUNT(*) AS duplicated_groups,
    COALESCE(
        SUM(occurrence_count - 1),
        0
    ) AS duplicate_extra_rows
FROM duplicate_groups;
