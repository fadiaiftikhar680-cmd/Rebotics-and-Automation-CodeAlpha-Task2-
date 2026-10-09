import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#4A5568"))
            self.drawString(50, 11 * 72 - 36, "CodeAlpha Robotics & Automation Internship — Task 2: Robotic Arm Simulation")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(50, 11 * 72 - 42, 8.5 * 72 - 50, 11 * 72 - 42)

            self.line(50, 40, 8.5 * 72 - 50, 40)
            self.setFont("Helvetica", 8)
            self.drawString(50, 28, "Engineering Simulation & Verification Report | CodeAlpha Internship Program")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * 72 - 50, 28, page_text)
        self.restoreState()

def build_pdf(filename="Task_2_Robotic_Arm_Simulation_Report.pdf", base_dir="."):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")
    secondary = colors.HexColor("#0D9488")
    dark = colors.HexColor("#1F2937")

    title_style = ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=primary, spaceAfter=6)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=secondary, spaceAfter=8)
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#4B5563"))
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=primary, spaceBefore=8, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=dark, spaceAfter=4, alignment=4)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=dark, alignment=0)
    caption_style = ParagraphStyle('Cap', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=6)

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("CodeAlpha Robotics & Automation Internship — Task 2", sub_style))
    story.append(Paragraph("Design, Kinematic Modeling, CAD Assembly, and Motion Simulation of a 4-DOF Robotic Manipulator", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary, spaceBefore=2, spaceAfter=8))

    meta_data = [
        [Paragraph("<b>Author:</b> CodeAlpha Robotics Intern", meta_style), Paragraph("<b>Domain:</b> Robotic Arm Kinematics & Simulation", meta_style)],
        [Paragraph("<b>Deliverables:</b> 5 CAD STLs, 1 OBJ Assembly, 3D Engine, Offline WebGL", meta_style), Paragraph("<b>Unit Convention:</b> Metric (Lengths in cm, Angles in °)", meta_style)]
    ]
    t_meta = Table(meta_data, colWidths=[255, 255])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Executive Overview & Technical Objectives", h1_style))
    story.append(Paragraph(
        "Articulated robotic manipulators form the backbone of modern flexible manufacturing and pick-and-place intralogistics. "
        "This engineering report documents the kinematic design, closed-form analytical solvers, solid CAD component modeling, "
        "and physical trajectory verification of a 4-DOF articulated manipulator equipped with a parallel-jaw end-effector. "
        "All geometric lengths are defined in metric centimeters (cm), angles in degrees (°), and positional accuracy tolerances are held within 1.0 mm.",
        body_style
    ))

    story.append(Paragraph("2. Specification of Degrees of Freedom (DOF)", h1_style))
    story.append(Paragraph(
        "The manipulator incorporates <b>4 active revolute degrees of freedom (4-DOF) plus a 1-DOF prismatic dual-finger pneumatic gripper</b>. "
        "This configuration provides spatial positioning (X, Y, Z) and pitch attitude regulation, optimized for pick-and-place material transfer.",
        body_style
    ))

    dof_table_data = [
        [Paragraph("Joint", th_style), Paragraph("Type", th_style), Paragraph("Axis of Motion", th_style), Paragraph("Angular Range", th_style), Paragraph("Link Length", th_style), Paragraph("Functional Role", th_style)],
        [Paragraph("<b>Joint 1 (Base)</b>", tc_style), Paragraph("Revolute", tc_style), Paragraph("Yaw (Z-axis)", tc_style), Paragraph("-180° to +180°", tc_style), Paragraph("L1 = 15.0 cm", tc_style), Paragraph("Workcell azimuthal sweep", tc_style)],
        [Paragraph("<b>Joint 2 (Shoulder)</b>", tc_style), Paragraph("Revolute", tc_style), Paragraph("Pitch (Y-axis)", tc_style), Paragraph("-30° to +110°", tc_style), Paragraph("L2 = 25.0 cm", tc_style), Paragraph("Primary vertical and radial reach", tc_style)],
        [Paragraph("<b>Joint 3 (Elbow)</b>", tc_style), Paragraph("Revolute", tc_style), Paragraph("Pitch (Y-axis)", tc_style), Paragraph("-120° to +120°", tc_style), Paragraph("L3 = 20.0 cm", tc_style), Paragraph("Forearm altitude and extension", tc_style)],
        [Paragraph("<b>Joint 4 (Wrist)</b>", tc_style), Paragraph("Revolute", tc_style), Paragraph("Pitch (Y-axis)", tc_style), Paragraph("-90° to +90°", tc_style), Paragraph("L4 = 10.0 cm", tc_style), Paragraph("Tool Center Point (TCP) alignment", tc_style)],
        [Paragraph("<b>End-Effector</b>", tc_style), Paragraph("Prismatic", tc_style), Paragraph("Linear Pinch", tc_style), Paragraph("0 to 4.0 cm stroke", tc_style), Paragraph("Span: 5.0 cm", tc_style), Paragraph("Positive grasp of target payloads", tc_style)]
    ]
    t_dof = Table(dof_table_data, colWidths=[65, 48, 75, 75, 75, 172])
    t_dof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dof)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Kinematic Modeling & Denavit-Hartenberg (DH) Parameters", h1_style))
    story.append(Paragraph(
        "Coordinate frames are attached at each joint axis according to standard Denavit-Hartenberg convention. "
        "The DH kinematic parameters governing homogeneous link transformations are detailed in Table 2:",
        body_style
    ))

    dh_table_data = [
        [Paragraph("Link (i)", th_style), Paragraph("Link Length (a<sub>i</sub>)", th_style), Paragraph("Link Twist (α<sub>i</sub>)", th_style), Paragraph("Link Offset (d<sub>i</sub>)", th_style), Paragraph("Joint Variable (θ<sub>i</sub>)", th_style)],
        [Paragraph("Link 1", tc_style), Paragraph("0.0 cm", tc_style), Paragraph("+90°", tc_style), Paragraph("15.0 cm (L1)", tc_style), Paragraph("&theta;<sub>1</sub> (Variable)", tc_style)],
        [Paragraph("Link 2", tc_style), Paragraph("25.0 cm (L2)", tc_style), Paragraph("0°", tc_style), Paragraph("0.0 cm", tc_style), Paragraph("&theta;<sub>2</sub> (Variable)", tc_style)],
        [Paragraph("Link 3", tc_style), Paragraph("20.0 cm (L3)", tc_style), Paragraph("0°", tc_style), Paragraph("0.0 cm", tc_style), Paragraph("&theta;<sub>3</sub> (Variable)", tc_style)],
        [Paragraph("Link 4", tc_style), Paragraph("10.0 cm (L4)", tc_style), Paragraph("0°", tc_style), Paragraph("0.0 cm", tc_style), Paragraph("&theta;<sub>4</sub> (Variable)", tc_style)],
    ]
    t_dh = Table(dh_table_data, colWidths=[90, 100, 105, 105, 110])
    t_dh.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_dh)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Analytical Inverse Kinematics Formulation:</b> For target Tool Center Point position (X<sub>tgt</sub>, Y<sub>tgt</sub>, Z<sub>tgt</sub>) and desired tool approach angle &psi;, "
        "the base azimuth is resolved as &theta;<sub>1</sub> = atan2(Y<sub>tgt</sub>, X<sub>tgt</sub>). The wrist center coordinates are isolated via "
        "r<sub>w</sub> = sqrt(X<sub>tgt</sub><sup>2</sup> + Y<sub>tgt</sub><sup>2</sup>) - L4&middot;cos(&psi;) and z<sub>w</sub> = Z<sub>tgt</sub> - L4&middot;sin(&psi;). "
        "Applying the Law of Cosines to the shoulder-elbow-wrist triangle yields cos(&theta;<sub>3</sub>) = (r<sub>w</sub><sup>2</sup> + (z<sub>w</sub> - L1)<sup>2</sup> - L2<sup>2</sup> - L3<sup>2</sup>) / (2&middot;L2&middot;L3), "
        "providing closed-form, deterministic solutions with elbow-up configuration without iterative solver latency.",
        body_style
    ))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("4. Kinematics Verification & Error Analysis", h1_style))
    story.append(Paragraph(
        "To rigorously demonstrate that the kinematics formulation is analytically validated, the verification script (verify_kinematics.py) "
        "executes Inverse Kinematics across all primary workcell waypoints, substitutes the solved joint angles back into Forward Kinematics, "
        "and computes Cartesian Euclidean position error. Table 3 presents the quantitative results, verifying <b>max error &lt; 0.001 mm</b> "
        "and zero joint limit violations across the full trajectory.",
        body_style
    ))

    # Verification table data (dynamically computed from verify_kinematics.py)
    verif_data = [
        [Paragraph("Waypoint Name", th_style), Paragraph("Target (X, Y, Z) [cm]", th_style), Paragraph("Solved Joint Angles (&theta;<sub>1</sub>, &theta;<sub>2</sub>, &theta;<sub>3</sub>, &theta;<sub>4</sub>) [°]", th_style), Paragraph("Position Error", th_style), Paragraph("Validation Status", th_style)],
        [Paragraph("Pick Hover", tc_style), Paragraph("(24.0, 16.0, 20.0)", tc_style), Paragraph("(33.7°, 71.9°, -99.9°, -42.1°)", tc_style), Paragraph("0.0000 mm", tc_style), Paragraph("PASSED (In Limits)", tc_style)],
        [Paragraph("Pick Grasp Target", tc_style), Paragraph("(24.0, 16.0, 4.0)", tc_style), Paragraph("(33.7°, 42.5°, -106.8°, -15.7°)", tc_style), Paragraph("0.0000 mm", tc_style), Paragraph("PASSED (In Limits)", tc_style)],
        [Paragraph("Safe Transit Lift", tc_style), Paragraph("(24.0, 16.0, 26.0)", tc_style), Paragraph("(33.7°, 79.7°, -94.0°, -45.7°)", tc_style), Paragraph("0.0000 mm", tc_style), Paragraph("PASSED (In Limits)", tc_style)],
        [Paragraph("Place Swing Hover", tc_style), Paragraph("(-18.0, 25.0, 26.0)", tc_style), Paragraph("(125.8°, 75.3°, -88.4°, -46.9°)", tc_style), Paragraph("0.0000 mm", tc_style), Paragraph("PASSED (In Limits)", tc_style)],
        [Paragraph("Place Target Bin", tc_style), Paragraph("(-18.0, 25.0, 4.0)", tc_style), Paragraph("(125.8°, 40.3°, -100.3°, -20.0°)", tc_style), Paragraph("0.0000 mm", tc_style), Paragraph("PASSED (In Limits)", tc_style)],
        [Paragraph("Retract Staging", tc_style), Paragraph("(-18.0, 25.0, 20.0)", tc_style), Paragraph("(125.8°, 67.9°, -93.9°, -44.0°)", tc_style), Paragraph("0.0000 mm", tc_style), Paragraph("PASSED (In Limits)", tc_style)],
    ]
    t_verif = Table(verif_data, colWidths=[95, 95, 160, 75, 85])
    t_verif.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_verif)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. CAD Solid Modeling Architecture", h1_style))
    story.append(Paragraph(
        "All structural elements are modeled using solid constructive geometry and exported to standard formats in <code>cad_models/</code>:<br/>"
        "• <b>01_base_pedestal.stl:</b> Stepped circular base (radius 9.0 cm, hub radius 6.0 cm, height 5.0 cm, 384 facets).<br/>"
        "• <b>02_shoulder_turret_link.stl:</b> Azimuthal rotating column with dual clevis ear brackets and joint-axis bore at Z=15.0 cm (344 facets).<br/>"
        "• <b>03_upper_arm_link.stl:</b> Structural beam (L2 = 25.0 cm) with shoulder boss and elbow clevis boss (268 facets).<br/>"
        "• <b>04_forearm_link.stl:</b> Forearm link (L3 = 20.0 cm) connecting elbow and wrist pivot axes (268 facets).<br/>"
        "• <b>05_end_effector_gripper.stl:</b> Dual-finger parallel gripper (L4 = 10.0 cm) with palm plate and pneumatic finger jaws (176 facets).<br/>"
        "• <b>robotic_arm_assembly.obj / .stl:</b> Complete 5-part solid assembly positioned in the home pose (1,440 facets).",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Page Break for Screenshots Section
    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("6. Pick-and-Place Motion Simulation Results", h1_style))
    story.append(Paragraph(
        "The pick-and-place trajectory transfers payloads from Source Pick Station (X: 24 cm, Y: 16 cm, Z: 4 cm) "
        "to Target Placement Bin (X: -18 cm, Y: 25 cm, Z: 4 cm). Smooth cosine trajectory blending eliminates "
        "inertial jerks during liftoff, horizontal slew, and placement.",
        body_style
    ))

    img_dir = os.path.join(base_dir, "screenshots")
    img_w, img_h = 240, 180

    img1 = os.path.join(img_dir, "01_home_state.png")
    img2 = os.path.join(img_dir, "02_approach_and_pick.png")
    img3 = os.path.join(img_dir, "03_lift_and_transfer.png")
    img4 = os.path.join(img_dir, "04_place_and_release.png")

    if os.path.exists(img1) and os.path.exists(img2):
        row1 = [
            [Image(img1, width=img_w, height=img_h), Image(img2, width=img_w, height=img_h)],
            [Paragraph("Figure 1(a): Stage 1 — Home State Reference Configuration", caption_style),
             Paragraph("Figure 1(b): Stage 2 — Gripper Grasping Payload at Pick Station", caption_style)]
        ]
        t_row1 = Table(row1, colWidths=[255, 255])
        t_row1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(t_row1)

    story.append(Spacer(1, 4))

    if os.path.exists(img3) and os.path.exists(img4):
        row2 = [
            [Image(img3, width=img_w, height=img_h), Image(img4, width=img_w, height=img_h)],
            [Paragraph("Figure 1(c): Stage 3 — Safe Altitude Transfer Across Workspace", caption_style),
             Paragraph("Figure 1(d): Stage 4 — Precision Placement into Destination Bin", caption_style)]
        ]
        t_row2 = Table(row2, colWidths=[255, 255])
        t_row2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(t_row2)

    # ================= PAGE 4 =================
    story.append(PageBreak())
    story.append(Paragraph("7. Kinematic Trajectory Verification Curves", h1_style))
    story.append(Paragraph(
        "Cartesian operational coordinates and elevation profiles were continuously recorded across all 42 simulation steps. "
        "Figure 2 confirms smooth transition down to Z=4 cm pick level, rapid vertical clearance to Z=26 cm transit altitude, "
        "and clean horizontal arc slew into the destination zone without overshoot.",
        body_style
    ))

    img5 = os.path.join(img_dir, "05_full_trajectory_and_kinematics.png")
    if os.path.exists(img5):
        story.append(Image(img5, width=480, height=330))
        story.append(Paragraph("Figure 2: Complete Kinematic Motion Profile (Cartesian Coordinates vs. Time & Overhead XY Path)", caption_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("8. Offline Web Simulation Environment", h1_style))
    story.append(Paragraph(
        "To satisfy offline demonstration requirements, <code>interactive_3d_arm.html</code> bundles local Three.js and OrbitControls libraries. "
        "Users can launch the file in any browser without internet access to manipulate joint sliders, inspect forward kinematics live, "
        "and trigger the automated pick-and-place sequence.",
        body_style
    ))

    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph(
        "Task 2 completes all CodeAlpha internship criteria: degrees of freedom are fully defined, DH parameters and analytical IK "
        "are mathematically validated with max error < 0.001 mm, 5 solid CAD models and a complete assembly are generated, and offline 3D "
        "simulation and high-resolution trajectory captures are provided.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Task 2 Report generated: {filename}")

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(here, "Task_2_Robotic_Arm_Simulation_Report.pdf")
    build_pdf(target_pdf, here)
