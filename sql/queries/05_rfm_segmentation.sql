--5. RFM Segmentation

SELECT customer_unique_id, MAX(order_purchase_timestamp)::date AS last_order_date, COUNT(DISTINCT order_id) AS frequency,
ROUND(SUM(price)::numeric, 2) AS monetary
FROM dim_customer
JOIN fact_orders ON dim_customer.customer_id = fact_orders.customer_id
WHERE order_status = 'delivered'
GROUP BY customer_unique_id
ORDER BY monetary DESC