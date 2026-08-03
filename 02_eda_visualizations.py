import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Add this line - prevents window popups, saves directly to file
import matplotlib.pyplot as plt
import os

# Load master table
master = pd.read_csv(r'C:\Users\Sandhya\OneDrive\Desktop\Olist Dataset\archive\master_table.csv')

# Output folder for saving charts
output_folder = r'C:\Users\Sandhya\OneDrive\Desktop\python_learning\olist_ecommerce_project\charts'
os.makedirs(output_folder, exist_ok=True)

print(f"Master table loaded: {master.shape}")
print(f"Columns: {master.columns.tolist()}")

# --- CHART 1: Top 10 Product Categories by Revenue ---

# Aggregate revenue by English category name
category_revenue = (
    master.groupby('product_category_name_english')['total_order_value']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

category_revenue.columns = ['category', 'total_revenue']

print("Top 10 Categories by Revenue:")
print(category_revenue)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.barh(category_revenue['category'][::-1], 
               category_revenue['total_revenue'][::-1],
               color='steelblue', edgecolor='white')

# Add value labels on bars
for bar, val in zip(bars, category_revenue['total_revenue'][::-1]):
    ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
            f'R$ {val:,.0f}', va='center', fontsize=9)

ax.set_title('Top 10 Product Categories by Revenue', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Total Revenue (BRL)', fontsize=11)
ax.set_ylabel('Product Category', fontsize=11)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'R$ {x/1e6:.1f}M'))
plt.tight_layout()

# Save
chart1_path = os.path.join(output_folder, 'chart1_category_revenue.png')
plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"\nChart 1 saved to: {chart1_path}")

# --- CHART 2: Monthly Revenue Trend ---

# Aggregate revenue by year-month
monthly_revenue = (
    master.groupby('order_year_month')['total_order_value']
    .sum()
    .reset_index()
)
monthly_revenue.columns = ['year_month', 'total_revenue']

# Remove last month (likely incomplete data)
monthly_revenue = monthly_revenue.iloc[:-1]

print("Monthly Revenue:")
print(monthly_revenue)

# Plot
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(monthly_revenue['year_month'], monthly_revenue['total_revenue'],
        color='steelblue', linewidth=2.5, marker='o', markersize=5)

ax.fill_between(monthly_revenue['year_month'], monthly_revenue['total_revenue'],
                alpha=0.15, color='steelblue')

ax.set_title('Monthly Revenue Trend (2016-2018)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Total Revenue (BRL)', fontsize=11)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'R$ {x/1e6:.1f}M'))

# Rotate x labels so they don't overlap
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()

# Save
chart2_path = os.path.join(output_folder, 'chart2_monthly_revenue.png')
plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"\nChart 2 saved to: {chart2_path}")

# --- CHART 3: Top 10 Customer States by Order Volume ---

state_orders = (
    master.groupby('customer_state')['order_id']
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
state_orders.columns = ['state', 'order_count']

print("Top 10 States by Orders:")
print(state_orders)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

colors = ['#1f4e79' if i == 0 else 'steelblue' for i in range(len(state_orders))]

bars = ax.bar(state_orders['state'], state_orders['order_count'],
              color=colors, edgecolor='white')

# Add value labels on top of bars
for bar, val in zip(bars, state_orders['order_count']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
            f'{val:,}', ha='center', va='bottom', fontsize=9)

ax.set_title('Top 10 Customer States by Order Volume', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Customer State', fontsize=11)
ax.set_ylabel('Number of Orders', fontsize=11)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
plt.tight_layout()

# Save
chart3_path = os.path.join(output_folder, 'chart3_state_orders.png')
plt.savefig(chart3_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"\nChart 3 saved to: {chart3_path}")

# --- CHART 4: Delivery Delay vs Average Review Score ---

# Only use rows where review score exists
delay_review = master.dropna(subset=['review_score']).copy()

# Create delay buckets
def delay_bucket(days):
    if days < -20:
        return 'Very Early (>20 days)'
    elif days < -10:
        return 'Early (10-20 days)'
    elif days < 0:
        return 'Slightly Early (0-10 days)'
    elif days <= 7:
        return 'Slightly Late (0-7 days)'
    else:
        return 'Very Late (>7 days)'

delay_review['delay_bucket'] = delay_review['delivery_delay_days'].apply(delay_bucket)

# Define order for x axis
bucket_order = [
    'Very Early (>20 days)',
    'Early (10-20 days)',
    'Slightly Early (0-10 days)',
    'Slightly Late (0-7 days)',
    'Very Late (>7 days)'
]

avg_score = (
    delay_review.groupby('delay_bucket')['review_score']
    .mean()
    .reindex(bucket_order)
    .reset_index()
)
avg_score.columns = ['delay_bucket', 'avg_review_score']

print("Avg Review Score by Delay Bucket:")
print(avg_score)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

colors = ['#2ecc71' if 'Early' in b else '#e74c3c' for b in avg_score['delay_bucket']]

bars = ax.bar(avg_score['delay_bucket'], avg_score['avg_review_score'],
              color=colors, edgecolor='white', width=0.6)

# Add value labels
for bar, val in zip(bars, avg_score['avg_review_score']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Impact of Delivery Timing on Customer Review Score', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Delivery Timing', fontsize=11)
ax.set_ylabel('Average Review Score (1-5)', fontsize=11)
ax.set_ylim(0, 5.5)
ax.axhline(y=4.0, color='gray', linestyle='--', alpha=0.5, label='Score = 4.0')
plt.xticks(fontsize=9)
plt.tight_layout()

# Save
chart4_path = os.path.join(output_folder, 'chart4_delay_vs_review.png')
plt.savefig(chart4_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"\nChart 4 saved to: {chart4_path}")

# --- CHART 5: Order Value Distribution ---

# Remove extreme outliers for clean visualization (keep 99th percentile)
p99 = master['total_order_value'].quantile(0.99)
order_values = master[master['total_order_value'] <= p99]['total_order_value']

print(f"Order value stats (excluding top 1% outliers):")
print(order_values.describe())

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(order_values, bins=60, color='steelblue', edgecolor='white', alpha=0.85)

# Add mean and median lines
mean_val = order_values.mean()
median_val = order_values.median()

ax.axvline(mean_val, color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: R$ {mean_val:.0f}')
ax.axvline(median_val, color='#2ecc71', linestyle='--', linewidth=2, label=f'Median: R$ {median_val:.0f}')

ax.set_title('Distribution of Order Values', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Order Value (BRL)', fontsize=11)
ax.set_ylabel('Number of Orders', fontsize=11)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'R$ {x:.0f}'))
ax.legend(fontsize=11)
plt.tight_layout()

# Save
chart5_path = os.path.join(output_folder, 'chart5_order_value_distribution.png')
plt.savefig(chart5_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"\nChart 5 saved to: {chart5_path}")