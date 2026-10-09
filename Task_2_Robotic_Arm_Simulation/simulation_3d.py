import os
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

# Link lengths in centimeters
L1 = 15.0  # Base to shoulder height
L2 = 25.0  # Upper arm length
L3 = 20.0  # Forearm length
L4 = 10.0  # Wrist to end-effector

def forward_kinematics(theta1, theta2, theta3, theta4):
    """
    Computes joint positions given angles in degrees.
    theta1: Base yaw (-180 to 180)
    theta2: Shoulder pitch (-30 to 120)
    theta3: Elbow pitch (-120 to 120)
    theta4: Wrist pitch (-90 to 90)
    """
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    t3 = np.radians(theta3)
    t4 = np.radians(theta4)

    # Base at origin
    p0 = np.array([0.0, 0.0, 0.0])
    
    # Joint 1: Base turret / shoulder pivot
    p1 = np.array([0.0, 0.0, L1])

    # Shoulder to elbow (in arm plane)
    r2 = L2 * np.cos(t2)
    z2 = L1 + L2 * np.sin(t2)
    p2 = np.array([r2 * np.cos(t1), r2 * np.sin(t1), z2])

    # Elbow to wrist
    angle23 = t2 + t3
    r3 = r2 + L3 * np.cos(angle23)
    z3 = z2 + L3 * np.sin(angle23)
    p3 = np.array([r3 * np.cos(t1), r3 * np.sin(t1), z3])

    # Wrist to Tool Center Point (TCP)
    angle234 = angle23 + t4
    r4 = r3 + L4 * np.cos(angle234)
    z4 = z3 + L4 * np.sin(angle234)
    p4 = np.array([r4 * np.cos(t1), r4 * np.sin(t1), z4])

    return [p0, p1, p2, p3, p4]

def inverse_kinematics(target_x, target_y, target_z, wrist_angle_deg=-45.0):
    """
    Analytical Inverse Kinematics for 4-DOF articulated arm.
    Solves for theta1, theta2, theta3, theta4 to place TCP at (target_x, target_y, target_z).
    """
    theta1 = np.degrees(np.arctan2(target_y, target_x))
    r_target = np.sqrt(target_x**2 + target_y**2)
    z_target = target_z

    psi = np.radians(wrist_angle_deg)
    # Wrist position (p3)
    r_wrist = r_target - L4 * np.cos(psi)
    z_wrist = z_target - L4 * np.sin(psi)

    # Distance from shoulder (p1: 0, L1) to wrist
    dr = r_wrist
    dz = z_wrist - L1
    D = np.sqrt(dr**2 + dz**2)

    # Check reachability
    if D > (L2 + L3) * 0.999:
        D = (L2 + L3) * 0.999
    if D < abs(L2 - L3):
        D = abs(L2 - L3) + 0.01

    # Law of cosines for elbow
    cos_theta3 = (D**2 - L2**2 - L3**2) / (2.0 * L2 * L3)
    cos_theta3 = np.clip(cos_theta3, -1.0, 1.0)
    theta3_rad = -np.arccos(cos_theta3) # Elbow up configuration

    # Shoulder angle
    alpha = np.arctan2(dz, dr)
    beta = np.arctan2(L3 * np.sin(-theta3_rad), L2 + L3 * np.cos(theta3_rad))
    theta2_rad = alpha + beta

    theta2 = np.degrees(theta2_rad)
    theta3 = np.degrees(theta3_rad)
    theta4 = wrist_angle_deg - (theta2 + theta3)

    return theta1, theta2, theta3, theta4

def draw_cylinder(ax, p_start, p_end, radius=1.6, color='#2563EB', alpha=0.9):
    """Draws a 3D cylindrical link between two points."""
    v = p_end - p_start
    length = np.linalg.norm(v)
    if length < 1e-4:
        return
    v_norm = v / length

    # Construct orthogonal basis
    not_v = np.array([1, 0, 0]) if abs(v_norm[0]) < 0.8 else np.array([0, 1, 0])
    n1 = np.cross(v_norm, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_norm, n1)

    theta = np.linspace(0, 2*np.pi, 16)
    s = np.linspace(0, length, 4)
    Theta, S = np.meshgrid(theta, s)

    X = p_start[0] + S * v_norm[0] + radius * (np.outer(np.ones(len(s)), np.cos(theta)) * n1[0] + np.outer(np.ones(len(s)), np.sin(theta)) * n2[0])
    Y = p_start[1] + S * v_norm[1] + radius * (np.outer(np.ones(len(s)), np.cos(theta)) * n1[1] + np.outer(np.ones(len(s)), np.sin(theta)) * n2[1])
    Z = p_start[2] + S * v_norm[2] + radius * (np.outer(np.ones(len(s)), np.cos(theta)) * n1[2] + np.outer(np.ones(len(s)), np.sin(theta)) * n2[2])

    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, shade=True)

