# Benchmark Results

Shared benchmark results for the Analytics Lab.

## Benchmark

- Rows: 25,000,000
- Script: `benchmarks/dataframe_benchmark.py`

## Nomad

- Platform: Windows
- CPU: Intel Core i5-10210U
- RAM: 16 GB
- pandas: 0.5617 s
- Polars: 0.0672 s
- DuckDB: 0.1156 s

## Mac

- Platform: macOS
- CPU: Apple M4 Pro
- RAM: 24 GB
- pandas: 0.1107 s
- Polars: 0.0100 s
- DuckDB: 0.0212 s