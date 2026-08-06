--2. Product Analysis

SELECT product_category_name AS product_category, COUNT(fact_orders.product_id) AS units_sold, ROUND(SUM(price)::numeric, 2) AS total_revenue,
ROUND(AVG(review_score)::numeric, 2) AS avg_review_score
FROM dim_product
JOIN fact_orders ON dim_product.product_id = fact_orders.product_id
WHERE order_status = 'delivered'
GROUP BY product_category_name
ORDER BY total_revenue DESC