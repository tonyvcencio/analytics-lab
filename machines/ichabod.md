# Ichabod

## Role

Headless Linux server for databases, automation, services, storage, and remote analytics workloads.

## Hardware

Ichabod is an assembled, operational headless Linux server built primarily from secondhand components.

### Installed Components

| Component | Specification | Condition / Source | Cost |
|---|---|---|---:|
| CPU | Intel Core i3-12100T (4 cores / 8 threads) | Used - Ebay | $96.30 |
| Motherboard | MSI PRO B760M-P DDR4 | Used - Mint - Amazon Resale | $100.63 |
| Memory | Samsung 8GB DDR4-3200 | Used - Ebay | $32.62 |
| CPU Cooler | ARCTIC Freezer 36 | New - Ebay | $32.09 |
| Power Supply | Lian Li 550W | New - Amazon | $55.58 |
| Primary SSD | Samsung PM9B1 256GB NVMe | New - Amazon | $74.89 |
| Secondary SSD | Kingston NV2 500GB NVMe (Sr. Gimperihno) | Used - Ebay | $55.74 |
| Case | Cooler Master MasterBox Q300L V1 | Used - Mint - Amazon Resale | $27.81 |
| **Total** | | | **$475.66** |

### Accounting Notes

- Costs include applicable sales tax and shipping.
- Tax on the mixed Amazon order was allocated proportionally.
- Initial hardware investment is tracked separately from future upgrades.
- Component condition reflects the condition at purchase.
- Sr. Gimperihno refers to the Kingston NV2 500GB SSD.

## Operating System

- Distribution: Ubuntu Server 24.04.5 LTS
- Kernel at initial validation: 6.8.0-146-generic
- Architecture: x86_64
- Administration: Headless, primarily over SSH
- Network: Wired Ethernet

## Core Services

Planned capabilities include:

- SSH
- Git
- Python
- SQL Databases
- Scheduled jobs
- Containerized services
- Remote development

## Administration

Ichabod will be administered primarily from Nomad and Mac over SSH.

## Storage

Ubuntu Server is installed on the Samsung PM9B1 256GB NVMe SSD. The Kingston NV2 500GB NVMe SSD (Sr. Gimperihno) is reserved for secondary, noncritical workloads. Its filesystem and mounting configuration have not yet been established.

### Primary Storage Layout

- Primary device: Samsung PM9B1 256GB NVMe (`nvme0n1`)
- Usable device capacity: approximately 238.5 GiB
- Ubuntu installed using Logical Volume Manager (LVM)
- EFI system partition: approximately 1 GiB
- Boot partition: approximately 2 GiB
- LVM physical volume: approximately 235.4 GiB
- Root logical volume: approximately 100 GiB
- Remaining volume-group capacity has not yet been allocated
- Future storage allocation strategy remains undecided

## Validation

**Initial hardware commissioning completed: October 11, 2026.**

All completed initial hardware diagnostics passed.

Commissioning established a baseline for CPU stability, memory operation,
NVMe health, thermal performance, and operating-system reliability.

These results do not constitute exhaustive hardware certification.
Additional long-duration testing and secondary-storage validation remain
future tasks.

- [x] Hardware assembled
- [x] POST successful
- [x] Linux Ubuntu 24.04.5 LTS installed
- [x] Wired network configured
- [x] SSH server enabled
- [x] Mac SSH authentication verified
- [ ] Nomad SSH key authentication
- [ ] Git configured
- [ ] Python environment validated
- [ ] Database service validated

### Hardware Diagnostics

- [x] CPU identified: Intel Core i3-12100T (4 cores / 8 threads)
- [x] CPU stress test completed: 5 minutes, 8 workers, 0 failures
- [x] Memory identified: Samsung 8GB DDR4-3200
- [x] Memory testing completed: 3 passes, no errors
- [x] Samsung PM9B1 NVMe SMART health checked
- [x] Kingston NV2 NVMe SMART health checked
- [x] Kingston NV2 short self-test passed
- [x] Kingston NV2 extended self-test passed
- [x] System temperatures inspected
- [x] Kernel error logs reviewed

#### CPU Stress and Thermal Validation

Test performed: October 11, 2026.

- Processor: Intel Core i3-12100T
- Physical cores: 4
- Logical threads: 8
- Test utility: `stress-ng`
- Workload: Matrix multiplication
- CPU workers: 8
- Duration: 300 seconds
- Workers passed: 8
- Workers failed: 0
- Total reported operations: 2,805,817
- Reported operations per second: 9,352.66
- Observed CPU package temperature before testing: 32°C
- Observed CPU package temperature during testing: 46°C
- Observed CPU package temperature after testing: 35°C
- Kernel warnings/errors during final inspection: None reported

