import os
import pandas as pd

orders = pd.read_csv('../data/raw/olist_orders_dataset.csv')
customers = pd.read_csv('../data/raw/olist_customers_dataset.csv')
products = pd.read_csv('../data/raw/olist_products_dataset.csv')
#
# print('ORDERS INFORMATION')
# print(orders.info())
# print('----------------')
# print(orders.isnull().sum())
#
# print("\n")
#
# print('PRODUCTS INFO')
# print(products.info())
# print('--------------')
# print(products.isnull().sum())
#
# print("\n")
# print('Customer info')
# print(customers.info())
# print(customers.isnull().sum())

# orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
# orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
# orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
# orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
# orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
#
# # print("Date type check: ")
# # print(orders[['order_purchase_timestamp', 'order_delivered_customer_date', 'order_purchase_timestamp',
# # 'order_approved_at', 'order_delivered_carrier_date', 'order_estimated_delivery_date']].dtypes)
#
# products['product_category_name'] = products['product_category_name'].fillna('unknown')
#
# print("Preostala prazna polja u kategoriji proizvoda: ")
# print(products['product_category_name'].isnull().sum())
#
cols_to_zero = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty']
products[cols_to_zero] = products[cols_to_zero].fillna(0)

orders.to_csv('../data/processed/orders_clean.csv', index=False)
products.to_csv('../data/processed/products_clean.csv', index=False)
customers.to_csv('../data/processed/customers.csv', index=False)
