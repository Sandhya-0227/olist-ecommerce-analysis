import pandas as pd

base_path = r'C:\Users\Sandhya\OneDrive\Desktop\Olist Dataset\archive' + '\\'

customers = pd.read_csv(base_path + 'olist_customers_dataset.csv')
orders = pd.read_csv(base_path + 'olist_orders_dataset.csv')
order_items = pd.read_csv(base_path + 'olist_order_items_dataset.csv')
order_payments = pd.read_csv(base_path + 'olist_order_payments_dataset.csv')
order_reviews = pd.read_csv(base_path + 'olist_order_reviews_dataset.csv')
products = pd.read_csv(base_path + 'olist_products_dataset.csv')
sellers = pd.read_csv(base_path + 'olist_sellers_dataset.csv')
geolocation = pd.read_csv(base_path + 'olist_geolocation_dataset.csv')
category_translation = pd.read_csv(base_path + 'product_category_name_translation.csv')

print("All files loaded successfully")

# Check shape and basic info for the 3 most important tables
for name, df in [('orders', orders),
                 ('order_items', order_items),
                 ('order_reviews', order_reviews)]:
    print(f"\n{'='*40}")
    print(f"TABLE: {name}")
    print(f"Shape: {df.shape}")
    print(f"\nColumn names:\n{df.columns.tolist()}")
    print(f"\nNull counts:\n{df.isnull().sum()}")
    print(f"\nData types:\n{df.dtypes}")

# Convert timestamp columns to datetime
timestamp_cols = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

for col in timestamp_cols:
    orders[col] = pd.to_datetime(orders[col])

print("Timestamp conversion done")
print(f"\nData types after conversion:\n{orders.dtypes}")

# --- SECTION 4: Calculate Delivery Metrics ---

# Days taken to deliver to customer from purchase
orders['delivery_days'] = (
    orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
).dt.days

# Days difference between actual and estimated delivery (negative = early, positive = late)
orders['delivery_delay_days'] = (
    orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']
).dt.days

# Days taken for order to be approved after purchase
orders['approval_days'] = (
    orders['order_approved_at'] - orders['order_purchase_timestamp']
).dt.days

print("Delivery metrics calculated")
print(f"\nSample of new columns:")
print(orders[['order_id', 'order_status', 'delivery_days', 
              'delivery_delay_days', 'approval_days']].head(10))

print(f"\nDelivery metrics summary:")
print(orders[['delivery_days', 'delivery_delay_days', 'approval_days']].describe())

# --- SECTION 5: Filter to Delivered Orders Only ---

delivered_orders = orders[orders['order_status'] == 'delivered'].copy()

print(f"Total orders: {len(orders)}")
print(f"Delivered orders: {len(delivered_orders)}")
print(f"Non-delivered orders removed: {len(orders) - len(delivered_orders)}")
print(f"\nDelivered orders as % of total: {len(delivered_orders)/len(orders)*100:.1f}%")

# Check nulls in delivered orders only
print(f"\nNull counts in delivered orders:")
print(delivered_orders[['delivery_days', 'delivery_delay_days', 'approval_days']].isnull().sum())

# --- SECTION 6: Drop remaining nulls and build master table ---

# Drop the 8 rows with missing delivery dates in delivered orders
delivered_orders = delivered_orders.dropna(subset=['delivery_days', 'delivery_delay_days'])

print(f"Delivered orders after dropping nulls: {len(delivered_orders)}")

# Join order_items to get product, seller, price, freight
master = delivered_orders.merge(order_items, on='order_id', how='left')

# Join products to get category
master = master.merge(products[['product_id', 'product_category_name']], 
                      on='product_id', how='left')

# Join category translation to get English category names
master = master.merge(category_translation, 
                      on='product_category_name', how='left')

# Join customers to get customer state
master = master.merge(customers[['customer_id', 'customer_state', 'customer_city']], 
                      on='customer_id', how='left')

# Join reviews to get review score
master = master.merge(order_reviews[['order_id', 'review_score']], 
                      on='order_id', how='left')

# Create total order value column
master['total_order_value'] = master['price'] + master['freight_value']

print(f"\nMaster table shape: {master.shape}")
print(f"\nMaster table columns:\n{master.columns.tolist()}")
print(f"\nNull counts in master table:\n{master.isnull().sum()}")

# --- SECTION 7: Handle nulls and save master table ---

# Fill missing category names with 'uncategorized'
master['product_category_name'] = master['product_category_name'].fillna('uncategorized')
master['product_category_name_english'] = master['product_category_name_english'].fillna('uncategorized')

# Add time columns for grouping later
master['order_year'] = master['order_purchase_timestamp'].dt.year
master['order_month'] = master['order_purchase_timestamp'].dt.month
master['order_year_month'] = master['order_purchase_timestamp'].dt.to_period('M').astype(str)

# Final null check
print("Null counts after cleaning:")
print(master.isnull().sum())

# Save master table to CSV
output_path = r'C:\Users\Sandhya\OneDrive\Desktop\Olist Dataset\archive\master_table.csv'
master.to_csv(output_path, index=False)

print(f"\nMaster table saved successfully")
print(f"Final shape: {master.shape}")