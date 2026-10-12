import duckdb

database_path = r"C:\Analytics\Projects\analytics-lab\data\nomad_lab.duckdb"

con = duckdb.connect(database_path)

result = con.execute("""
    SELECT
        department,
        SUM(cases) AS total_cases
    FROM department_cases
    GROUP BY department
    ORDER BY total_cases DESC
""").fetchdf()

print(result)

con.close()