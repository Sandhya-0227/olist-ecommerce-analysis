import pandas as pd
import sqlite3

conn = sqlite3.connect('olist.db')

# Revenue Analysis
# 1. What is the total revenue, total orders, and average order value overall?
query = """
select 
    sum(total_order_value) as total_revenue,
    count(order_id) as total_orders,
    avg(total_order_value) as avg_order_value
from olist_master
"""
result = pd.read_sql_query(query, conn)
print(result)

# checking total orders and unique orders
query="""
SELECT COUNT(order_id) as total_rows, COUNT(DISTINCT order_id) as unique_orders
FROM olist_master
"""
result=pd.read_sql_query(query, conn)
print(result) 

# 2. Which are the top 10 product categories by total revenue and average order value?
query = """
select 
    product_category_name_english,
    sum(total_order_value) as total_revenue,
    round(avg(total_order_value),2) as avg_order_value
from olist_master
group by product_category_name_english
order by total_revenue desc, avg_order_value desc
limit 10
"""
result = pd.read_sql_query(query, conn)
print(result)

# 3. What is the monthly revenue for each year — 2017 and 2018 side by side?
query="""
select 
    order_month,
    round(sum(case when order_year = 2017 then total_order_value else 0 end),2) as revenue_2017,
    round(sum(case when order_year = 2018 then total_order_value else 0 end),2) as revenue_2018
from olist_master
where order_year in (2017,2018)
group by order_month
order by order_month
"""
result=pd.read_sql_query(query, conn)
print(result)

