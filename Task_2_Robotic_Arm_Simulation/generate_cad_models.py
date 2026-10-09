import os
import numpy as np
import trimesh

# Global kinematic dimensions (Unit: centimeters [cm])
L1 = 15.0  # Base to shoulder joint pivot
L2 = 25.0  # Upper arm length (shoulder to elbow)
L3 = 20.0  # Forearm length (elbow to wrist)
L4 = 10.0  # Wrist to Tool Center Point (TCP)

def create_base_pedestal():
    """Generates solid stepped cylindrical base pedestal with mounting flange."""
    flange = trimesh.creation.cylinder(radius=9.0, height=2.0, sections=48)
    flange.apply_translation([0, 0, 1.0])

    hub = trimesh.creation.cylinder(radius=6.0, height=3.0, sections=48)
    hub.apply_translation([0, 0, 3.5])

    base = trimesh.util.concatenate([flange, hub])
    return base

def create_shoulder_turret():
    """Generates shoulder rotating turret with clevis fork and joint axis bore."""
    turret_body = trimesh.creation.cylinder(radius=4.5, height=10.0, sections=48)
    turret_body.apply_translation([0, 0, 5.0])

    # Clevis fork ears (two vertical plates holding the shoulder pivot at Z=15.0 cm)
    ear_l = trimesh.creation.box(extents=[3.0, 1.6, 6.0])
    ear_l.apply_translation([0, -2.6, 12.0])

    ear_r = trimesh.creation.box(extents=[3.0, 1.6, 6.0])
    ear_r.apply_translation([0, +2.6, 12.0])

    # Shoulder pivot pin cylinder at Z=15.0 cm
    pin = trimesh.creation.cylinder(radius=1.8, height=7.2, sections=32)
    # Rotate cylinder to align along Y-axis
    rot_x = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    pin.apply_transform(rot_x)
    pin.apply_translation([0, 0, 15.0])

    turret = trimesh.util.concatenate([turret_body, ear_l, ear_r, pin])
    return turret

def create_upper_arm():
    """Generates tapered upper arm link with clevis boss at both ends (L2 = 25.0 cm)."""
    # Main beam extending along Z from 0 to L2
    beam = trimesh.creation.box(extents=[3.6, 3.2, L2])
    beam.apply_translation([0, 0, L2 / 2.0])

    # Shoulder joint boss at Z=0
    boss_shoulder = trimesh.creation.cylinder(radius=2.5, height=3.4, sections=32)
    rot_x = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    boss_shoulder.apply_transform(rot_x)

    # Elbow joint boss at Z=L2
    boss_elbow = trimesh.creation.cylinder(radius=2.2, height=3.4, sections=32)
    boss_elbow.apply_transform(rot_x)
    boss_elbow.apply_translation([0, 0, L2])

    arm = trimesh.util.concatenate([beam, boss_shoulder, boss_elbow])
    return arm

def create_forearm():
    """Generates forearm link with elbow and wrist boss (L3 = 20.0 cm)."""
    beam = trimesh.creation.box(extents=[2.8, 2.6, L3])
    beam.apply_translation([0, 0, L3 / 2.0])

    # Elbow mating boss at Z=0
    boss_elbow = trimesh.creation.cylinder(radius=2.0, height=2.8, sections=32)
    rot_x = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    boss_elbow.apply_transform(rot_x)

    # Wrist boss at Z=L3
    boss_wrist = trimesh.creation.cylinder(radius=1.8, height=2.8, sections=32)
    boss_wrist.apply_transform(rot_x)
    boss_wrist.apply_translation([0, 0, L3])

    forearm = trimesh.util.concatenate([beam, boss_elbow, boss_wrist])
    return forearm

def create_gripper():
    """Generates two-finger parallel gripper end-effector (L4 = 10.0 cm)."""
    # Wrist mounting coupling & pneumatic actuator housing (0 to 6 cm)
    wrist_flange = trimesh.creation.cylinder(radius=1.8, height=2.0, sections=32)
    wrist_flange.apply_translation([0, 0, 1.0])

    body = trimesh.creation.box(extents=[4.8, 2.8, 4.0])
    body.apply_translation([0, 0, 4.0])

    # Palm bracket (4 to 6 cm)
    palm = trimesh.creation.box(extents=[5.4, 2.4, 1.0])
    palm.apply_translation([0, 0, 6.5])

    # Two parallel finger jaws (6 to 10 cm, spaced 3.6 cm apart)
    finger_l = trimesh.creation.box(extents=[0.8, 1.8, 3.5])
    finger_l.apply_translation([-1.8, 0, 8.25])

    finger_r = trimesh.creation.box(extents=[0.8, 1.8, 3.5])
    finger_r.apply_translation([+1.8, 0, 8.25])

    gripper = trimesh.util.concatenate([wrist_flange, body, palm, finger_l, finger_r])
    return gripper