def render_scene(angles, payload_pos=None, title="", save_path=None, trajectory=None):
    """Renders high-quality 3D view of the robot arm."""
    fig = plt.figure(figsize=(9, 7), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=28, azim=48)

    pts = forward_kinematics(*angles)
    
    # Environment: Floor grid
    grid_size = 40
    gx, gy = np.meshgrid(np.linspace(-grid_size, grid_size, 9), np.linspace(-grid_size, grid_size, 9))
    ax.plot_wireframe(gx, gy, np.zeros_like(gx), color='#E2E8F0', linewidth=0.7)

    # Base pedestal
    ax.plot([-6, 6, 6, -6, -6], [-6, -6, 6, 6, -6], [0, 0, 0, 0, 0], color='#475569', linewidth=2)
    draw_cylinder(ax, pts[0], pts[1], radius=3.2, color='#334155', alpha=0.95)

    # Links
    draw_cylinder(ax, pts[1], pts[2], radius=2.2, color='#2563EB', alpha=0.9)
    draw_cylinder(ax, pts[2], pts[3], radius=1.8, color='#0284C7', alpha=0.9)
    draw_cylinder(ax, pts[3], pts[4], radius=1.3, color='#0D9488', alpha=0.9)

    # Joint spheres
    joint_colors = ['#1E293B', '#F59E0B', '#F59E0B', '#10B981']
    for p, c in zip(pts[1:], joint_colors):
        ax.scatter([p[0]], [p[1]], [p[2]], color=c, s=140, edgecolor='black', linewidth=1, zorder=10)

    # Gripper fingers at TCP (pts[4])
    tcp = pts[4]
    gripper_span = 3.5
    ax.scatter([tcp[0]], [tcp[1]], [tcp[2]], color='#EF4444', s=90, marker='o')

    # Draw Source Container / Pick Station (Green)
    pick_x, pick_y, pick_z = 24.0, 16.0, 2.0
    ax.scatter([pick_x], [pick_y], [0], color='#16A34A', s=350, marker='s', alpha=0.7, label='Source Pick Zone')
    
    # Draw Destination Bin / Place Station (Purple)
    place_x, place_y, place_z = -18.0, 25.0, 2.0
    ax.scatter([place_x], [place_y], [0], color='#9333EA', s=350, marker='^', alpha=0.7, label='Destination Place Zone')

    # Payload Box if picked or present
    if payload_pos is not None:
        ax.scatter([payload_pos[0]], [payload_pos[1]], [payload_pos[2]], color='#F97316', s=260, marker='D', edgecolor='black', label='Target Payload (Cube)')
    
    # Trajectory trace line
    if trajectory is not None and len(trajectory) > 0:
        traj_pts = np.array(trajectory)
        ax.plot(traj_pts[:, 0], traj_pts[:, 1], traj_pts[:, 2], color='#DC2626', linestyle='--', linewidth=2.2, label='TCP Motion Path')

    ax.set_xlim([-45, 45])
    ax.set_ylim([-45, 45])
    ax.set_zlim([0, 55])
    ax.set_xlabel('X (cm)', fontweight='bold', labelpad=8)
    ax.set_ylabel('Y (cm)', fontweight='bold', labelpad=8)
    ax.set_zlabel('Z (cm)', fontweight='bold', labelpad=8)
    
    # Degrees of freedom readout annotation
    dof_text = (
        f"Joint 1 (Base Yaw): {angles[0]:.1f}°\n"
        f"Joint 2 (Shoulder): {angles[1]:.1f}°\n"
        f"Joint 3 (Elbow): {angles[2]:.1f}°\n"
        f"Joint 4 (Wrist): {angles[3]:.1f}°\n"
        f"TCP: ({tcp[0]:.1f}, {tcp[1]:.1f}, {tcp[2]:.1f}) cm"
    )
    fig.text(0.12, 0.82, dof_text, fontsize=8.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.95))

    ax.set_title(title, fontsize=12, fontweight='bold', pad=14, color='#0F172A')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def run_simulation_pipeline(output_dir):
    """Executes pick and place sequence, captures screenshots, and creates animated GIF."""
    os.makedirs(output_dir, exist_ok=True)
    screenshots_dir = os.path.join(output_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Key Waypoints for Pick-and-Place:
    # 1. Home
    # 2. Hover above Pick Zone (24, 16, 18)
    # 3. Grip Pick Object (24, 16, 4)
    # 4. Lift with Object (24, 16, 26)
    # 5. Swing to Place Hover (-18, 25, 26)
    # 6. Lower to Place Zone (-18, 25, 4)
    # 7. Release & Retreat (-18, 25, 20)
    # 8. Return Home

    waypoints = [
        {"name": "Home Position", "angles": (0.0, 45.0, -45.0, 0.0), "has_box": False, "box_pos": (24, 16, 4)},
        {"name": "Hover Above Pick Zone", "pos": (24.0, 16.0, 20.0), "wrist": -70.0, "has_box": False, "box_pos": (24, 16, 4)},
        {"name": "Descend & Grasp Object (Pick)", "pos": (24.0, 16.0, 4.0), "wrist": -80.0, "has_box": True, "box_pos": (24, 16, 4)},
        {"name": "Lift Payload to Safe Clearance", "pos": (24.0, 16.0, 26.0), "wrist": -60.0, "has_box": True, "box_pos": None},
        {"name": "Transit / Swing Transfer to Target", "pos": (-18.0, 25.0, 26.0), "wrist": -60.0, "has_box": True, "box_pos": None},
        {"name": "Descend & Position into Destination (Place)", "pos": (-18.0, 25.0, 4.0), "wrist": -80.0, "has_box": True, "box_pos": None},
        {"name": "Release Object & Retract Upward", "pos": (-18.0, 25.0, 20.0), "wrist": -70.0, "has_box": False, "box_pos": (-18, 25, 4)},
        {"name": "Return to Idle / Ready State", "angles": (0.0, 45.0, -45.0, 0.0), "has_box": False, "box_pos": (-18, 25, 4)},
    ]

    # Convert positions to angles via IK where needed
    solved_waypoints = []
    for wp in waypoints:
        if "angles" in wp:
            q = wp["angles"]
        else:
            q = inverse_kinematics(*wp["pos"], wrist_angle_deg=wp["wrist"])
        solved_waypoints.append({
            "name": wp["name"],
            "angles": q,
            "has_box": wp["has_box"],
            "box_pos": wp["box_pos"]
        })

    # High-res stage snapshots to save for report
    stage_snapshots = [
        (0, "01_home_state.png", "Stage 1: Robot Arm at Home Reference Configuration"),
        (2, "02_approach_and_pick.png", "Stage 2: End-Effector Grasping Payload at Source (Pick)"),
        (4, "03_lift_and_transfer.png", "Stage 3: Trajectory Transfer with Payload in Workspace"),
        (5, "04_place_and_release.png", "Stage 4: Precision Placement at Target Bin (Place)")
    ]

    trajectory_history = []
    anim_frames = []

    # Interpolate trajectory smoothly
    current_q = np.array(solved_waypoints[0]["angles"])
    pts_start = forward_kinematics(*current_q)
    trajectory_history.append(pts_start[-1])

    frame_idx = 0
    total_stages = len(solved_waypoints) - 1

    for step_i in range(total_stages):
        q_start = np.array(solved_waypoints[step_i]["angles"])
        q_end = np.array(solved_waypoints[step_i + 1]["angles"])
        has_box = solved_waypoints[step_i + 1]["has_box"]
        static_box_pos = solved_waypoints[step_i + 1]["box_pos"]

        # 6 interpolation steps per segment
        num_substeps = 6
        for t in np.linspace(0, 1, num_substeps):
            # Smooth S-curve (cosine blending)
            blend = 0.5 * (1.0 - np.cos(np.pi * t))
            q_interp = q_start + blend * (q_end - q_start)
            pts = forward_kinematics(*q_interp)
            tcp = pts[-1]
            trajectory_history.append(tcp)

            box_pos = (tcp[0], tcp[1], tcp[2] - 2.5) if has_box else static_box_pos

            # Save frame for GIF
            frame_filename = os.path.join(screenshots_dir, f"temp_frame_{frame_idx:03d}.png")
            render_scene(
                q_interp,
                payload_pos=box_pos,
                title=f"Pick-and-Place Motion Simulation: {solved_waypoints[step_i+1]['name']}",
                save_path=frame_filename,
                trajectory=trajectory_history
            )
            anim_frames.append(frame_filename)
            frame_idx += 1

    # Save the 4 official report screenshots
    for wp_idx, out_name, title in stage_snapshots:
        wp = solved_waypoints[wp_idx]
        pts = forward_kinematics(*wp["angles"])
        tcp = pts[-1]
        box_pos = (tcp[0], tcp[1], tcp[2] - 2.5) if wp["has_box"] else wp["box_pos"]
        save_file = os.path.join(screenshots_dir, out_name)
        render_scene(
            wp["angles"],
            payload_pos=box_pos,
            title=title,
            save_path=save_file,
            trajectory=trajectory_history
        )
        print(f"Saved snapshot: {save_file}")

    # Generate Kinematics & Trajectory Combined Plot (05_full_trajectory_and_kinematics.png)
    generate_kinematics_plots(trajectory_history, os.path.join(screenshots_dir, "05_full_trajectory_and_kinematics.png"))

    # Build Animated GIF
    gif_path = os.path.join(output_dir, "pick_and_place_simulation.gif")
    images = [Image.open(fn) for fn in anim_frames]
    if images:
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=120,
            loop=0
        )
        print(f"Saved animated GIF: {gif_path}")

    # Cleanup temporary frame files
    for fn in anim_frames:
        try:
            os.remove(fn)
        except:
            pass

