--4. Customer Retention

SELECT customer_unique_id, COUNT(DISTINCT(order_id)) AS total_orders, ROUND(SUM(price)::numeric, 2) AS total_spent
FROM dim_customer
JOIN fact_orders ON fact_orders.customer_id = dim_customer.customer_id
WHERE order_status = 'delivered'
GROUP BY customer_unique_id
HAVING COUNT(DISTINCT order_id) > 1
ORDER BY total_orders DESC