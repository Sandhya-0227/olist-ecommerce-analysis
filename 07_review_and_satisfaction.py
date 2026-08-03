# Review & Satisfaction
# 8. What is the distribution of review scores — how many orders got each score from 1 to 5?
import pandas as pd
import sqlite3

conn = sqlite3.connect('olist.db')

query = """
select 
    review_score, 
    count(distinct order_id) as order_count,
    ROUND(COUNT(DISTINCT order_id) * 100.0 / SUM(COUNT(DISTINCT order_id)) OVER(), 2) as order_review
from olist_master
where review_score is not null
group by review_score
order by review_score desc
"""
result = pd.read_sql_query(query, conn)
print(result)

# 9. What is the average review score for late orders versus early orders?
query = """
select 
    case when delivery_delay_days > 0 then 'Late' else 'Early' end as delivery_category,
    count(distinct order_id) as order_count,
    round(avg(review_score),2) as avg_review_score
from olist_master
where review_score is not null
group by delivery_category
"""
result = pd.read_sql_query(query, conn)
print(result)