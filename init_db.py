import os
import psycopg2

conn = psycopg2.connect(os.environ['DATABASE_URL'])

cur = conn.cursor()

with open('schema.sql') as f:
    cur.execute(f.read())

conn.commit()

cur.close()
conn.close()
