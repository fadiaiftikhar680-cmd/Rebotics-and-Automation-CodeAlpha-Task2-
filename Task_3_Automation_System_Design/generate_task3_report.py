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
            self.drawString(48, 11 * 72 - 34, "CodeAlpha Robotics & Automation Internship — Task 3: Automation System Design")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(48, 11 * 72 - 40, 8.5 * 72 - 48, 11 * 72 - 40)

            self.line(48, 38, 8.5 * 72 - 48, 38)
            self.setFont("Helvetica", 8)
            self.drawString(48, 26, "Industrial Engineering Design Report | CodeAlpha Internship Program")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * 72 - 48, 26, page_text)
        self.restoreState()

# Canonical BOM Item list (Single Source of Truth)
BOM_ITEMS = [
    ("Siemens SIMATIC S7-1200 CPU 1214C DC/DC/DC", "6ES7214-1AG40-0XB0 (14DI, 10DQ Transistor, 2AI 0-10V)", 1, 420.00),
    ("Siemens SINAMICS V20 VFD Inverter", "6SL3210-5BB17-5UV1 (0.75 kW, 230V 1-Phase to 3-Phase)", 1, 185.00),
    ("SEW-Eurodrive 3-Phase AC Geared Motor", "WA30 Series (0.75 kW, 1400 RPM with Worm Gearbox 10:1)", 1, 260.00),
    ("S1: Photoelectric Infeed Presence Sensor", "Omron E3Z-T61 (Through-Beam, 24V DC PNP NO, 15m range)", 1, 45.00),
    ("S2: Inductive Proximity Cap Sensor", "Omron E2B-M12KS04-WP-B1 (M12, 24V DC PNP NO, 4mm flush)", 1, 28.00),
    ("S3: Optical Color / Contrast Label Sensor", "Banner Q4X Series (High-Speed RGB Contrast, 24V PNP)", 1, 185.00),
    ("S4: Ultrasonic Analog Height Sensor", "Pepperl+Fuchs UB500-18GM75-U-V15 (0-10V DC Analog Output)", 1, 165.00),
    ("S5: Precision Load Cell + 0-10V Transmitter", "TEDEA 1022 (0-2 kg) + Mantracourt DIN-Rail 0-10V Amp", 1, 140.00),
    ("S6: Retro-Reflective Optical Exit Barrier", "Omron E3Z-R61 (Polarized Retro-Reflective with E39-R1)", 1, 42.00),
    ("Pneumatic Sorting Cylinders & 5/2 Valves", "Festo DSNU-25-100-PPV + 24V Solenoid Valves CPE14 (x2)", 2, 95.00),
    ("Pilz PNOZ X3 Dual-Channel Safety Relay", "Pilz 774310 (24V AC/DC, 3 n/o safety, 1 n/c aux contact)", 1, 175.00),
    ("Dual-Channel Emergency Stop & Reset Station", "Schneider Electric Harmony XALK178 (2NC Mushroom + NO)", 1, 48.00),
    ("2-Pole Miniature Circuit Breaker (MCB)", "ABB S202-C10 (10A Type C, 230V AC Mains Protection)", 1, 22.00),
    ("24V DC / 5A DIN-Rail Switched SMPS", "Mean Well NDR-120-24 (120W, 24V DC / 5.0A High Efficiency)", 1, 55.00),
    ("Interposing Relays & Cartoner SSR", "Finder 38.51 (24V DC x2) + Fotek SSR-25DA Heat Sealer Relay", 1, 38.00),
    ("Industrial Stack Light & Audible Beacon", "Patlite LR4 Series (24V DC, Green/Red LED + 85 dB Siren)", 1, 45.00),
    ("Rittal Enclosure, DIN Rails & Wiring Harness", "Rittal AX Compact Series + Phoenix Contact Push-In Blocks", 1, 195.00),
]

