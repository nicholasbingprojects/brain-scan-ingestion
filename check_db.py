import duckdb

con = duckdb.connect("brain_scan_staging.duckdb")
tables = con.execute("SHOW TABLES;").fetchall()
print("Tables in DuckDB:", tables)

# If tables exist, check staged datasets
if any("staging_datasets" in t for t in tables):
    print("\n--- Staged Datasets ---")
    print(con.execute("SELECT * FROM staging_datasets;").df())

if any("audit_integrity_logs" in t for t in tables):
    print("\n--- Integrity Audit Summary ---")
    print(con.execute("SELECT dataset_id, status, count(*) FROM audit_integrity_logs GROUP BY dataset_id, status;").df())

con.close()