CREATE SCHEMA IF NOT EXISTS elo;

SELECT schema_name FROM information_schema.schemata;
SELECT nspname FROM pg_catalog.pg_namespace;

Drop schema if exists elo cascade;

SELECT * FROM information_schema.tables
WHERE table_schema = 'public'

SELECT table_schema||'.'||table_name AS full_rel_name
  FROM information_schema.tables
 WHERE table_schema = 'autobus';