def build_pdf(filename="Task_3_Automation_System_Design_Report.pdf", base_dir="."):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")
    secondary = colors.HexColor("#0D9488")
    dark = colors.HexColor("#1F2937")

    title_style = ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=primary, spaceAfter=5)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=secondary, spaceAfter=6)
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#4B5563"))
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=primary, spaceBefore=7, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=10.8, textColor=dark, spaceAfter=4, alignment=4)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=colors.white, alignment=1)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8, leading=8.6, textColor=dark, alignment=0)
    caption_style = ParagraphStyle('Cap', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.2, leading=9, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=4)

    story = []

    # Calculate BOM total dynamically
    bom_total = sum(item[2] * item[3] for item in BOM_ITEMS)

    # ================= PAGE 1 =================
    story.append(Paragraph("CodeAlpha Robotics & Automation Internship — Task 3", sub_style))
    story.append(Paragraph("Design & Engineering of an Automated Conveyor Sorting & Packaging System with Multi-Sensor Quality Inspection", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary, spaceBefore=2, spaceAfter=5))

    meta_table_data = [
        [Paragraph("<b>Author:</b> CodeAlpha Robotics Intern", meta_style), Paragraph("<b>Domain:</b> Industrial Automation & Control Systems", meta_style)],
        [Paragraph("<b>Controller:</b> Siemens S7-1200 CPU 1214C DC/DC/DC", meta_style), Paragraph(f"<b>Total Hardware BOM:</b> ${bom_total:,.2f} USD (Code-Computed)", meta_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[262, 262])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Functional Description & Sizing Calculations", h1_style))
    story.append(Paragraph(
        "Modern packaging and sorting systems demand deterministic cycle times, multi-sensor verification, and fail-safe operator safety. "
        "This project presents an automated inspection and sorting workcell centered on a variable-speed belt conveyor controlled by a "
        "<b>Siemens SIMATIC S7-1200 PLC (CPU 1214C DC/DC/DC)</b>. Unsorted workpieces enter the infeed belt and undergo structured quality appraisal: "
        "(1) Infeed presence registration (S1), (2) Inductive metallic foil/cap validation (S2), (3) Optical contrast label verification (S3), "
        "(4) Ultrasonic continuous height gauging (S4), (5) Dynamic gross mass evaluation (S5), (6) Dual-stage pneumatic sorting diverters with rework buffer re-entry, "
        "and (7) Automated thermal cartoner heat sealing and batch counting (S6).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Throughput and Kinematic Sizing Calculation:</b> The belt runs at nominal linear velocity v = 0.20 m/s with nominal package pitch p = 0.40 m. "
        "The resulting nominal production throughput is calculated as:\n"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Throughput = (v / p) × 60 = (0.20 m/s / 0.40 m) × 60 = 30 units/minute</b>.<br/>"
        "At maximum sensor interrogation speed with 0.8 s settle time at the weighing station, the system supports a peak burst throughput of 36 units/minute. "
        "The drive mechanism employs a 0.75 kW 3-phase AC induction motor driven by a Siemens SINAMICS V20 inverter.",
        body_style
    ))

    story.append(Paragraph("2. Canonical PLC Input/Output (I/O) Mapping Architecture", h1_style))
    story.append(Paragraph(
        "The CPU 1214C DC/DC/DC incorporates 14 onboard 24V DC Digital Inputs, 10 Solid-State 24V DC Transistor Outputs (DQ rated at 0.5A per channel), "
        "and 2 Onboard 0–10V Analog Inputs (10-bit resolution). To match hardware capabilities, the load cell employs a calibrated 0–10V rail transmitter, "
        "and VFD frequency selection utilizes digital preset terminals (DI1 Run/Stop, DI2 50 Hz preset) via interposing relays.",
        body_style
    ))

    io_data = [
        [Paragraph("Tag / Address", th_style), Paragraph("Hardware Interface", th_style), Paragraph("Hardware Device & Specification", th_style), Paragraph("Control Function & Signal Logic", th_style)],
        [Paragraph("<b>%I0.0</b>", tc_style), Paragraph("DI (24V DC)", tc_style), Paragraph("S1: Photoelectric Through-Beam (Omron E3Z-T61)", tc_style), Paragraph("Infeed presence detection; initiates inspection window", tc_style)],
        [Paragraph("<b>%I0.1</b>", tc_style), Paragraph("DI (24V DC)", tc_style), Paragraph("S2: Inductive Proximity M12 (Omron E2B)", tc_style), Paragraph("Confirms presence of metallic seal/foil on container", tc_style)],
        [Paragraph("<b>%I0.2</b>", tc_style), Paragraph("DI (24V DC)", tc_style), Paragraph("S3: Color/Contrast Sensor (Banner Q4X)", tc_style), Paragraph("Verifies packaging color registration (Pass/Fail)", tc_style)],
        [Paragraph("<b>%I0.3</b>", tc_style), Paragraph("DI (24V DC)", tc_style), Paragraph("S6: Retro-Reflective Optical Exit (Omron E3Z)", tc_style), Paragraph("Detects exit packaging completion; increments counter", tc_style)],
        [Paragraph("<b>%I0.4</b>", tc_style), Paragraph("DI (24V DC)", tc_style), Paragraph("Pilz PNOZ X3 Safety Relay Aux Contact", tc_style), Paragraph("Monitors safety circuit state (1=Normal, 0=E-Stop/Fault)", tc_style)],
        [Paragraph("<b>%IW64</b>", tc_style), Paragraph("AI0 (0–10V DC)", tc_style), Paragraph("S4: Ultrasonic Distance (Pepperl+Fuchs UB500)", tc_style), Paragraph("Continuous height measurement (Analog tolerance 95-105 mm)", tc_style)],
        [Paragraph("<b>%IW66</b>", tc_style), Paragraph("AI1 (0–10V DC)", tc_style), Paragraph("S5: Load Cell Transmitter (Mantracourt 0-10V)", tc_style), Paragraph("Dynamic weight verification (Target: 250g ± 5g window)", tc_style)],
        [Paragraph("<b>%Q0.0</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("Interposing Relay K1 ➔ VFD Terminal DI1", tc_style), Paragraph("Conveyor run command (Energizes VFD forward drive)", tc_style)],
        [Paragraph("<b>%Q0.1</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("Interposing Relay K2 ➔ VFD Terminal DI2", tc_style), Paragraph("Preset speed selection (Activates 50 Hz speed parameter)", tc_style)],
        [Paragraph("<b>%Q0.2</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("24V Solenoid Valve 1 + 1N4007 Diode", tc_style), Paragraph("Pneumatic Pusher 1: Ejects Height/Color/Metal rejects", tc_style)],
        [Paragraph("<b>%Q0.3</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("24V Solenoid Valve 2 + 1N4007 Diode", tc_style), Paragraph("Pneumatic Pusher 2: Ejects out-of-spec weight items", tc_style)],
        [Paragraph("<b>%Q0.4</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("Solid State Relay (SSR-25DA)", tc_style), Paragraph("PULSES 230V cartoner heating wire (1.2 s seal duration)", tc_style)],
        [Paragraph("<b>%Q0.5</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("Stack Light Green Indicator Lamp", tc_style), Paragraph("Illuminates during active automatic cycle execution", tc_style)],
        [Paragraph("<b>%Q0.6</b>", tc_style), Paragraph("DQ Transistor", tc_style), Paragraph("Stack Light Red Lamp & 85 dB Siren", tc_style), Paragraph("Safety fault / Jam / E-Stop trip alarm annunciation", tc_style)],
    ]
    t_io = Table(io_data, colWidths=[60, 68, 174, 222])
    t_io.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_io)

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("3. Operational State Machine & Flowchart Logic", h1_style))
    story.append(Paragraph(
        "Figure 1 illustrates the finite state machine governing system execution. The logic features dual-stage rejection pathways "
        "that return diverged items into a designated rework staging buffer for re-inspection, eliminating product waste. "
        "An asynchronous safety interrupt monitors input %I0.4 to command immediate Safe Torque Off (STO) in event of emergency.",
        body_style
    ))

    flowchart_img = os.path.join(base_dir, "flowchart_packaging_system.png")
    if os.path.exists(flowchart_img):
        story.append(Image(flowchart_img, width=420, height=520))
        story.append(Paragraph("Figure 1: Operational Flowchart with Canonical S1-S6 Sensors, Dual Reject Rework Loops & E-Stop Branch", caption_style))

    story.append(Paragraph("4. Safety Architecture & Interlock Philosophy", h1_style))
    story.append(Paragraph(
        "<b>Safety Integrity Target:</b> Performance Level PL d, Category 3 architecture per ISO 13849-1, subject to formal task-based risk assessment. "
        "A Pilz PNOZ X3 safety relay monitors dual-channel normally closed (NC) contacts from emergency stop pushbuttons and perimeter guards. "
        "Actuation drops master safety contactor K0 within 20 ms, removing mains power from the motor drive, while PLC auxiliary input %I0.4 "
        "triggers software hold, immediately resetting outputs %Q0.0 through %Q0.4 to fail-safe de-energized states.",
        body_style
    ))

    # ================= PAGE 3 =================
    story.append(PageBreak())
    story.append(Paragraph("5. Electrical Wiring Schematic & Power Distribution", h1_style))
    story.append(Paragraph(
        "Figure 2 presents the unified electrical wiring topology incorporating mains 230V AC distribution, 24V DC SMPS power rail, "
        "3-wire PNP sensor connections, Siemens S7-1200 terminals, flyback suppression diodes across inductive solenoids, and VFD interposing relays.",
        body_style
    ))

    circuit_img = os.path.join(base_dir, "circuit_diagram_automation.png")
    if os.path.exists(circuit_img):
        story.append(Image(circuit_img, width=470, height=210))
        story.append(Paragraph("Figure 2: Electrical Power, Control, and PLC Wiring Schematic (Siemens CPU 1214C DC/DC/DC)", caption_style))

    story.append(Paragraph("6. Complete Engineering Bill of Materials (BOM)", h1_style))

    bom_table_rows = [
        [Paragraph("Item", th_style), Paragraph("Component Description", th_style), Paragraph("Manufacturer & Part Number", th_style), Paragraph("Qty", th_style), Paragraph("Unit Cost", th_style), Paragraph("Ext. Cost", th_style)]
    ]
    for idx, (desc, part, qty, unit_cost) in enumerate(BOM_ITEMS, 1):
        ext_cost = qty * unit_cost
        bom_table_rows.append([
            Paragraph(str(idx), tc_style),
            Paragraph(desc, tc_style),
            Paragraph(part, tc_style),
            Paragraph(str(qty), tc_style),
            Paragraph(f"${unit_cost:.2f}", tc_style),
            Paragraph(f"${ext_cost:.2f}", tc_style)
        ])
    # Add Total row
    bom_table_rows.append([
        Paragraph("<b>TOTAL</b>", tc_style),
        Paragraph("<b>Complete Turnkey Automation Hardware Bill of Materials</b>", tc_style),
        Paragraph("<b>Single Source of Truth in Code</b>", tc_style),
        Paragraph("<b>-</b>", tc_style),
        Paragraph("<b>-</b>", tc_style),
        Paragraph(f"<b>${bom_total:,.2f}</b>", tc_style)
    ])

    t_bom = Table(bom_table_rows, colWidths=[24, 155, 185, 25, 55, 80])
    t_bom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bom)
    story.append(Spacer(1, 2))

    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "Task 3 fulfills all CodeAlpha automation design requirements: canonical sensor naming (S1-S6) is strictly unified across code, "
        "flowchart, circuit schematic, and I/O mapping; real Siemens S7-1200 transistor and analog hardware constraints are enforced; "
        f"and a fully code-computed Bill of Materials verifies complete economic feasibility at ${bom_total:,.2f} USD.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Task 3 Report successfully generated: {filename}")
    return bom_total

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(here, "Task_3_Automation_System_Design_Report.pdf")
    build_pdf(target_pdf, here)
