import os
import pandas as pd


def clean_orders_products_customers():
    orders = pd.read_csv('../data/raw/olist_orders_dataset.csv')
    customers = pd.read_csv('../data/raw/olist_customers_dataset.csv')
    products = pd.read_csv('../data/raw/olist_products_dataset.csv')
    # print('--- ORDERS INFO ---'); print(orders.info()); print(orders.isnull().sum())
    # print('--- PRODUCTS INFO ---'); print(products.info()); print(products.isnull().sum())
    # print('--- CUSTOMERS INFO ---'); print(customers.info()); print(customers.isnull().sum))

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


def clean_items_payments_translations():
    order_items = pd.read_csv('../data/raw/olist_order_items_dataset.csv')
    order_payments = pd.read_csv('../data/raw/olist_order_payments_dataset.csv')
    category_translation = pd.read_csv('../data/raw/product_category_name_translation.csv')

    # print('--- ORDER ITEMS INFO ---');print(order_items.info());print(order_items.isnull().sum());
    # print('\n');
    # print('--- ORDER PAYMENTS INFO ---');print(order_payments.info());print(order_payments.isnull().sum());
    # print('\n');
    # print('--- CATEGORY TRANSLATION INFO ---');print(category_translation.info());print(category_translation.isnull().sum())

    order_items['shipping_limit_date'] = pd.to_datetime(order_items['shipping_limit_date'])

    order_items.to_csv('../data/processed/order_items_clean.csv', index=False)
    order_payments.to_csv('../data/processed/order_payments_clean.csv', index=False)
    category_translation.to_csv('../data/processed/category_translation_clean.csv', index=False)
