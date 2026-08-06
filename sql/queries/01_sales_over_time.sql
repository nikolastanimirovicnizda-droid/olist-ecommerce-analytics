--1. Sales Over Time

SELECT year, month, month_name, COUNT(DISTINCT(order_id)) as total_orders,
 ROUND(SUM(price)::numeric, 2) AS total_revenue, ROUND(AVG(price)::numeric, 2) AS avg_order_value
FROM dim_date
JOIN fact_orders ON order_date_id = date_id
WHERE order_status = 'delivered'
GROUP BY year, month, month_name
ORDER BY year, month