import os
import pandas as pd


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

def clean_orders_products_customers():
    orders = pd.read_csv('../data/raw/olist_orders_dataset.csv')
    customers = pd.read_csv('../data/raw/olist_customers_dataset.csv')
    products = pd.read_csv('../data/raw/olist_products_dataset.csv')

    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
    ]

    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])

    products['product_category_name'] = products['product_category_name'].fillna("unknown")

    cols_to_zero = [
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
    ]

    products[cols_to_zero] = products[cols_to_zero].fillna(0)

    orders.to_csv('../data/processed/orders_clean.csv', index=False)
    products.to_csv('../data/processed/products_clean.csv', index=False)
    customers.to_csv('../data/processed/customers_clean.csv', index=False)
