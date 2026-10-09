# Task 4: Mini Project – Robotics/Automation Proposal

**Domain:** Robotics & Automation (CodeAlpha Internship Task 4)  
**Project Title:** AI-Driven Autonomous Mobile Robots (AMRs) for Next-Generation Industrial Intralogistics & Smart Warehousing  
**Deliverables Completed:**
1. **Four-Tier AMR System Architecture Diagram:** [`architecture_diagram.png`](architecture_diagram.png)
2. **Architecture Generator Script:** [`generate_diagram.py`](generate_diagram.py)
3. **Full 6-Page Formal Engineering Proposal (PDF):** [`Task_4_AI_Robotics_Proposal.pdf`](Task_4_AI_Robotics_Proposal.pdf) (Single source of truth in code, code-computed budget and ROI model, verified references)

---

### Project Scope & Architectural Highlights
- **Hardware Architecture:** NVIDIA Jetson AGX Orin 64GB (275 TOPS), dual Sick/Keyence 360° industrial safety LiDARs, Intel RealSense D435i active stereo depth camera, dual 48V 400W planetary BLDC hub servomotors (45 Nm torque), and 48V 60Ah LiFePO4 smart battery with CANbus BMS.
- **Autonomy & Perception Stack:** ROS 2 (Jazzy Jalisco), `slam_toolbox` lifelong mapping, Extended Kalman Filter (EKF) sensor fusion (wheel odometry + IMU + scan-matching LiDAR), Ultralytics YOLOv8 TensorRT FP16 acceleration (<13 ms latency @ 80 FPS), and Timed Elastic Band (TEB) dynamic trajectory optimization.
- **Multi-Agent Fleet Coordination:** Open VDA 5050 communication interface, Conflict-Based Search (CBS) spatial-temporal intersection reservations, and AWS IoT Core digital twin telemetry.
- **Implementation Timeline:** 5-phase, 10-month Gantt milestone roadmap (M1 to M5).
- **Safety Standard:** ISO 3691-4:2023 driverless industrial truck safety verification and Category 0 protective stop fields.

### Single Source of Truth: Budget & ROI Model
- **Single-Unit Prototype R&D Budget:** Exactly **$9,178.00 USD** (computed dynamically from 7 verified commercial hardware components).
- **Turnkey Production 2-AMR Cell Deployment:**
  - Initial Capital Expenditure (CapEx): **$48,000.00 USD** (2 production units + automated docking stations + fleet server).
  - Annual Operational Baseline Replaced: 2 operators across 2 shifts (4,000 hrs/yr @ $22/hr) = **$88,000.00 / year**.
  - Annual AMR Operating Costs (OpEx): **$14,000.00 / year**.
  - Net Annual Cash Flow Savings: **$74,000.00 / year**.
  - **Payback Period:**
    $$\text{Payback Period} = \frac{\text{CapEx}}{\text{Net Annual Cash Flow}} \times 12 = \frac{\$48,000.00}{\$74,000.00/\text{yr}} \times 12 \approx 7.8\text{ months (~0.65 years)}.$$