def export_all_cad(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print("Generating precision 3D CAD models using solid CSG...")

    # Build individual component meshes
    p1 = create_base_pedestal()
    p2 = create_shoulder_turret()
    p3 = create_upper_arm()
    p4 = create_forearm()
    p5 = create_gripper()

    # Export individual binary STL files
    parts = [
        ("01_base_pedestal.stl", p1),
        ("02_shoulder_turret_link.stl", p2),
        ("03_upper_arm_link.stl", p3),
        ("04_forearm_link.stl", p4),
        ("05_end_effector_gripper.stl", p5)
    ]

    for fname, mesh in parts:
        fpath = os.path.join(output_dir, fname)
        mesh.export(fpath, file_type='stl')
        print(f"Exported {fname}: {len(mesh.faces)} faces, {len(mesh.vertices)} vertices")

    # Assembly at Home Pose: theta1=0 deg, theta2=45 deg, theta3=-45 deg, theta4=0 deg
    # In Home Pose:
    # Part 1 (Base): at origin
    # Part 2 (Turret): at origin, rotated theta1
    # Part 3 (Upper Arm): shoulder pivot at [0, 0, L1], rotated theta2 around Y
    # Part 4 (Forearm): elbow at [0, 0, L1] + R(theta2)*[0, 0, L2], rotated theta2+theta3
    # Part 5 (Gripper): wrist at p_elbow + R(theta2+theta3)*[0, 0, L3], rotated theta2+theta3+theta4

    t1_rad = np.radians(0.0)
    t2_rad = np.radians(45.0)
    t3_rad = np.radians(-45.0)
    t4_rad = np.radians(0.0)

    # Base mesh (part 1)
    m1 = p1.copy()

    # Turret mesh (part 2)
    m2 = p2.copy()
    R1 = trimesh.transformations.rotation_matrix(t1_rad, [0, 0, 1])
    m2.apply_transform(R1)

    # Upper arm (part 3)
    m3 = p3.copy()
    # Rotation around Y by theta2:
    R2 = trimesh.transformations.rotation_matrix(t2_rad, [0, 1, 0])
    # Combine with base yaw R1
    T3 = trimesh.transformations.translation_matrix([0, 0, L1]) @ R1 @ R2
    m3.apply_transform(T3)

    # Forearm (part 4)
    m4 = p4.copy()
    R23 = trimesh.transformations.rotation_matrix(t2_rad + t3_rad, [0, 1, 0])
    elbow_local = np.array([0, 0, L2, 1.0])
    elbow_world = (T3 @ elbow_local)[:3]
    T4 = trimesh.transformations.translation_matrix(elbow_world) @ R1 @ R23
    m4.apply_transform(T4)

    # Gripper (part 5)
    m5 = p5.copy()
    R234 = trimesh.transformations.rotation_matrix(t2_rad + t3_rad + t4_rad, [0, 1, 0])
    wrist_local = np.array([0, 0, L3, 1.0])
    wrist_world = (T4 @ wrist_local)[:3]
    T5 = trimesh.transformations.translation_matrix(wrist_world) @ R1 @ R234
    m5.apply_transform(T5)

    # Combine into full 5-part assembly
    assembly = trimesh.util.concatenate([m1, m2, m3, m4, m5])
    asm_stl = os.path.join(output_dir, "robotic_arm_assembly.stl")
    assembly.export(asm_stl, file_type='stl')
    print(f"Exported full assembly STL ({len(assembly.faces)} faces): {asm_stl}")

    # Export multi-part Wavefront OBJ with distinct groups
    obj_path = os.path.join(output_dir, "robotic_arm_assembly.obj")
    with open(obj_path, 'w') as f:
        f.write("# 4-DOF Articulated Robotic Arm Complete 5-Part Assembly\n")
        f.write("# CodeAlpha Robotics & Automation Internship — Task 2\n")
        f.write("# Unit convention: Centimeters [cm] (1 unit = 1 cm = 10 mm)\n\n")

        v_offset = 1
        part_meshes = [
            ("Base_Pedestal", m1),
            ("Shoulder_Turret", m2),
            ("Upper_Arm_Link", m3),
            ("Forearm_Link", m4),
            ("End_Effector_Gripper", m5)
        ]
        for name, p_mesh in part_meshes:
            f.write(f"g {name}\n")
            for v in p_mesh.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for face in p_mesh.faces:
                f.write(f"f {face[0]+v_offset} {face[1]+v_offset} {face[2]+v_offset}\n")
            v_offset += len(p_mesh.vertices)
            f.write("\n")
    print(f"Exported full assembly OBJ (5 distinct parts): {obj_path}")

if __name__ == '__main__':
    cad_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cad_models")
    export_all_cad(cad_dir)
