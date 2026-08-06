--3. Customer Analytics

SELECT customer_state AS state, COUNT(DISTINCT(customer_unique_id)) AS total_customers,
COUNT(DISTINCT order_id) AS total_orders, ROUND(SUM(price)::numeric, 2) AS total_revenue
FROM dim_customer
JOIN fact_orders ON fact_orders.customer_id = dim_customer.customer_id
WHERE order_status = 'delivered'
GROUP BY customer_state
ORDER BY total_revenue DESC
LIMIT 10