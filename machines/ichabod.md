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

## Validation

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