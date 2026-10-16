# Project 004 — Ichabod Pocket

**Rabbit R1 × Ichabod University**

## Overview

Ichabod Pocket is a custom application being developed for the
Rabbit R1, providing portable access to system monitoring,
analytics operations, and selected services hosted on Ichabod.

The project combines Rabbit OS3, Rabbit Creations, Python,
and the existing Health Metrics Analytics infrastructure.

Its primary objective is to provide a lightweight interface
for interacting with Ichabod without requiring AI inference
for routine monitoring operations.

## Infrastructure

| Component | Configuration |
|---|---|
| Device | Rabbit R1 |
| Operating System | Rabbit OS3 |
| Server | Ichabod |
| Server OS | Ubuntu Server 24.04.5 LTS |
| Processor | Intel Core i3-12100T |
| Memory | 8 GB DDR4 |
| Existing Monitoring | Project 001 — Health Metrics |
| Computer Agent | rabbit-agent 0.1.16 |
| AI Provider | OpenRouter |
| Application Platform | Rabbit Creations |

## Project Objectives

1. Develop a dedicated Rabbit R1 monitoring dashboard.
2. Retrieve real-time system measurements from Ichabod.
3. Reuse the existing Health Metrics infrastructure.
4. Implement secure, read-only access to server information.
5. Minimize dependence on cloud AI inference.
6. Explore optional voice-controlled server operations.
7. Document the implementation as a portfolio project.

## Planned Monitoring Capabilities

- CPU package temperature
- CPU utilization
- Memory utilization
- Disk utilization
- System uptime
- Server availability
- Analytics pipeline status

## Development Status

**Project established:** October 16, 2026

**Current phase:** Planning and integration validation

### Completed

- [x] Rabbit OS3 configured.
- [x] Rabbit Agent installed on Ichabod.
- [x] Dedicated Linux service account established.
- [x] Agent process ownership independently verified.
- [x] Agent cron configuration independently verified.
- [x] Rabbit Hole connection confirmed.
- [x] Physical Rabbit R1 internet connectivity demonstrated.
- [x] Browser-to-R1 conversational continuity demonstrated.
- [x] Thermal measurements independently validated.

### Pending

- [ ] Verify Rabbit-to-Ichabod command execution.
- [ ] Rotate previously exposed Rabbit Agent connection token.
- [ ] Review Project 001's Health Metrics collector.
- [ ] Design a restricted monitoring API.
- [ ] Implement authenticated read-only access.
- [ ] Develop the Rabbit Creation dashboard.
- [ ] Test live metrics retrieval on the physical R1.
- [ ] Benchmark faster free AI models.

## Verified Thermal Sensors

Initial validation completed October 16, 2026.

| Sensor | Linux Type | Verified Temperature |
|---|---|---|
| thermal_zone0 | acpitz | 27.8°C |
| thermal_zone1 | x86_pkg_temp | 30.0°C |

The readings were independently verified through Ubuntu.

The `x86_pkg_temp` sensor represents the Intel CPU package
temperature.

The `acpitz` sensor represents an ACPI firmware-defined
thermal zone.

## Related Projects

### Project 001 — Health Metrics Analytics

Ichabod Pocket will reuse the existing Python-based
system monitoring infrastructure developed for Project 001.

The objective is to consume existing metrics rather than
create a competing monitoring system.

## Security Principles

- No unrestricted administrator access.
- No API credentials or pairing tokens stored in GitHub.
- No arbitrary shell execution required for routine monitoring.
- Monitoring interfaces should expose only approved operations.
- Authentication and secure transport must be established
  before exposing server information remotely.

## Documentation

- [Architecture](docs/architecture.md)
- [Development Roadmap](docs/roadmap.md)
- [Development Log](docs/development-log.md)

## Next Milestone

**Ichabod Pocket v0.1 — Server Health Dashboard**

Develop a lightweight Rabbit Creation capable of displaying
live system measurements retrieved from Ichabod through
a restricted, read-only monitoring interface.