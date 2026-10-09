import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
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
            self.drawString(54, 11 * 72 - 36, "CodeAlpha Robotics & Automation Internship — Task 1: Research Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

            self.line(54, 42, 8.5 * 72 - 54, 42)
            self.setFont("Helvetica", 8)
            self.drawString(54, 30, "Academic & Technical Submission | CodeAlpha Internship Program")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * 72 - 54, 30, page_text)
        self.restoreState()

def clean_text_for_word_count(text):
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'&[a-zA-Z]+;', ' ', clean)
    clean = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', clean)
    words = clean.split()
    return words

# Define the verified academic references
REFERENCES = [
    "[1] ISO 10218-1:2011 & ISO 10218-2:2011, Robots and robotic devices — Safety requirements for industrial robots — Part 1: Robots; Part 2: Robot systems and integration, International Organization for Standardization, Geneva.",
    "[2] ISO/TS 15066:2016, Robots and robotic devices — Collaborative robots, Technical Specification, International Organization for Standardization, Geneva.",
    "[3] Siciliano, B., & Khatib, O. (Eds.). (2016). Springer Handbook of Robotics (2nd ed.). Springer-Verlag Berlin Heidelberg. https://doi.org/10.1007/978-3-319-32552-1.",
    "[4] Craig, J. J. (2018). Introduction to Robotics: Mechanics and Control (4th ed.). Pearson Education.",
    "[5] Tao, F., Zhang, H., Liu, A., & Nee, A. Y. C. (2019). Digital Twin in Industry: State-of-the-Art. IEEE Transactions on Industrial Informatics, 15(4), 2405–2415. https://doi.org/10.1109/TII.2018.2873186.",
    "[6] Brogardh, T. (2007). Present and future robot control development—An industrial perspective. Annual Reviews in Control, 31(1), 69–79. https://doi.org/10.1016/j.arcontrol.2007.01.002.",
    "[7] Kagermann, H., Wahlster, W., & Helbig, J. (2013). Recommendations for implementing the strategic initiative INDUSTRIE 4.0: Final report of the Industrie 4.0 Working Group. National Academy of Science and Engineering (Acatech), Frankfurt am Main.",
    "[8] Monostori, L., Kadar, B., Bauernhansl, T., Kondoh, S., Kumara, S., Reinhart, G., Sauer, O., Schuh, G., Sihn, W., & Ueda, K. (2016). Cyber-physical systems in manufacturing. CIRP Annals, 65(2), 621–641. https://doi.org/10.1016/j.cirp.2016.06.005.",
    "[9] Villani, V., Pini, F., Leali, F., & Secchi, C. (2018). Survey on human–robot collaboration in industrial settings: Safety, intuitive interfaces and applications. Mechatronics, 55, 248–266. https://doi.org/10.1016/j.mechatronics.2018.02.009."
]

