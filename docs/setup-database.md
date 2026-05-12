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
