# Database setup

## Prerequisites
- PostgreSQL 14 or higher installed and running.

## Steps

1. Connect as superuser:
```bash
   sudo -u postgres psql
```

2. Create database and application user:
```sql
   CREATE DATABASE db_name;
   CREATE USER user_name WITH PASSWORD '<your-secure-password>';
   GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;
```

3. Connect to the new database and create medallion schemas:
```sql
   \c db_name
   CREATE SCHEMA raw;
   CREATE SCHEMA staging;
   CREATE SCHEMA marts;

   GRANT ALL ON SCHEMA raw TO user_name;
   GRANT ALL ON SCHEMA staging TO user_name;
   GRANT ALL ON SCHEMA marts TO user_name;
```

4. Exit psql with `\q`.

5. Test the connection with the application user:
```bash
   psql -h localhost -U user_name -d db_name
```

6. Update your local `.env` file with the password chosen in step 2:

## Notes on architecture

This project uses a **medallion architecture** with three schemas:

- `raw` (Bronze): raw data ingested from sources, append-only.
- `staging` (Silver): cleaned and typed data, built with dbt.
- `marts` (Gold): dimensional model for analytics, built with dbt.

See [architecture.md](architecture.md) for details.

## Security

The `user_name` user has database-scoped privileges but is **not** a superuser. This follows the **least privilege principle**: if application credentials leak, damage is contained.
