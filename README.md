# Roster ETL

This project is a **mini ETL pipeline** that reads roster data from a JSON file, transforms and validates it, and loads it into an SQLite database. 

It demonstrates core concepts of Data Engineering, including data validation, normalization, deduplication, and database operations.

---

## Features

- Read roster data from JSON (`roster_data.json`)
- Validate and clean data
- Transform data types (e.g., convert roles to integers)
- Normalize data into `Users`, `Courses`, and `Members` tables
- Insert data into SQLite database (`rosterdb.sqlite3`)
- Handles duplicate entries and updates roles using `UPSERT`
- Logging of invalid or missing data
