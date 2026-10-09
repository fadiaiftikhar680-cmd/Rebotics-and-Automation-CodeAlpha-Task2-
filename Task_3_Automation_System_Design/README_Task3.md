# Task 3: Automation System Design

**Domain:** Robotics & Automation (CodeAlpha Internship Task 3)  
**System Title:** Industrial Conveyor Sorting & Packaging Automation System  
**Deliverables Completed:**
1. **System Automation Flowchart:** [`flowchart_packaging_system.png`](flowchart_packaging_system.png) (Finite State Machine with canonical S1–S6 sensors, dual reject loops returning to rework, and E-Stop safety interrupt)
2. **Electrical & Control System Circuit Schematic:** [`circuit_diagram_automation.png`](circuit_diagram_automation.png) (Unified wiring schematic with 230V AC mains, MCB, 24V SMPS, Pilz PNOZ X3 safety relay, S7-1200 CPU 1214C DC/DC/DC terminals, 3-wire PNP sensors, and solenoid flyback diodes)
3. **Diagram Generator Script:** [`generate_diagrams.py`](generate_diagrams.py)
4. **Complete 3-Page Engineering Explanation Report (PDF):** [`Task_3_Automation_System_Design_Report.pdf`](Task_3_Automation_System_Design_Report.pdf) (Single source of truth in code, code-computed BOM, and sizing calculations)

---

### Canonical Sensor and Actuator Mapping Table (Single Source of Truth)
| Device Tag | Hardware Signal | Component Model | Functional Logic |
| :---: | :---: | :---: | :---: |
| **S1** | `%I0.0` (24V DI) | Omron E3Z-T61 Through-Beam Optical | Infeed presence detection / cycle initiation |
| **S2** | `%I0.1` (24V DI) | Omron E2B-M12KS04 Inductive Proximity | Metallic seal / foil cap presence confirmation |
| **S3** | `%I0.2` (24V DI) | Banner Q4X Optical Color / Contrast | Label color verification (Pass / Fail) |
| **S4** | `%IW64` (0–10V AI0) | Pepperl+Fuchs UB500 Ultrasonic Distance | Continuous height gauging (Tolerance 95–105 mm) |
| **S5** | `%IW66` (0–10V AI1) | TEDEA 1022 Load Cell + 0–10V Transmitter | Dynamic gross mass verification (Target: 250g ± 5g) |
| **S6** | `%I0.3` (24V DI) | Omron E3Z-R61 Retro-Reflective Barrier | Exit packaging confirmation & batch counter |
| **PNOZ** | `%I0.4` (24V DI) | Pilz PNOZ X3 Auxiliary Contact | Safety monitoring loop (1 = Normal, 0 = E-Stop) |
| **VFD Run** | `%Q0.0` (Transistor) | Interposing Relay K1 ➔ SINAMICS V20 DI1 | Conveyor motor start / stop command |
| **VFD Speed**| `%Q0.1` (Transistor) | Interposing Relay K2 ➔ SINAMICS V20 DI2 | Preset speed selection (Activates 50 Hz preset) |
| **Pusher 1**| `%Q0.2` (Transistor) | Festo 24V Solenoid Valve 1 + 1N4007 Diode | Ejects Height / Color / Metal rejects to rework |
| **Pusher 2**| `%Q0.3` (Transistor) | Festo 24V Solenoid Valve 2 + 1N4007 Diode | Ejects out-of-spec weight items to rework |
| **Heater** | `%Q0.4` (Transistor) | Solid State Relay Fotek SSR-25DA | Pulses 230V cartoner heating wire (1.2 s) |
| **Green Light**| `%Q0.5` (Transistor) | Patlite LR4 24V Green Indicator | Illuminates during active automatic cycle |
| **Red Light**| `%Q0.6` (Transistor) | Patlite LR4 24V Red Indicator + 85 dB Siren | Safety fault / Jam / E-Stop trip alarm |

---

### Sizing and Performance Metrics
- **Nominal Production Throughput:**
  $$\text{Throughput} = \frac{v}{p} \times 60 = \frac{0.20\text{ m/s}}{0.40\text{ m}} \times 60 = 30\text{ units/minute}$$
- **Burst Throughput:** 36 units/minute (based on 0.8 s sensor dwell time).
- **Turnkey Hardware Bill of Materials (BOM):** Exactly **$1,878.00 USD** (computed dynamically from 17 verified commercial components).
- **Safety Standard:** Target Performance Level PL d, Category 3 architecture per ISO 13849-1, subject to formal task-based risk assessment.
