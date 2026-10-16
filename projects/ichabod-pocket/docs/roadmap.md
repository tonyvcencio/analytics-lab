# Ichabod Pocket — Development Roadmap

**Project 004 | Roadmap v0.1**

**Established:** October 16, 2026

**Current Phase:** Foundation and Integration Validation

## Project Vision

Transform the Rabbit R1 into a portable interface for monitoring
Ichabod University and interacting with selected analytics services.

Routine monitoring should be fast, secure, and independent of
large language model inference.

AI-assisted operations will be developed as optional enhancements.

---

## Phase 0 — Foundation and Integration

**Status: In Progress**

### Completed

- [x] Configure Rabbit OS3.
- [x] Configure OpenRouter as AI provider.
- [x] Install Rabbit Agent on Ichabod.
- [x] Establish Rabbit Cloud connection.
- [x] Verify dedicated Linux service account.
- [x] Verify agent process ownership.
- [x] Verify agent cron configuration.
- [x] Inspect OS3 command permission scope.
- [x] Deny persistent broad command-execution permission.
- [x] Demonstrate Rabbit R1 internet connectivity.
- [x] Demonstrate browser-to-device conversational continuity.
- [x] Identify Linux thermal sensors.
- [x] Independently validate thermal readings.

### Remaining

- [ ] Rotate previously exposed Rabbit Agent connection token.
- [ ] Verify the exact OS3-to-Ichabod command-execution pathway.
- [ ] Investigate intermittent physical R1 AI connectivity errors.
- [ ] Benchmark alternative free OpenRouter models.

### Exit Criteria

The existing integration is documented, security follow-ups are
addressed, and the monitoring architecture is ready for implementation.

---

## Phase 1 — Monitoring API

**Status: Planned**

### Objectives

Develop a lightweight, authenticated, read-only interface for
retrieving system health information from Ichabod.

### Tasks

- [ ] Review Project 001 Health Metrics collector.
- [ ] Identify existing measurements and data formats.
- [ ] Review collector frequency and storage.
- [ ] Identify existing DuckDB integration.
- [ ] Define monitoring API requirements.
- [ ] Select a lightweight Python API framework.
- [ ] Implement server availability endpoint.
- [ ] Implement CPU utilization endpoint.
- [ ] Implement CPU package temperature endpoint.
- [ ] Implement memory utilization endpoint.
- [ ] Implement disk utilization endpoint.
- [ ] Implement system uptime endpoint.
- [ ] Implement consolidated health summary.
- [ ] Add authentication and access restrictions.
- [ ] Test API locally on Ichabod.
- [ ] Validate measurements against Ubuntu.

### Exit Criteria

A restricted API can reliably provide accurate system
measurements without arbitrary shell execution.

---

## Phase 2 — Rabbit Creation Dashboard

**Status: Planned**

### Objectives

Build a dedicated Rabbit Creation capable of displaying
Ichabod's system health information.

### Tasks

- [ ] Verify Rabbit Creations networking capabilities.
- [ ] Determine supported authentication mechanisms.
- [ ] Establish secure access to the monitoring API.
- [ ] Design a compact dashboard interface.
- [ ] Display CPU package temperature.
- [ ] Display CPU utilization.
- [ ] Display memory utilization.
- [ ] Display disk utilization.
- [ ] Display system uptime.
- [ ] Display server connection status.
- [ ] Implement manual refresh.
- [ ] Test on the physical Rabbit R1.
- [ ] Evaluate performance and usability.

### Exit Criteria

The Rabbit R1 displays current measurements retrieved
from Ichabod without requiring LLM inference.

---

## Phase 3 — Analytics Integration

**Status: Future**

### Objectives

Expand Ichabod Pocket beyond basic system monitoring
to provide visibility into analytics operations.

### Tasks

- [ ] Display Project 001 collector status.
- [ ] Display recent collection timestamps.
- [ ] Display analytics pipeline status.
- [ ] Display recent pipeline execution results.
- [ ] Identify failed or delayed jobs.
- [ ] Add historical metrics summaries.
- [ ] Explore integration with additional projects.

### Exit Criteria

Ichabod Pocket provides useful operational information
about both the server and its analytics workloads.

---

## Phase 4 — Voice and AI Integration

**Status: Experimental**

### Objectives

Introduce optional natural-language interaction and
AI-assisted analysis without compromising the security
or responsiveness of basic monitoring.

### Tasks

- [ ] Evaluate reliable free OpenRouter models.
- [ ] Benchmark model response times.
- [ ] Investigate local AI inference options.
- [ ] Develop natural-language health summaries.
- [ ] Explore voice-based metrics requests.
- [ ] Define approved automation operations.
- [ ] Implement explicit authorization for sensitive actions.
- [ ] Test failure handling and permission boundaries.

### Exit Criteria

Voice and AI features provide additional functionality
without becoming dependencies for routine monitoring.

---

## Preliminary Performance Targets

| Operation | Target |
|---|---|
| Dashboard startup | Under 3 seconds |
| Metrics refresh | Under 2 seconds |
| Basic AI response | Under 10 seconds |
| Complex AI response | Under 30 seconds |

These are initial design targets and have not been benchmarked.

---

## Development Priorities

**Priority 1:** Security and reliable monitoring.

**Priority 2:** Functional Rabbit Creation dashboard.

**Priority 3:** Analytics integration.

**Priority 4:** Voice interaction and advanced automation.

## Next Development Session

1. Inspect Project 001 Health Metrics collector.
2. Identify existing metrics and storage formats.
3. Determine how to expose approved measurements.
4. Design the first restricted monitoring API.

The first implementation milestone is:

**Ichabod Pocket v0.1 — Server Health Dashboard**