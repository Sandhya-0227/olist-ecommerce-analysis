import pandas as pd
import sqlite3

# Load master table
master = pd.read_csv(r'C:\Users\Sandhya\OneDrive\Desktop\Olist Dataset\archive\master_table.csv')

# Create SQLite database and load master table into it
conn = sqlite3.connect('olist.db')
master.to_sql('olist_master', conn, if_exists='replace', index=False)

print("Database created and table loaded successfully")
print(f"Rows loaded: {len(master)}")

# to check the data upto 5 rows
query = """
select *
from olist_master
limit 5
"""
result = pd.read_sql_query(query, conn)
print(result)

# this query is used to see all the columns along with their datatype
query ="""
PRAGMA table_info(olist_master)
"""
result = pd.read_sql_query(query, conn)
print(result[['name','type']])