# Body content sections (strictly verifiable claims, linked citations [1]-[9])
SECTIONS = [
    {
        "title": "1. Introduction and the Evolution of Industrial Robotics",
        "paragraphs": [
            "Industrial robotics has undergone fundamental structural shifts over the past six decades, transforming from isolated, rigid automation mechanisms into cognitive, networked cyber-physical production entities [3, 6]. The deployment of the first Unimate arm on General Motors die-casting lines in 1961 inaugurated the first generation of robotics, characterized by open-loop or fixed-sequence execution designed strictly to isolate human workers from hazardous, repetitive thermal and mechanical operations [3]. In subsequent decades, the integration of solid-state sensors and rudimentary optical feedback enabled second-generation adaptive positioning, while the maturation of programmable logic controllers (PLCs), high-speed deterministic fieldbuses, and multi-axis coordinate kinematics established the high-speed automotive assembly paradigms of the late twentieth century [4, 6].",
            "Today, the international manufacturing sector operates within the paradigm of Industry 4.0, a cyber-physical transformation formalized by the German strategic initiative under Kagermann et al. [7] and synthesized comprehensively by Monostori et al. [8]. Rather than relying on monolithic, mass-production assembly lines requiring weeks of physical retooling between product variants, modern competitive manufacturing mandates high-mix, low-volume (HMLV) agility, rapid reconfiguration, and resilient supply integration. Within this context, industrial robots are no longer treated as isolated machine tools isolated behind perimeter fencing; they serve as intelligent edge-computing physical agents capable of autonomous trajectory adaptation, continuous cloud synchronization, and cooperative co-presence alongside human technicians [8, 9]."
        ]
    },
    {
        "title": "2. Core Architectural Pillars of Industry 4.0 Robotics",
        "paragraphs": [
            "The realization of intelligent manufacturing is driven by four interdependent architectural pillars: collaborative robotics, autonomous mobile navigation, cyber-physical digital twins, and industrial IoT communication infrastructure.",
            "<b>2.1 Collaborative Robots (Cobots) and Human-Robot Collaboration (HRC):</b> Traditional industrial manipulators operate with high kinetic energy and rigid gear trains, necessitating physical perimeter interlocks, light curtains, and safety mats mandated under ISO 10218-1 and ISO 10218-2 [1]. Collaborative robots, by contrast, incorporate power and force limiting (PFL), elastic series actuators, joint-level torque sensors, and rounded low-inertia chassis governed by the technical specifications of ISO/TS 15066 [2, 9]. As surveyed by Villani et al. [9], collaborative workcells leverage complementary human and machine capabilities: human operators contribute cognitive reasoning, tactile dexterity, and non-linear problem-solving, while cobots supply sub-millimeter repeatable positioning, ergonomic lift assistance, and uninterrupted cycle execution. ISO/TS 15066 establishes quantitative bio-mechanical thresholds for transient and quasi-static contact across designated anatomical body regions, requiring strict velocity limiting and dynamic protective zone monitoring whenever human operators enter collaborative envelopes [2].",
            "<b>2.2 Autonomous Mobile Robots (AMRs) in Flexible Intralogistics:</b> Material transport has migrated from conventional Automated Guided Vehicles (AGVs) requiring physical magnetic floor tapes or optical retro-reflectors toward autonomous mobile robots [3]. Utilizing 2D and 3D LiDAR sensors, visual odometry, and Simultaneous Localization and Mapping (SLAM) algorithms, AMRs maintain continuous internal representations of factory layouts. When temporary blockages, staging pallets, or maintenance personnel obstruct primary travel routes, AMRs dynamically compute alternate routes in real time without halting upstream production flows.",
            "<b>2.3 Digital Twins and Virtual Commissioning:</b> A digital twin represents an ultra-high-fidelity, bidirectional mathematical and physics-based software duplicate of physical robotic cells [5]. As synthesized by Tao et al. [5], digital twins merge multi-body kinematic solvers, finite-element stress models, and PLC control code within synchronized simulation platforms. Prior to physical installation, virtual commissioning validates reachability envelopes, cycle-time bottlenecks, singularity zones, and collision boundaries. During operational deployment, continuous telemetry streaming enables digital twin algorithms to identify harmonic drive gear wear, backlash escalation, and bearing vibration anomalies hundreds of operating hours prior to mechanical breakdown [5, 6]. Furthermore, digital twins allow control engineers to test firmware updates and path-optimization algorithms in silico before deploying changes to live factory floor cells, virtually eliminating downtime caused by untested software faults [5].",
            "<b>2.4 IIoT, Edge AI, and Deterministic Fieldbus Networks:</b> Modern robotic controllers function as edge computing nodes interconnected via open communication standards such as OPC Unified Architecture (IEC 62541) and Time-Sensitive Networking (TSN / IEEE 802.1Qbv) [8]. Low-latency edge computing enables deep learning inference directly adjacent to the robotic manipulator, executing visual defect classification, packaging barcode validation, and component orientation estimation within milliseconds without overburdening cloud bandwidth. As emphasized by Monostori et al. [8], the integration of deterministic industrial networks ensures that sensor feedback, motion interpolators, and supervisory safety systems exchange critical state vectors within bounded microsecond jitter tolerances."
        ]
    },
    {
        "title": "3. Comparative Technical Analysis: Traditional Manipulators versus Collaborative Robots",
        "paragraphs": [
            "To understand the operational trade-offs governing robotic cell design, Table 1 details a comparative engineering evaluation between traditional caged industrial articulated arms and contemporary collaborative manipulators based on international safety norms [1, 2, 9].",
            "Traditional industrial arms maximize payload density and structural rigidity, achieving Tool Center Point (TCP) velocities exceeding 2.0 m/s for heavy automotive body-in-white spot welding and foundry manipulation [3, 6]. However, their reliance on physical safety perimeters limits production line modularity. Conversely, cobots sacrifice maximum payload capacity and top speed to satisfy the stringent biomechanical force-limiting criteria of ISO/TS 15066, enabling floor-space reduction, rapid line reconfiguration, and intuitive hand-guiding lead-through programming [2, 9]."
        ]
    },
    {
        "title": "4. Sensing Modalities, Kinematic Control, and Machine Vision",
        "paragraphs": [
            "The responsiveness and autonomy of an Industry 4.0 robotic cell rely directly on closed-loop multi-sensor feedback architectures and rigorous kinematic formulations [3, 4]. Forward kinematics maps actuated joint displacements into Cartesian operational coordinates via homogeneous transformation matrices, while analytical and numerical inverse kinematics resolve required joint angles for target end-effector poses [4]. Differential kinematics utilizes the manipulator Jacobian matrix to relate joint angular velocities to operational linear and rotational velocities, providing the mathematical basis for singularity avoidance and Cartesian impedance control [3, 4]. Modern systems incorporate three primary sensory streams to govern these controllers:",
            "<b>4.1 3D Structured Light and Time-of-Flight Vision:</b> Conventional 2D machine vision frequently fails when subjected to fluctuating ambient factory lighting, shadows, or reflective metallic finishes. Industrial 3D sensors project modulated fringe patterns or compute laser photon phase shifts to synthesize high-density point clouds. This sensory capability facilitates random bin-picking, where robotic arms identify, isolate, and grasp randomly stacked, unoriented castings or plastic housings directly from transport bins.",
            "<b>4.2 Multi-Axis Force and Torque Compliance:</b> Mounted at the tool mounting flange, six-axis strain-gauge or piezoelectric transducers capture instantaneous forces and moments along Cartesian axes [3, 4]. Through hybrid position/force control architectures and active impedance control, robotic arms dynamically modulate joint torques. This compliance prevents tool breakage and workpiece gouging during surface polishing, aerospace composite trimming, and tight-clearance peg-in-hole mechanical assemblies.",
            "<b>4.3 Multi-Turn Absolute Encoders and Closed-Loop Servo Drives:</b> High-resolution optical or magnetic encoders mounted directly to output shafts resolve joint angles to fractions of an arc-second [4]. By retaining absolute angular position through power outages, modern manipulators eliminate mechanical zero-return homing routines, ensuring immediate line resumption following emergency stops."
        ]
    },
    {
        "title": "5. Industrial Applications and Sectoral Case Studies",
        "paragraphs": [
            "<b>Automotive Powertrain and Battery Cell Manufacturing:</b> In automotive fabrication, robotic systems execute structural adhesive dispensing, vision-guided component alignment, and precision fastener torquing [3, 6]. Within electric vehicle battery assembly, collaborative robots equipped with vacuum end-effectors handle fragile pouch cells, while closed-loop vision sensors verify electrode alignment and thermal interface material thickness with high repeatability.",
            "<b>Semiconductor Fabrication and Cleanroom Automation:</b> Semiconductor manufacturing imposes stringent particulate limits governed by ISO 14644 cleanroom classifications. Specialized vacuum-rated robotic manipulators equipped with Bernoulli non-contact end-effectors transport 300 mm silicon wafers between chemical vapor deposition, ion implantation, and lithography chambers, eliminating human contamination hazards and mechanical micro-fractures.",
            "<b>Intralogistics Sorting and E-Commerce Fulfillment:</b> Modern distribution hubs coordinate dense fleets of autonomous mobile robots and sorting manipulators governed by multi-agent coordination software [3, 8]. Mobile platforms navigate underneath storage racks to deliver items directly to ergonomic picking stations, where vision-guided robotic arms equipped with adaptive suction cups sort varied packaging geometries without requiring mechanical retooling."
        ]
    },
    {
        "title": "6. Safety Standards, Cyber-Physical Security, and Systemic Challenges",
        "paragraphs": [
            "Despite dramatic technical progress, industrial robotic deployments face notable engineering and governance hurdles:",
            "<b>Safety Compliance and Risk Assessment:</b> Deploying collaborative applications requires rigorous adherence to ISO 10218-1/2 and ISO/TS 15066 [1, 2]. System integrators must conduct systematic task-based risk assessments, measuring clamping and transient impact forces at every stage of the cycle. Whenever path analysis reveals potential pinch points against stationary equipment, physical guarding or speed-and-separation laser scanners must supplement power-and-force limiting mechanisms [2, 9].",
            "<b>Legacy Protocol Interoperability:</b> Industrial facilities routinely operate brownfield machinery built across multiple decades, utilizing disparate communication standards including Modbus, Profibus, CANopen, and CC-Link. Integrating these heterogenous assets into unified Industry 4.0 data pipelines requires robust edge gateway hardware and middleware abstraction layers [8].",
            "<b>Cyber-Physical Security in Connected Workcells:</b> As robotic controllers connect to enterprise Ethernet backbones and cloud fleet management portals, they become susceptible to network penetration, unauthorized trajectory overrides, and telemetry interception. Hardened system design demands hardware security modules (HSMs), cryptographically signed firmware verification, and strict operational segmentation between IT and OT network domains."
        ]
    },
    {
        "title": "7. Future Research Horizons and Emerging Frontiers",
        "paragraphs": [
            "The future trajectory of industrial robotics points toward Robotics 5.0, characterized by human-centric design, environmental sustainability, and cognitive adaptability [8, 9]. Key emerging research avenues include:",
            "<b>Embodied Artificial Intelligence and Multimodal Foundation Models:</b> Contemporary research explores Vision-Language-Action (VLA) foundation models capable of interpreting high-level operator prompts and translating them into dynamically feasible kinematic trajectories, drastically lowering programming complexity for small and medium-sized enterprises.",
            "<b>Neuromorphic Event-Based Sensing:</b> Event cameras measuring microsecond-level pixel luminance changes are replacing conventional frame-based cameras in ultra-high-speed tracking tasks. By eliminating motion blur and operating with minimal data throughput, neuromorphic sensors offer significant advantages for rapid visual servoing.",
            "<b>Sustainable Lifecycle Engineering:</b> With increasing attention to industrial decarbonization, robot manufacturers are engineering regenerative braking servo drives, lightweight carbon-composite arm links, and trajectory optimization algorithms designed to minimize kinetic energy consumption across 24/7 operating cycles [6]."
        ]
    },
    {
        "title": "8. Conclusion",
        "paragraphs": [
            "Industrial robotics within the Industry 4.0 ecosystem has transitioned from isolated, deterministic machinery into adaptable, networked partners in intelligent manufacturing [7, 8]. The convergence of collaborative force-limited actuation, autonomous mobile transport, digital twin virtual commissioning, and robust industrial communication enables enterprises to achieve unprecedented manufacturing flexibility and ergonomic quality [1, 5, 9]. By adhering to rigorous international safety standards and addressing integration challenges, engineering teams can fully harness modern robotics to build agile, resilient, and sustainable production architectures for the future."
        ]
    }
]