**Result: PASS**

The ARCTIC Freezer 36 maintained low observed CPU temperatures
during the workload.

The recorded 46°C temperature represents an observation during
testing, not a verified maximum temperature.

#### Storage Health Notes

- Samsung PM9B1: No media errors reported during initial SMART inspection.
- Kingston NV2 (Sr. Gimperihno): Approximately 17,159 power-on hours
  and 84 unsafe shutdowns at initial inspection.
- Kingston SMART reported no media errors, although historical NVMe
  error-log entries were present.
- Kingston short and extended NVMe self-tests completed successfully.
- Secondary storage is designated for noncritical workloads until
  its long-term reliability is established.

### Outstanding Configuration

- [ ] Establish server directory structure
- [ ] Configure SQL environment
- [ ] Establish storage strategy for Sr. Gimperihno
- [ ] Configure scheduled maintenance and monitoring
- [ ] Establish backup procedures
- [ ] Review and apply outstanding Ubuntu package updates
- [ ] Evaluate available firmware updates
- [ ] Review and allocate unused LVM capacity
- [ ] Perform controlled read/write testing on secondary SSD


## Rabbit R1 Integration

### Phase 1 — Agent Installation and Connectivity

**Completed: October 13, 2026**

Rabbit R1 running Rabbit OS3 was successfully connected to Ichabod
through the official Rabbit computer agent.

The integration establishes a foundation for future voice-controlled
server monitoring, analytics operations, and automation.

### Configuration

| Component | Configuration |
|---|---|
| Device | Rabbit R1 |
| Operating System | Rabbit OS3 |
| AI Provider | OpenRouter |
| Agent Version | rabbit-agent 0.1.16 |
| Host System | Ichabod — Ubuntu Server 24.04.5 LTS |
| Service Account | rabbit-agent |
| Account UID/GID | 1001 / 1001 |
| Installation Directory | /home/rabbit-agent/.rabbit-agent |
| Connection | Rabbit Cloud |
| Connection Status | Confirmed through Rabbit Hole |

### Security and Isolation

A dedicated, nonadministrative Linux account was created specifically
for the Rabbit computer agent.

- [x] Dedicated rabbit-agent account created
- [x] Separate home directory established
- [x] Account confirmed without sudo privileges
- [x] Home directory write access verified
- [x] Access to administrator SSH directory listing denied
- [x] Installer reviewed before execution
- [x] Installer includes cryptographic verification mechanisms
- [x] Agent installed without elevated privileges
- [x] Rabbit Hole connection confirmed
- [x] Automatic workspace exploration deferred

Account separation provides a basic security boundary but does not
constitute complete filesystem or network isolation.

The agent executable itself has not undergone a comprehensive
security audit.

### Background Maintenance

The Rabbit installer configures user-level cron scheduling:

- At system reboot: run Rabbit maintenance script
- Every 10 minutes: run Rabbit maintenance script

Scheduled command:

`/home/rabbit-agent/.rabbit-agent/install.sh`

The installer supports automatic updates and agent startup.

### API Configuration

Rabbit OS3 was configured with OpenRouter as its AI provider.

Free-model variants were selected for initial experimentation.

The OpenRouter API key was configured with a $50 spending allowance.
This allowance is not prepaid credit and does not indicate actual
expenditure.

API usage and billing should be reviewed before expanding usage.

No API credentials or pairing tokens are stored in this repository.

### Phase 1 Results

- [x] Rabbit OS3 onboarding completed
- [x] OpenRouter provider configured
- [x] Dedicated Linux account established
- [x] Rabbit Agent v0.1.16 installed
- [x] Agent startup successful
- [x] Ichabod connection confirmed in Rabbit Hole
- [ ] Agent process ownership independently verified
- [ ] Scheduled cron entries independently verified
- [ ] Rabbit-to-Ichabod command execution tested
- [ ] Health metrics integration implemented

**Result: PHASE 1 COMPLETE — CONNECTION ESTABLISHED**

### Phase 2 — Planned Integration

The next objective is to provide Rabbit R1 with controlled,
read-only access to Ichabod's existing health-metrics collector.

Planned capabilities include:

- Retrieve current CPU utilization
- Retrieve memory utilization
- Retrieve disk usage
- Report system uptime
- Summarize server health through Rabbit R1

Future access should remain limited to explicitly approved
operations and directories.

No server health integration has been implemented yet.