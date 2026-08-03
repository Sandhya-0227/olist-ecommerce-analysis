# Seller Performance
# 10. Who are the top 10 sellers by total revenue generated?
import pandas as pd
import sqlite3

conn = sqlite3.connect('olist.db')

query = """
select
    seller_id, 
    count(distinct order_id) as total_orders,
    round(sum(total_order_value),2) as total_revenue,
    round(avg(total_order_value),2) as avg_order_value
from olist_master
group by seller_id
order by total_revenue desc
limit 10
"""
result = pd.read_sql_query(query, conn)
print(result)