def calculate_word_count():
    total_words = 0
    for sec in SECTIONS:
        # Include title words
        total_words += len(clean_text_for_word_count(sec["title"]))
        for p in sec["paragraphs"]:
            total_words += len(clean_text_for_word_count(p))
    # Add executive summary words
    exec_summary_text = (
        "The Fourth Industrial Revolution has redefined manufacturing paradigms through the convergence of "
        "cyber-physical systems, autonomous robotics, artificial intelligence, and the Industrial Internet of Things. "
        "Moving beyond traditional isolated workcells, modern factories deploy collaborative robots, autonomous mobile "
        "robots, and edge-driven sensor feedback loops synchronized with real-time digital twins. This comprehensive research "
        "report investigates the architectural pillars, kinematic and sensing technologies, comparative performance metrics, "
        "industrial case studies, safety frameworks under ISO 10218 and ISO/TS 15066, and forward-looking research frontiers "
        "shaping the next generation of intelligent manufacturing systems."
    )
    total_words += len(clean_text_for_word_count(exec_summary_text))
    return total_words, exec_summary_text

def build_pdf(filename="Task_1_Research_Report_Robotics_Industry_4.0.pdf"):
    body_word_count, exec_summary = calculate_word_count()
    print(f"Calculated Body Word Count (Strict): {body_word_count} words")
    assert 1700 <= body_word_count <= 1900, f"Word count {body_word_count} not in range [1700, 1900]!"

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

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=21, leading=25, textColor=primary, spaceAfter=8)
    sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=secondary, spaceAfter=10)
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#4B5563"))
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=primary, spaceBefore=10, spaceAfter=5, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=dark, spaceAfter=5, alignment=4)
    bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=12, firstLineIndent=-8, spaceAfter=3, alignment=4)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=dark, alignment=0)
    callout_style = ParagraphStyle('Callout', parent=body_style, fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor("#1E293B"))

    story = []

    # Title & Header
    story.append(Paragraph("CodeAlpha Robotics & Automation Internship — Task 1", sub_style))
    story.append(Paragraph("Robotics in Manufacturing & Industry 4.0: Autonomous Systems, Cobots, and Digital Twin Integration", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary, spaceBefore=2, spaceAfter=8))

    meta_table_data = [
        [
            Paragraph("<b>Author:</b> CodeAlpha Robotics Intern", meta_style),
            Paragraph("<b>Domain:</b> Robotics & Industrial Automation", meta_style)
        ],
        [
            Paragraph("<b>Submission Date:</b> October 2026", meta_style),
            Paragraph(f"<b>Word Count:</b> {body_word_count:,} Words (Body & Summary; Excl. References)", meta_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[255, 255])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Executive Summary Box
    summary_html = f"<b>Executive Summary:</b> {exec_summary}"
    summary_table = Table([[Paragraph(summary_html, callout_style)]], colWidths=[512])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # Add Sections
    for sec in SECTIONS:
        story.append(Paragraph(sec["title"], h1_style))
        for p in sec["paragraphs"]:
            story.append(Paragraph(p, body_style))
        
        # Insert Table after section 3
        if "3. Comparative Technical Analysis" in sec["title"]:
            table_data = [
                [Paragraph("Feature / Parameter", th_style), Paragraph("Traditional Industrial Manipulator", th_style), Paragraph("Collaborative Robot (Cobot)", th_style)],
                [
                    Paragraph("<b>Safety Framework</b>", tc_style),
                    Paragraph("Physical cages, interlocks, light curtains (ISO 10218-1/2) [1]", tc_style),
                    Paragraph("Power and Force Limiting (PFL), speed/separation monitoring (ISO/TS 15066) [2, 9]", tc_style)
                ],
                [
                    Paragraph("<b>Typical Payload Capacity</b>", tc_style),
                    Paragraph("High (typically 20 kg to over 1,000 kg for heavy body-in-white fabrication) [3]", tc_style),
                    Paragraph("Low to moderate (typically 3 kg to 35 kg; optimized for light handling) [9]", tc_style)
                ],
                [
                    Paragraph("<b>Maximum TCP Speed</b>", tc_style),
                    Paragraph("2.0 m/s to 5.0 m/s; high kinetic energy motion profile [3, 6]", tc_style),
                    Paragraph("Regulated (typically 0.25 m/s to 1.0 m/s within collaborative zone) [2]", tc_style)
                ],
                [
                    Paragraph("<b>Repeatability</b>", tc_style),
                    Paragraph("±0.01 mm to ±0.03 mm (High-rigidity cast iron / cycloidal gearing) [4]", tc_style),
                    Paragraph("±0.03 mm to ±0.1 mm (Elastic joint torque sensors and harmonic drives) [9]", tc_style)
                ],
                [
                    Paragraph("<b>Programming & Setup</b>", tc_style),
                    Paragraph("Proprietary teach pendant scripting (RAPID, KRL, Karel); extended commissioning [6]", tc_style),
                    Paragraph("Hand-guiding lead-through, graphical zero-code interfaces; rapid line reconfiguration [9]", tc_style)
                ],
                [
                    Paragraph("<b>Footprint & Mobility</b>", tc_style),
                    Paragraph("Large fixed footprint, dedicated bolted concrete base [3]", tc_style),
                    Paragraph("Compact, lightweight structure, relocatable onto mobile AMR bases [3, 8]", tc_style)
                ]
            ]
            t1 = Table(table_data, colWidths=[116, 198, 198])
            t1.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), primary),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(Spacer(1, 3))
            story.append(t1)
            story.append(Spacer(1, 5))

    # References Section
    story.append(Spacer(1, 4))
    story.append(Paragraph("9. References", h1_style))
    for ref in REFERENCES:
        story.append(Paragraph(ref, bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Task 1 Report successfully generated: {filename}")
    return body_word_count

def generate_markdown(word_count, exec_summary, md_filename="Research_Report_Industry_4_0.md"):
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write("# CodeAlpha Robotics & Automation Internship — Task 1\n")
        f.write("## Research Report: Robotics in Manufacturing & Industry 4.0: Autonomous Systems, Cobots, and Digital Twin Integration\n\n")
        f.write(f"**Domain:** Robotics & Industrial Automation  \n")
        f.write(f"**Author:** CodeAlpha Robotics Intern  \n")
        f.write(f"**Submission Date:** October 2026  \n")
        f.write(f"**Body Word Count:** {word_count:,} Words (Body & Summary; Excluding References)  \n")
        f.write(f"**PDF Deliverable:** [Task_1_Research_Report_Robotics_Industry_4.0.pdf](Task_1_Research_Report_Robotics_Industry_4.0.pdf)  \n\n")
        f.write("---\n\n")
        f.write(f"### Executive Summary\n{exec_summary}\n\n---\n\n")

        for sec in SECTIONS:
            f.write(f"### {sec['title']}\n\n")
            for p in sec["paragraphs"]:
                # Strip simple html tags for markdown readability
                p_md = p.replace("<b>", "**").replace("</b>", "**").replace("<i>", "*").replace("</i>", "*")
                f.write(f"{p_md}\n\n")
            if "3. Comparative Technical Analysis" in sec["title"]:
                f.write("| Feature / Parameter | Traditional Industrial Manipulator | Collaborative Robot (Cobot) |\n")
                f.write("| :--- | :--- | :--- |\n")
                f.write("| **Safety Framework** | Physical cages, interlocks, light curtains (ISO 10218-1/2) [1] | Power and Force Limiting (PFL), speed/separation monitoring (ISO/TS 15066) [2, 9] |\n")
                f.write("| **Typical Payload Capacity** | High (typically 20 kg to over 1,000 kg) [3] | Low to moderate (typically 3 kg to 35 kg) [9] |\n")
                f.write("| **Maximum TCP Speed** | 2.0 m/s to 5.0 m/s; high kinetic energy motion profile [3, 6] | Regulated (typically 0.25 m/s to 1.0 m/s within collaborative zone) [2] |\n")
                f.write("| **Repeatability** | ±0.01 mm to ±0.03 mm [4] | ±0.03 mm to ±0.1 mm [9] |\n")
                f.write("| **Programming & Setup** | Proprietary teach pendant scripting (RAPID, KRL, Karel) [6] | Hand-guiding lead-through, graphical zero-code interfaces [9] |\n")
                f.write("| **Footprint & Mobility** | Large fixed footprint, dedicated bolted base [3] | Compact, lightweight, mountable on mobile AMR bases [3, 8] |\n\n")

        f.write("### 9. References\n\n")
        for ref in REFERENCES:
            f.write(f"- {ref}\n")
    print(f"Task 1 Markdown successfully generated: {md_filename}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "Task_1_Research_Report_Robotics_Industry_4.0.pdf")
    md_path = os.path.join(base_dir, "Research_Report_Industry_4_0.md")
    wc, summary = calculate_word_count()
    build_pdf(pdf_path)
    generate_markdown(wc, summary, md_path)
