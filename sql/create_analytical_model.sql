-- 1. DIMENSION: Customer

DROP TABLE IF EXISTS dim_customer CASCADE;
CREATE TABLE dim_customer AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM stg_customers;

ALTER TABLE dim_customer ADD PRIMARY KEY (customer_id);

-- 2. DIMENSION: Product
DROP TABLE IF EXISTS dim_product CASCADE;
CREATE TABLE dim_product AS
SELECT
    p.product_id,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category_name,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM stg_products p
LEFT JOIN stg_category_translation t
    ON p.product_category_name = t.product_category_name;

ALTER TABLE dim_product ADD PRIMARY KEY (product_id);

-- 3. DIMENSION: Geography
DROP TABLE IF EXISTS dim_geography CASCADE;
CREATE TABLE dim_geography AS
SELECT
    geolocation_zip_code_prefix AS zip_code_prefix,
    geolocation_city AS city,
    geolocation_state AS state,
    AVG(geolocation_lat) AS latitude,
    AVG(geolocation_lng) AS longitude
FROM stg_geolocation
GROUP BY geolocation_zip_code_prefix, geolocation_city, geolocation_state;

ALTER TABLE dim_geography ADD PRIMARY KEY (zip_code_prefix);

-- 4. DIMENSION: Date
DROP TABLE IF EXISTS dim_date CASCADE;
CREATE TABLE dim_date AS
WITH date_series AS (
    SELECT generate_series(
         '2016-01-01'::date,
         '2020-12-31'::date,
         '1 day'::interval
    )::date AS full_date
)
SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INT AS date_id,
    full_date,
    EXTRACT(YEAR FROM full_date)::INT AS year,
    EXTRACT(QUARTER FROM full_date)::INT AS quarter,
    EXTRACT(MONTH FROM full_date)::INT AS month,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(DAY FROM full_date)::INT AS day_of_month,
    EXTRACT(ISODOW FROM full_date)::INT AS day_of_week,
    TO_CHAR(full_date, 'Day') AS day_name,
    CASE WHEN EXTRACT(ISODOW FROM full_date) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_series;

ALTER TABLE dim_date ADD PRIMARY KEY (date_id);

-- 5. FACT TABLE: Orders
DROP TABLE IF EXISTS fact_orders CASCADE;
CREATE TABLE fact_orders AS
SELECT
    oi.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    c.customer_zip_code_prefix AS customer_zip_code,
    TO_CHAR(o.order_purchase_timestamp::timestamp, 'YYYYMMDD')::INT AS order_date_id,
    o.order_status,
    o.order_purchase_timestamp::timestamp AS order_purchase_timestamp,
    o.order_approved_at::timestamp AS order_approved_at,
    o.order_delivered_carrier_date::timestamp AS order_delivered_carrier_date,
    o.order_delivered_customer_date::timestamp AS order_delivered_customer_date,
    o.order_estimated_delivery_date::timestamp AS order_estimated_delivery_date,
    oi.price,
    oi.freight_value,
    r.review_score,
    p.payment_type,
    p.payment_installments,
    p.payment_value
FROM stg_order_items oi
JOIN stg_orders o ON oi.order_id = o.order_id
LEFT JOIN stg_customers c ON o.customer_id = c.customer_id
LEFT JOIN (
    SELECT order_id, AVG(review_score)::NUMERIC(3,2) AS review_score
    FROM stg_order_reviews
    GROUP BY order_id
) r ON oi.order_id = r.order_id
LEFT JOIN (
    SELECT order_id,
           STRING_AGG(DISTINCT payment_type, ', ') AS payment_type,
           MAX(payment_installments) AS payment_installments,
           SUM(payment_value) AS payment_value
    FROM stg_order_payments
    GROUP BY order_id
) p ON oi.order_id = p.order_id;

ALTER TABLE fact_orders ADD PRIMARY KEY (order_id, order_item_id);