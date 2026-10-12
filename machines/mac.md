# Mac — M4 Pro Analytics Workstation

## Role

Primary macOS analytics and development workstation within the Analytics Lab.

The Mac serves as the main environment for Python development, data analysis,
performance benchmarking, Jupyter notebooks, GitHub development, and remote
Linux administration.

## Hardware

- Machine: Apple Mac mini
- Processor: Apple M4 Pro
- Architecture: ARM64 / Apple Silicon
- Operating system: macOS
- Primary display: Samsung 34-inch ultrawide
- Secondary display: Dell P2419H (portrait orientation)

## Development Environment

- Homebrew package manager
- zsh terminal
- Python 3.14.8
- Project-specific Python virtual environment (`.venv`)
- Visual Studio Code
- Python and Jupyter extensions
- Git and GitHub CLI
- SSH authentication with GitHub

### Python Analytics Libraries

- NumPy
- pandas
- Polars
- DuckDB
- Matplotlib
- Jupyter

Python dependencies are managed through the project's virtual environment.

## Analytics Benchmarks

Initial dataframe aggregation benchmarks using Python 3.14.8.

| Library | 5 Million Rows | 25 Million Rows |
|---|---:|---:|
| pandas | 0.0256 s | 0.1107 s |
| Polars | 0.0328 s | 0.0100 s |
| DuckDB | 0.0114 s | 0.0212 s |

The benchmark measures specific aggregation operations rather than
end-to-end dataset generation or processing time.

These are preliminary results. Future benchmarking should use repeated
measurements to account for run-to-run variability.

Additional benchmark documentation is maintained in
[Benchmark Results](../benchmarks/results.md).

## Git and GitHub

The Mac uses Git and SSH-authenticated GitHub access for project version control.

Primary repository: `tonyvcencio/analytics-lab`

The Mac and Windows Nomad share project code through GitHub while maintaining
independent Python environments.

## Linux Infrastructure Administration

The Mac serves as the remote administration workstation for Ichabod,
the headless Ubuntu Server 24.04 LTS machine.

Completed activities:

- Prepared Ubuntu installation media using the BOOT USB drive
- Established SSH connectivity to Ichabod
- Performed remote hardware inventory
- Inspected CPU, memory, and NVMe health
- Conducted NVMe short and extended self-tests
- Completed three passes of memory stability testing
- Conducted a five-minute CPU stress test
- Monitored CPU temperatures and inspected kernel logs

Ichabod completed initial hardware commissioning on October 11, 2026.

Detailed hardware and commissioning records are maintained separately.

## Current Projects

- Analytics Lab development
- Python and SQL experimentation
- Cross-platform development with Nomad
- Ichabod remote administration

## Planned Development

- Build an SQL → Python → Jupyter analytics pipeline
- Expand reproducible performance benchmarking
- Practice Git branching and merging
- Develop automated infrastructure health reports
- Explore larger datasets and Apple Silicon acceleration
- Integrate analytical workloads with Ichabod

## Status

**Operational — analytics development environment established and tested.**

Last reviewed: October 11, 2026.