import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_amr_architecture(save_path):
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=180)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Title
    ax.text(5.5, 7.1, "SYSTEM ARCHITECTURE: AI-DRIVEN AUTONOMOUS MOBILE ROBOT (AMR)", fontsize=13, fontweight='bold', ha='center', color='#1E3A8A')
    ax.text(5.5, 6.75, "Four-Tier Cyber-Physical Autonomy & Cloud Fleet Management Pipeline", fontsize=9, ha='center', color='#475569')

    # Layer 4: Cloud & Fleet Management (Top)
    ax.add_patch(patches.FancyBboxPatch((0.5, 5.3), 10.0, 1.2, boxstyle="round,pad=0.06", facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.5))
    ax.text(0.8, 6.15, "TIER 4: CLOUD FLEET MANAGEMENT & IIoT WAREHOUSE INTEGRATION", fontsize=8.5, fontweight='bold', color='#1E40AF')
    ax.text(0.8, 5.6, "• Enterprise WMS/MES Interface via REST & GraphQL\n• Centralized Multi-Agent Task Dispatcher (Fleet Traffic Manager)\n• Digital Twin Visualization & Real-Time Telemetry Dashboard (MQTT / WebSockets)", fontsize=7.5, color='#1E293B')
    ax.text(9.8, 5.85, "CLOUD / ERP\nLAYER", fontsize=8, fontweight='bold', ha='center', color='#3B82F6')

    # Layer 3: ROS 2 Navigation Stack
    ax.add_patch(patches.FancyBboxPatch((0.5, 3.7), 10.0, 1.3, boxstyle="round,pad=0.06", facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=1.5))
    ax.text(0.8, 4.65, "TIER 3: EMBEDDED AUTONOMY & ROS 2 (JAZZY) NAVIGATION STACK (Nav2)", fontsize=8.5, fontweight='bold', color='#166534')
    ax.text(0.8, 4.05, "• Global Path Planner: Dijkstra / A* over Static Occupancy Grid\n• Local Planner: Timed Elastic Band (TEB) with Dynamic Obstacle Avoidance\n• Behavior Trees: Mission Sequencing, Docking Recovery, and Safe Halt Routines", fontsize=7.5, color='#1E293B')
    ax.text(9.8, 4.35, "AUTONOMY\nLAYER", fontsize=8, fontweight='bold', ha='center', color='#16A34A')

    # Layer 2: Edge AI & Perception
    ax.add_patch(patches.FancyBboxPatch((0.5, 2.1), 10.0, 1.3, boxstyle="round,pad=0.06", facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5))
    ax.text(0.8, 3.05, "TIER 2: EDGE AI PERCEPTION & STATE ESTIMATION (NVIDIA JETSON AGX ORIN)", fontsize=8.5, fontweight='bold', color='#92400E')
    ax.text(0.8, 2.45, "• Real-Time Object Detection: TensorRT YOLOv8 (Pedestrian & Forklift Identification @ 45 FPS)\n• SLAM Engine: 2D/3D LiDAR Cartographer with Loop Closure & Graph Optimization\n• Multi-Sensor Fusion: Extended Kalman Filter (EKF) combining LiDAR, IMU, and Wheel Odometry", fontsize=7.5, color='#1E293B')
    ax.text(9.8, 2.75, "EDGE AI\nLAYER", fontsize=8, fontweight='bold', ha='center', color='#D97706')

    # Layer 1: Physical Hardware & Actuation
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.4), 10.0, 1.4, boxstyle="round,pad=0.06", facecolor='#F1F5F9', edgecolor='#475569', linewidth=1.5))
    ax.text(0.8, 1.45, "TIER 1: PHYSICAL HARDWARE, SENSORS & SAFETY CHASSIS", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.text(0.8, 0.75, "• Sensors: Sick S300 2D Safety LiDARs (360°), Intel RealSense D435i RGB-D Camera, 6-Axis IMU\n• Actuation: Differential Drive High-Torque BLDC Motors (400W) with 2048-PPR Encoders\n• Safety & Power: 48V 60Ah LiFePO4 Smart BMS, Dual Hardware Emergency Stop, ISO 3691-4 PLC", fontsize=7.5, color='#334155')
    ax.text(9.8, 1.1, "HARDWARE\nLAYER", fontsize=8, fontweight='bold', ha='center', color='#475569')

    # Interconnecting arrows
    for y in [1.8, 3.4, 5.0]:
        ax.annotate('', xy=(5.5, y + 0.3), xytext=(5.5, y),
                    arrowprops=dict(facecolor='#1E3A8A', edgecolor='#1E3A8A', width=2, headwidth=7))
        ax.annotate('', xy=(5.8, y), xytext=(5.8, y + 0.3),
                    arrowprops=dict(facecolor='#0D9488', edgecolor='#0D9488', width=2, headwidth=7))

    ax.text(6.2, 1.95, "CAN 2.0B / EtherCAT", fontsize=7, color='#64748B', family='monospace')
    ax.text(6.2, 3.55, "ROS 2 DDS Middleware", fontsize=7, color='#64748B', family='monospace')
    ax.text(6.2, 5.15, "Industrial Wi-Fi 6 / MQTT", fontsize=7, color='#64748B', family='monospace')

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved architecture diagram: {save_path}")

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    draw_amr_architecture(os.path.join(here, "architecture_diagram.png"))
