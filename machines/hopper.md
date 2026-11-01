# Hopper

## Role

Windows analytics workstation and administration client.

## Hardware

- Dell Inspiron 7591 2-in-1
- Intel Core i5-10210U
- 16 GB DDR4-2666
- 512 GB SSD

## Shell

- Windows Terminal
- PowerShell 7.6.6

## Git and GitHub

- Git for Windows
- GitHub Desktop
- Default branch: 'main'
- Git identity configured
- Git Credential Manager

## Python

- Python 3.14.7
- Project-specific virtual environments
- pip dependency management

## VS Code

- Python
- Jupyter
- PowerShell
- SQLTools
- GitHub Pull Requests
- Remote - SSH

## Analytics

- Microsoft Excel
- Power BI Desktop
- Python
- pandas
- Polars
- DuckDB
- PyArrow
- Jupyter
- DBeaver Community
- SQLTools

## Analytics Benchmark

25,000,000-row dataframe benchmark:

- pandas: 0.5617 s
- Polars: 0.0672 s
- DuckDB: 0.1156 s

## Analytics Workflow Validation

Validated on 2026-10-11:

- [x] Windows-native Python virtual environment rebuilt
- [x] Shared `requirements.txt` installed successfully
- [x] VS Code configured to use project `.venv`
- [x] Jupyter notebook execution validated
- [x] pandas import validated
- [x] Polars import validated
- [x] DuckDB import validated
- [x] PyArrow interoperability validated
- [x] 25,000,000-row benchmark completed
- [x] DBeaver Community installed and configured
- [x] DuckDB database created and queried in DBeaver
- [x] Reproducible SQL creation script added
- [x] Python queried the same DuckDB database successfully

## Current State

Hopper is now a validated Windows analytics workstation and administration client.

It supports:

- Local Python and SQL analytics
- Jupyter-based exploration
- Power BI and Excel workflows
- Git/GitHub development
- DuckDB-based local databases
- DBeaver database administration
- SSH and Remote-SSH administration of Ichabod

## SSH and Remote Administration

- OpenSSH
- SCP
- SFTP
- ED25519 authentication
- ssh-agent
- VS Code Remote - SSH

## Current Projects

- SQL-Python
- Analytics Lab
- Ichabod administration

## Validation

- [x] Git commit/push workflow
- [x] Python virtual environment
- [x] SSH Key generation
- [x] ssh-agent
- [x] GitHub remote
- [ ] DuckDB workflow
- [ ] DBeaver
- [ ] SSH connection to Ichabod
- [ ] Remote database connection

## What I Learned

- Git repositories are independent of GitHub.
- A Python virtual environment isolates dependencies by project.
- SSH public and private keys serve different roles.
- ssh-agent can hold an unlocked private key for authenticated sessions.
- Git ignores empty directories unless placeholder files are used.
- Git tracks saved files, not unsaved editor buffers.
- Virtual environments isolate Python dependencies by project.
- `requirements.txt` provides a shared dependency definition across machines.
- DuckDB can be accessed from multiple tools, but local file locking matters.
- DBeaver and Python can act as separate clients against the same database file.
- SQL `INSERT` statements add rows rather than replacing existing data.
- Reproducible workflows are better than committing local database files.