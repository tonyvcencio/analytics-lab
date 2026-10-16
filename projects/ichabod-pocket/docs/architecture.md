# Ichabod Pocket — System Architecture

**Project 004 | Architecture v0.1**

## Overview

Ichabod Pocket is designed to provide secure, lightweight access
to system health information and analytics services running on
Ichabod University.

The architecture separates routine monitoring from AI-assisted
operations to minimize latency, cost, and unnecessary permissions.

## Proposed Architecture

```text
Rabbit R1 (Rabbit OS3)
         |
         v
Rabbit Creation
         |
         | Authenticated HTTPS
         v
Ichabod Pocket Monitoring API
         |
         | Restricted read-only access
         v
Project 001 — Health Metrics
         |
         +-- CPU utilization
         +-- CPU package temperature
         +-- Memory utilization
         +-- Disk utilization
         +-- System uptime
         +-- Collector status
```

**Status:** Proposed architecture. The monitoring API and Rabbit
Creation have not yet been implemented.

## Existing Infrastructure

### Ichabod University

| Component | Configuration |
|---|---|
| Server | Ichabod |
| Operating System | Ubuntu Server 24.04.5 LTS |
| Processor | Intel Core i3-12100T |
| Memory | 8 GB DDR4 |
| Existing Monitoring | Project 001 — Health Metrics |
| Computer Agent | rabbit-agent 0.1.16 |

### Project 001 — Health Metrics

Project 001 already includes a Python-based metrics collector
capable of gathering system information.

Ichabod Pocket will reuse this infrastructure wherever practical
rather than duplicate existing functionality.

The collector's data format, storage mechanism, and refresh
frequency will be reviewed during implementation.

## Rabbit Agent Integration

The Rabbit computer agent is installed on Ichabod under a
dedicated Linux service account.

| Property | Value |
|---|---|
| Account | rabbit-agent |
| UID/GID | 1001/1001 |
| Agent Version | 0.1.16 |
| Installation | /home/rabbit-agent/.rabbit-agent |
| Connection | Rabbit Cloud |

The agent operates without administrator privileges.

Process ownership and cron configuration were independently
verified on October 16, 2026.

The Rabbit Agent and Ichabod Pocket Monitoring API are separate
architectural components.

Routine dashboard operations should not require arbitrary
shell command execution through the Rabbit Agent.

## Thermal Monitoring

Thermal sensors were independently identified and validated
on October 16, 2026.

| Sensor | Linux Type | Verified Reading |
|---|---|---|
| thermal_zone0 | acpitz | 27.8°C |
| thermal_zone1 | x86_pkg_temp | 30.0°C |

### Sensor Identification

**thermal_zone0 — acpitz**

An ACPI firmware-defined thermal zone. Its exact physical
measurement location has not been established.

**thermal_zone1 — x86_pkg_temp**

Intel CPU package temperature sensor.

The measurements were independently confirmed through Ubuntu.

Although Rabbit OS3 reported matching values, the precise
command-execution path has not been independently verified.

## Security Architecture

Ichabod Pocket will follow these principles:

1. No administrator access for routine monitoring.
2. No unrestricted shell execution through the dashboard.
3. Explicitly approved read-only API endpoints.
4. Authentication for access to monitoring information.
5. Secure transport for remote connections.
6. No credentials or connection tokens committed to GitHub.
7. Minimal exposure of Ichabod's network services.

### Existing Security Decision

During initial testing, Rabbit OS3 requested persistent
permission to execute commands across Ichabod.

That permission was denied.

The proposed monitoring API will provide a more restricted
alternative for routine information retrieval.

### Open Security Items

- Rotate the previously exposed Rabbit Agent connection token.
- Determine supported authentication options for Rabbit Creations.
- Evaluate secure connectivity between Rabbit and Ichabod.
- Define API access restrictions.
- Validate the complete request and response path.

## Planned API Capabilities

Potential endpoints:

| Endpoint | Purpose |
|---|---|
| `/health` | Server availability |
| `/metrics/cpu` | CPU utilization and temperature |
| `/metrics/memory` | Memory utilization |
| `/metrics/disk` | Disk utilization |
| `/metrics/uptime` | System uptime |
| `/metrics/summary` | Consolidated health report |

These are preliminary endpoint designs, not implemented services.

## Future Architecture Extensions

Potential future capabilities include:

- Historical performance visualization.
- Analytics pipeline monitoring.
- Voice-generated system summaries.
- Notifications for abnormal conditions.
- Monitoring additional home-lab systems.
- Carefully restricted automation operations.

AI-assisted features will remain optional rather than becoming
dependencies for basic monitoring.

## Next Development Task

Inspect Project 001's existing Health Metrics collector.

Determine:

- Available measurements.
- Collection frequency.
- Storage format.
- Existing database integration.
- Simplest secure method for exposing approved measurements.

Use these findings to design the first monitoring API.