# Task 2: Robotic Arm Simulation & Kinematics Modeling

**Domain:** Robotics & Automation (CodeAlpha Internship Task 2)  
**Deliverables Completed:**
1. **Interactive 3D Simulation Web App (100% Offline):** [`interactive_3d_arm.html`](interactive_3d_arm.html) (Bundled with local `three.min.js` and `OrbitControls.js` for full offline execution)
2. **CAD Models (Solid Binary STL & Multi-Part OBJ):** Located in [`cad_models/`](cad_models/)
   - `01_base_pedestal.stl` (Stepped mounting flange & hub, 384 facets)
   - `02_shoulder_turret_link.stl` (Azimuthal column with clevis fork and joint bore, 344 facets)
   - `03_upper_arm_link.stl` (Main beam L2 = 25.0 cm with shoulder & elbow boss, 268 facets)
   - `04_forearm_link.stl` (Forearm link L3 = 20.0 cm with elbow & wrist boss, 268 facets)
   - `05_end_effector_gripper.stl` (Parallel pneumatic gripper L4 = 10.0 cm, 176 facets)
   - `robotic_arm_assembly.stl` (Complete 5-part solid assembly in home pose, 1,440 facets)
   - `robotic_arm_assembly.obj` (Wavefront OBJ with 5 distinct named groups)
3. **Rigorous Kinematics Verification Script:** [`verify_kinematics.py`](verify_kinematics.py) (Asserts IK -> FK position error < 1.0 mm and 0 joint limit violations across all 42 trajectory steps)
4. **Simulation Snapshots & Trajectory Plots:** Located in [`screenshots/`](screenshots/)
   - `01_home_state.png`
   - `02_approach_and_pick.png`
   - `03_lift_and_transfer.png`
   - `04_place_and_release.png`
   - `05_full_trajectory_and_kinematics.png`
5. **Animated Simulation GIF:** [`pick_and_place_simulation.gif`](pick_and_place_simulation.gif)
6. **Technical Engineering PDF Report:** [`Task_2_Robotic_Arm_Simulation_Report.pdf`](Task_2_Robotic_Arm_Simulation_Report.pdf) (Exactly 4 pages, clean typography, verification table, DH model)

---

### Unit Convention & Kinematic Specifications
- **Unit Convention:** Metric centimeters [cm] for spatial coordinates (1 unit = 1.0 cm = 10.0 mm), angles in degrees [°].
- **Kinematic Lengths:**
  - Base Height ($L_1$): $15.0\text{ cm}$
  - Upper Arm ($L_2$): $25.0\text{ cm}$
  - Forearm ($L_3$): $20.0\text{ cm}$
  - End-Effector ($L_4$): $10.0\text{ cm}$
  - Maximum Radial Reach: $55.0\text{ cm}$ ($550\text{ mm}$)
- **Degrees of Freedom (DOF):**
  - **Joint 1 (Base Turret):** Revolute, Yaw axis (Rotation around Z), Range: -180° to +180°
  - **Joint 2 (Shoulder):** Revolute, Pitch axis (Elevation), Range: -30° to +110°
  - **Joint 3 (Elbow):** Revolute, Pitch axis, Range: -120° to +120°
  - **Joint 4 (Wrist):** Revolute, Pitch axis, Range: -90° to +90°
  - **End-Effector:** Two-finger linear gripper (0 to 4.0 cm stroke)

### Denavit-Hartenberg (DH) Parameters
| Link $i$ | Link Length $a_i$ | Twist $\alpha_i$ | Offset $d_i$ | Joint Angle $\theta_i$ |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 0.0 cm | +90° | 15.0 cm | $\theta_1$ (Variable) |
| 2 | 25.0 cm | 0° | 0.0 cm | $\theta_2$ (Variable) |
| 3 | 20.0 cm | 0° | 0.0 cm | $\theta_3$ (Variable) |
| 4 | 10.0 cm | 0° | 0.0 cm | $\theta_4$ (Variable) |

### Quantitative Kinematics Validation
Run `python verify_kinematics.py`:
- **Pick Grasp Target $(24, 16, 4)\text{ cm}$:** Solved $(\theta_1=33.7^\circ, \theta_2=42.5^\circ, \theta_3=-106.8^\circ, \theta_4=-15.7^\circ) \implies \text{Error} = 0.0000\text{ mm}$
- **Place Target $( -18, 25, 4)\text{ cm}$:** Solved $(\theta_1=125.8^\circ, \theta_2=40.3^\circ, \theta_3=-100.3^\circ, \theta_4=-20.0^\circ) \implies \text{Error} = 0.0000\text{ mm}$
- **Trajectory Steps:** 42 / 42 verified with zero joint limit violations.
