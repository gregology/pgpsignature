export FLASK_APP=app

export FLASK_ENV=development

flask run

based on https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

update requirements `pipreqs ./ --force`


CREATE DATABASE "pgpsignature";
CREATE USER "user" WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE "pgpsignature" TO "user";

export FLASK_ENV=development

export FLASK_APP=app
export DB_HOST=localhost
export DB_NAME=pgpsignature
export DB_USERNAME=user
export DB_PASSWORD=password


```
import os
import psycopg2

conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

with open('schema.sql') as f:
    cur.execute(f.read())

conn.commit()

cur.close()
conn.close()
```

```
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    
    return conn
```

```
DROP TABLE IF EXISTS signatures;

CREATE TABLE signatures (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL
);
```

