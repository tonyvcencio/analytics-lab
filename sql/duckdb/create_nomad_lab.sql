DROP TABLE IF EXISTS department_cases;

CREATE TABLE department_cases (
    department VARCHAR,
    cases INTEGER
);

INSERT INTO department_cases VALUES
    ('A', 120),
    ('A', 135),
    ('B', 98),
    ('B', 110),
    ('C', 87);
SELECT
    department,
    SUM(cases) AS total_cases
FROM department_cases
GROUP BY department
ORDER BY total_cases DESC;
SELECT * FROM department_cases;
DROP TABLE IF EXISTS department_cases;
CREATE TABLE department_cases (
    department VARCHAR,
    cases INTEGER
);
INSERT INTO department_cases VALUES
    ('A', 120),
    ('A', 135),
    ('B', 98),
    ('B', 110),
    ('C', 87);
SELECT
    department,
    SUM(cases) AS total_cases
FROM department_cases
GROUP BY department
ORDER BY total_cases DESC;
