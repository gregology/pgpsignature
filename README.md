# PGP Signature

A repo for storing PGP Signatures.

## Production (Docker)

### Create Postgres database

```SQL
CREATE DATABASE "pgpsignature";
CREATE USER "user" WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE "pgpsignature" TO "user";
```

### Create container

```bash
docker run -d \
  -p 5000:5000 \
  --name="pgpsignature" \
  -e APP_SETTINGS="config.ProductionConfig" \
  -e DATABASE_URL="postgresql://user:password@host.docker.internal/pgpsignature" \
  gregology/pgpsignature:latest
```

### Initialize database

```bash
docker exec -it pgpsignature python /app/init_db.py 
```

## Development

### Create Postgres database

```SQL
CREATE DATABASE "pgpsignature";
CREATE USER "user" WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE "pgpsignature" TO "user";
```

### Install requirements
```bash
pip install -r requirements.txt
```
### Set environment variables

```bash
export APP_SETTINGS=config.DevelopmentConfig
export DATABASE_URL=postgresql://user:password@localhost/pgpsignature
```

### Initialize database

```bash
python /app/init_db.py 
```

### Run app

```bash
flask run
```
