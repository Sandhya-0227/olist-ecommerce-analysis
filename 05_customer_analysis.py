import pandas as pd
import sqlite3

conn = sqlite3.connect('olist.db')

# Customer Analysis
# 4. Which top 10 states contribute the most revenue — and what is their average review score?
query = """
select 
    customer_state,
    count(distinct order_id) as total_orders,
    round(sum(total_order_value),2) as total_revenue,
    round(avg(review_score),2) as avg_review_score
from olist_master
group by customer_state
order by total_revenue desc
limit 10
"""
result = pd.read_sql_query(query, conn)
print(result)

# 5. How many customers placed more than one order? What percentage of total customers is that?
query = """
select 
    customer_id,
    count(distinct order_id) as order_count
from olist_master
group by customer_id
having order_count > 1
"""
result = pd.read_sql_query(query, conn)
print(result)

# 5.2 What is the order frequency distribution — how many orders had 1 item, 2 items, 3 items, etc.?
query = """
select 
    order_item_id,
    count(distinct order_id) as order_count
from olist_master
group by order_item_id
"""
result = pd.read_sql_query(query, conn)
print(result)
