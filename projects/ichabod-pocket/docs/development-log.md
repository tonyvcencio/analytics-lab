# Ichabod Pocket — Development Log

**Project 004 | Development History**

## October 13, 2026 — Initial Rabbit Integration

### Objective

Connect the Rabbit R1 ecosystem to Ichabod, establishing a
foundation for remote server monitoring and future automation.

### Infrastructure

| Component | Configuration |
|---|---|
| Device | Rabbit R1 |
| Operating System | Rabbit OS3 |
| Server | Ichabod |
| Server OS | Ubuntu Server 24.04.5 LTS |
| Processor | Intel Core i3-12100T |
| Memory | 8 GB DDR4 |
| Agent | rabbit-agent 0.1.16 |
| Service Account | rabbit-agent |
| AI Provider | OpenRouter |

### Implementation

Installed the Rabbit computer agent under a dedicated Linux
service account.

Agent installation directory:

`/home/rabbit-agent/.rabbit-agent`

The account was configured without administrator privileges.

Rabbit Hole confirmed connectivity between Rabbit Cloud
and Ichabod.

### Outcome

**Initial Rabbit Agent integration established.**

The agent connection provides a foundation for exploring
computer interaction through Rabbit OS3.

---

## October 16, 2026 — Agent Verification

### Objective

Confirm that the agent operates under the intended Linux
account and document its maintenance configuration.

### Process Verification

Independent process inspection identified two running
Rabbit Agent processes.

Both were owned by the `rabbit-agent` service account.

The observed parent process had PPID 1.

### Cron Configuration

The service account's crontab contained:

```cron
@reboot /home/rabbit-agent/.rabbit-agent/install.sh >/dev/null 2>&1
*/10 * * * * /home/rabbit-agent/.rabbit-agent/install.sh >/dev/null 2>&1
```

These entries schedule the installation or maintenance script
at startup and every ten minutes.

The entries were verified, but successful execution of every
scheduled run was not independently established.

### Outcome

**Agent process ownership and cron configuration verified.**

---

## October 16, 2026 — Security Review

### Objective

Evaluate the permissions requested by Rabbit OS3 before
allowing computer interaction.

### Observation

Rabbit OS3 requested permission to execute commands on
Ichabod.

The permission was persistent and applied across the
computer rather than being limited to one operation.

### Decision

**The broad permission request was denied.**

Although the agent runs under a nonadministrative Linux
account, that restriction alone does not guarantee
complete isolation.

Routine monitoring should not require arbitrary
shell command execution.

### Security Follow-Up

During earlier process inspection, a Rabbit Agent
connection token appeared in command-line arguments.

The token itself is intentionally excluded from this log.

**Action required:** Rotate the exposed token through
the supported Rabbit Agent pairing process.

Future diagnostics should avoid printing process
arguments containing credentials.

---

## October 16, 2026 — OpenRouter Diagnostics

### Objective

Investigate slow or unsuccessful AI requests through
Rabbit OS3.

### Observations

The physical Rabbit R1 initially returned network errors
when attempting AI requests.

The errors occurred on both home Wi-Fi and an iPhone
hotspot.

An existing Rabbit Creation successfully streamed live
radio through the device's speaker.

This demonstrated that at least some device network
functions were operational.

The OS3 browser interface also responded to requests,
although latency varied significantly.

### OpenRouter Results

| Model | HTTP Status | Duration |
|---|---|---|
| Nemotron 3.5 Lightning (free) | 200 | 2.1 seconds |
| Nemotron 3 Ultra (free) | 524 | 300 seconds |

The Ultra request experienced an upstream timeout.

The Lightning request completed successfully.

These results represent individual observed requests,
not comprehensive model benchmarks.

### Outcome

OpenRouter connectivity was demonstrated, but physical
R1 AI reliability remains inconsistent.

The root cause has not been established.

---

## October 16, 2026 — Thermal Monitoring Validation

### Objective

Determine whether Rabbit OS3 could report genuine
system measurements from Ichabod.

### Rabbit OS3 Observations

The OS3 browser interface reported:

- `thermal_zone0`: 27.8°C
- `thermal_zone1`: 31.0°C

A subsequent physical Rabbit R1 response reported:

- `thermal_zone0`: 27.8°C
- `thermal_zone1`: 30.0°C

The physical device appeared to reuse information
from the shared OS3 conversation.

### Independent Ubuntu Verification

Executed directly on Ichabod:

```bash
for zone in /sys/class/thermal/thermal_zone*; do
    printf '%s: ' "$(basename "$zone")"
    cat "$zone/temp"
done
```

Observed output:

```text
thermal_zone0: 27800
thermal_zone1: 30000
```

Linux reports these values in thousandths of a
degree Celsius.

Therefore:

- `27800` = 27.8°C
- `30000` = 30.0°C

### Sensor Identification

Executed:

```bash
for zone in /sys/class/thermal/thermal_zone*; do
    printf '%s: ' "$(basename "$zone")"
    cat "$zone/type"
done
```

Observed output:

```text
thermal_zone0: acpitz
thermal_zone1: x86_pkg_temp
```

### Verified Sensors

| Sensor | Type | Temperature |
|---|---|---|
| thermal_zone0 | ACPI thermal zone | 27.8°C |
| thermal_zone1 | Intel CPU package | 30.0°C |

### Interpretation

The reported temperatures were independently
corroborated against Ichabod's actual sensors.

However, the exact command-execution pathway used
by Rabbit OS3 was not independently verified.

The physical Rabbit response also demonstrated
conversational continuity, but did not conclusively
establish fresh command execution from the device.

### Outcome

**Thermal measurements independently validated.**

This provides an initial foundation for a dedicated
server-monitoring interface.

---

## October 16, 2026 — Project 004 Established

### Project Name

**Ichabod Pocket**

### Objective

Develop a custom Rabbit Creation providing secure,
lightweight access to system monitoring and selected
analytics operations on Ichabod.

### Architecture Decision

Routine monitoring will use a proposed restricted,
read-only API rather than depend on AI inference
or unrestricted Rabbit Agent command execution.

### Related Infrastructure

Project 001 — Health Metrics Analytics

The existing collector will be evaluated for reuse.

### Initial Deliverables

- Project README
- System architecture document
- Development roadmap
- Development log
- Updated Ichabod machine documentation

### Next Development Session

Review the existing Project 001 collector.

Identify available metrics, storage formats, and
the simplest secure method for exposing approved
measurements to a Rabbit Creation.

**Next milestone: Ichabod Pocket v0.1 — Server Health Dashboard**
