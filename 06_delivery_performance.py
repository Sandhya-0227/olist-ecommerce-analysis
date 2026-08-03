# Delivery Performance
# 6. What is the average delivery days, average delay days, and percentage of late orders overall?
import pandas as pd
import sqlite3

conn = sqlite3.connect('olist.db')

query = """
select
    round(avg(delivery_days),2) as avg_del_days,
    round(avg(delivery_delay_days),2) as avg_delay_days,
    count(case when delivery_delay_days > 0 then order_id else null end) as late_orders,
    round(count(case when delivery_delay_days > 0 then order_id else null end) * 100.0 /count(distinct order_id),2) as per_late_orders
from olist_master
"""
result = pd.read_sql_query(query, conn)
print(result)

# 7. Which product categories have the worst average delivery delay?
query = """
select 
    product_category_name_english, 
    count(distinct order_id) as late_order_count, 
    round(avg(delivery_delay_days),2) as avg_del_delay
from olist_master
where delivery_delay_days > 0
group by product_category_name_english
having count(distinct order_id) > 50
order by avg_del_delay desc
limit 10
"""
result = pd.read_sql_query(query, conn)
print(result)