def generate_kinematics_plots(trajectory, save_path):
    """Plots TCP 3D path and Cartesian coordinates over time."""
    traj = np.array(trajectory)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), dpi=150)
    fig.suptitle("Robotic Arm Motion Profile & Kinematic Trajectory Verification", fontsize=14, fontweight='bold', color='#1E3A8A')

    time_steps = np.arange(len(traj))

    # X position
    axes[0, 0].plot(time_steps, traj[:, 0], color='#2563EB', linewidth=2)
    axes[0, 0].set_title("TCP X-Coordinate (cm)", fontweight='bold')
    axes[0, 0].set_ylabel("Position (cm)")
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)

    # Y position
    axes[0, 1].plot(time_steps, traj[:, 1], color='#0D9488', linewidth=2)
    axes[0, 1].set_title("TCP Y-Coordinate (cm)", fontweight='bold')
    axes[0, 1].set_ylabel("Position (cm)")
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)

    # Z position (Elevation)
    axes[1, 0].plot(time_steps, traj[:, 2], color='#EA580C', linewidth=2)
    axes[1, 0].axhline(y=4.0, color='red', linestyle=':', label='Pick/Place Contact Level (Z=4 cm)')
    axes[1, 0].set_title("TCP Z-Coordinate Elevation (cm)", fontweight='bold')
    axes[1, 0].set_xlabel("Simulation Step")
    axes[1, 0].set_ylabel("Position (cm)")
    axes[1, 0].legend()
    axes[1, 0].grid(True, linestyle='--', alpha=0.6)

    # 2D Overhead Top-Down XY Motion Path
    axes[1, 1].plot(traj[:, 0], traj[:, 1], color='#7C3AED', linewidth=2.5, marker='.', markersize=4)
    axes[1, 1].scatter([24.0], [16.0], color='#16A34A', s=120, label='Pick Station (24, 16)', zorder=5)
    axes[1, 1].scatter([-18.0], [25.0], color='#9333EA', s=120, label='Place Station (-18, 25)', zorder=5)
    axes[1, 1].scatter([0], [0], color='#1E293B', s=90, marker='x', label='Arm Base Origin', zorder=5)
    axes[1, 1].set_title("Overhead Horizontal (X-Y) Workspace Path", fontweight='bold')
    axes[1, 1].set_xlabel("X (cm)")
    axes[1, 1].set_ylabel("Y (cm)")
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"Saved kinematics trajectory chart: {save_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    run_simulation_pipeline(base_dir)
