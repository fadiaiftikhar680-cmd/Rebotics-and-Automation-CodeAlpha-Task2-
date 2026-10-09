import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_flowchart(save_path):
    fig, ax = plt.subplots(figsize=(11, 15), dpi=200)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 15)
    ax.axis('off')

    # Palette
    c_start = '#1E3A8A'      # Dark Blue
    c_proc = '#0284C7'       # Cyan Blue
    c_dec = '#D97706'        # Amber
    c_sens = '#0D9488'       # Teal
    c_reject = '#DC2626'     # Red
    c_border = '#0F172A'

    # Title Banner
    ax.text(5.5, 14.6, "AUTOMATED CONVEYOR SORTING & PACKAGING WORKFLOW", fontsize=13, fontweight='bold', ha='center', color='#0F172A')
    ax.text(5.5, 14.25, "Finite State Machine with Multi-Sensor Validation, Dual Reject Loops & E-Stop Safety Branch", fontsize=8.5, ha='center', color='#475569')

    def draw_box(btype, x, y, w, h, text, col, text_col='white', fsize=8):
        if btype == 'round':
            p = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.35", facecolor=col, edgecolor=c_border, linewidth=1.4)
        elif btype == 'diamond':
            pts = [(x + w/2, y + h), (x + w, y + h/2), (x + w/2, y), (x, y + h/2)]
            p = patches.Polygon(pts, facecolor=col, edgecolor=c_border, linewidth=1.4)
        else: # rect
            p = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.1", facecolor=col, edgecolor=c_border, linewidth=1.4)
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text, fontsize=fsize, fontweight='bold', ha='center', va='center', color=text_col)

    def draw_arrow(x1, y1, x2, y2, label=None, label_pos=None, lcol='#0F172A'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=lcol, edgecolor=lcol, width=1.4, headwidth=5.5, shrink=0.04))
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label, fontsize=7.5, fontweight='bold', color=lcol, ha='center', va='center')

    # Main Spine Sequence (x=3.4, w=4.2)
    bx = 3.4
    bw = 4.2

    draw_box('round', bx, 13.2, bw, 0.75, "START: Power-Up & Safety Reset\nPilz PNOZ Closed (%I0.4 = TRUE)", c_start)
    draw_box('rect', bx, 12.0, bw, 0.75, "Initialize PLC Scan & Energize Contactor\nStart VFD Conveyor (%Q0.0 Run, %Q0.1 Preset 50Hz)", c_proc)
    draw_box('rect', bx, 10.8, bw, 0.75, "Sensor S1 (Photoelectric %I0.0)\nInfeed Workpiece Leading-Edge Detected", c_sens)
    draw_box('diamond', bx, 9.4, bw, 0.95, "Inspection Stage 1:\nS2 Metal (%I0.1) & S3 Color (%I0.2) & S4 Height (%IW64)\nAll Within Specifications?", c_dec, '#0F172A', 7.5)
    
    # Reject 1 (Right branch)
    draw_box('rect', 8.1, 9.4, 2.5, 0.95, "ACTUATE DIVERTER 1 (%Q0.2)\nPneumatic Pusher 1 Ejection\n➔ Route to Rework Buffer", c_reject, 'white', 7.5)

    draw_box('rect', bx, 8.0, bw, 0.75, "Sensor S5 (Load Cell Transmitter %IW66)\nDynamic Gross Mass Measurement (250g ± 5g)", c_sens)
    draw_box('diamond', bx, 6.6, bw, 0.95, "Inspection Stage 2:\nMass Within Specified Window\n(245.0 g ≤ M ≤ 255.0 g)?", c_dec, '#0F172A', 7.5)

    # Reject 2 (Right branch)
    draw_box('rect', 8.1, 6.6, 2.5, 0.95, "ACTUATE DIVERTER 2 (%Q0.3)\nPneumatic Pusher 2 Ejection\n➔ Route to Rework Buffer", c_reject, 'white', 7.5)

    draw_box('rect', bx, 5.2, bw, 0.75, "Packaging & Cartoner Station\nActuate Heat Sealer SSR (%Q0.4 Pulse 1.2s)", c_proc)
    draw_box('rect', bx, 4.0, bw, 0.75, "Sensor S6 (Optical Exit Barrier %I0.3)\nDetect Exit & Increment Production Counter", c_sens)
    draw_box('diamond', bx, 2.6, bw, 0.95, "Batch Target Reached\n(Count ≥ Target Batch N)?", c_dec, '#0F172A', 7.5)
    draw_box('round', bx, 1.4, bw, 0.75, "BATCH COMPLETE: Stop VFD Drive\nDe-energize %Q0.0 / Announce Completion", c_start)

    # Emergency Stop Branch (Left side, x=0.5, w=2.4)
    draw_box('round', 0.5, 7.5, 2.4, 2.0, "EMERGENCY STOP / FAULT\n• E-Stop Pressed (%I0.4 = 0)\n• Drop STO Contactor K0\n• Halt VFD Instantly\n• De-energize Solenoids\n• Activate Red Beacon & Siren\n(%Q0.6 = TRUE)", c_reject, 'white', 7.5)

    # Connectors
    draw_arrow(5.5, 13.2, 5.5, 12.75)
    draw_arrow(5.5, 12.0, 5.5, 11.55)
    draw_arrow(5.5, 10.8, 5.5, 10.35)
    
    # Dec 1 to Dec 2
    draw_arrow(5.5, 9.4, 5.5, 8.75, "YES: PASSED", (5.5, 9.05))
    # Dec 1 to Reject 1
    draw_arrow(7.6, 9.875, 8.1, 9.875, "NO: FAIL", (7.85, 10.05))

    # Dec 2 to Process
    draw_arrow(5.5, 8.0, 5.5, 7.55)
    draw_arrow(5.5, 6.6, 5.5, 5.95, "YES: PASSED", (5.5, 6.25))
    # Dec 2 to Reject 2
    draw_arrow(7.6, 7.075, 8.1, 7.075, "NO: FAIL", (7.85, 7.25))

    draw_arrow(5.5, 5.2, 5.5, 4.75)
    draw_arrow(5.5, 4.0, 5.5, 3.55)
    draw_arrow(5.5, 2.6, 5.5, 2.15, "YES", (5.5, 2.35))

    # Loopback from Batch Target = NO (Return to S1 Infeed)
    ax.plot([3.4, 2.5, 2.5, 3.4], [3.075, 3.075, 11.175, 11.175], color='#0F172A', linewidth=1.4, linestyle='--')
    ax.annotate('', xy=(3.4, 11.175), xytext=(2.7, 11.175),
                arrowprops=dict(facecolor='#0F172A', edgecolor='#0F172A', width=1.4, headwidth=5.5))
    ax.text(2.35, 7.0, "NO: Next Item Infeed", fontsize=7.5, fontweight='bold', color='#1E293B', rotation=90, va='center')

    # Reject Loopback from Rework Buffer to Infeed
    ax.plot([9.35, 9.35, 10.7, 10.7, 5.5], [9.4, 8.8, 8.8, 11.7, 11.7], color='#DC2626', linewidth=1.3, linestyle=':')
    ax.plot([9.35, 9.35], [6.6, 8.8], color='#DC2626', linewidth=1.3, linestyle=':')
    ax.annotate('', xy=(5.5, 11.7), xytext=(6.5, 11.7),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=1.3, headwidth=5.5))
    ax.text(10.5, 10.3, "Rework Sorting Re-Entry Loop", fontsize=7, fontweight='bold', color='#DC2626', rotation=-90, va='center')

    # Safety interrupt lines from main loop to E-stop block
    ax.plot([3.4, 2.9], [12.375, 8.5], color='#DC2626', linewidth=1.2, linestyle='-.')
    ax.annotate('', xy=(2.9, 8.5), xytext=(3.4, 12.375),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=1.2, headwidth=5))
    ax.text(2.6, 10.8, "E-Stop\nTrip", fontsize=7, fontweight='bold', color='#DC2626', ha='center')

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Flowchart successfully generated: {save_path}")

def draw_circuit_schematic(save_path):
    fig, ax = plt.subplots(figsize=(13, 8.5), dpi=200)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Outer border
    ax.add_patch(patches.Rectangle((0.15, 0.15), 12.7, 8.2, facecolor='#F8FAFC', edgecolor='#64748B', linewidth=1.4))

    # Title Banner
    ax.text(6.5, 8.05, "ELECTRICAL CONTROL SYSTEM & PLC WIRING SCHEMATIC", fontsize=13, fontweight='bold', ha='center', color='#1E3A8A')
    ax.text(6.5, 7.75, "Conveyor Sorting & Packaging Automation (Siemens SIMATIC S7-1200 CPU 1214C DC/DC/DC Architecture)", fontsize=8.5, ha='center', color='#475569')

    # Section 1: Power & Safety Distribution (Left, x=0.4 to 3.2)
    # AC Mains & MCB
    ax.add_patch(patches.FancyBboxPatch((0.4, 5.7), 2.8, 1.8, boxstyle="round,pad=0.04", facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.3))
    ax.text(1.8, 7.25, "POWER MAINS & SMPS", fontsize=8.5, fontweight='bold', ha='center', color='#92400E')
    ax.text(1.8, 6.85, "230V AC (L1, N, PE) Mains Input", fontsize=7.5, ha='center', color='#78350F')
    ax.text(1.8, 6.45, "➔ 2-Pole 10A MCB (QF1)", fontsize=7.5, ha='center', color='#78350F')
    ax.text(1.8, 6.05, "➔ Mean Well NDR-120-24 SMPS\n    Output: 24V DC / 5A Regulated", fontsize=7, ha='center', color='#78350F')

    # Safety Relay Block (Pilz PNOZ X3)
    ax.add_patch(patches.FancyBboxPatch((0.4, 3.4), 2.8, 2.1, boxstyle="round,pad=0.04", facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.3))
    ax.text(1.8, 5.25, "SAFETY CIRCUIT (PL d / CAT 3)", fontsize=8, fontweight='bold', ha='center', color='#991B1B')
    ax.text(1.8, 4.85, "Dual-Channel E-Stop (NC)", fontsize=7.5, ha='center', color='#7F1D1D')
    ax.text(1.8, 4.50, "➔ Pilz PNOZ X3 Safety Relay\n    Terminals S11-S12 & S21-S22", fontsize=7, ha='center', color='#7F1D1D')
    ax.text(1.8, 4.05, "➔ Safety Contactor K0 (Main VFD Cut)\n➔ Aux Status ➔ PLC Input %I0.4", fontsize=7, ha='center', color='#7F1D1D')
    ax.text(1.8, 3.65, "Manual Reset Button (S_RST)", fontsize=7, ha='center', color='#991B1B')

    # Section 2: Sensor Field (Bottom Left, x=0.4 to 3.2)
    ax.add_patch(patches.FancyBboxPatch((0.4, 0.4), 2.8, 2.8, boxstyle="round,pad=0.04", facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1.3))
    ax.text(1.8, 2.95, "SENSOR FIELD (3-WIRE PNP)", fontsize=8, fontweight='bold', ha='center', color='#0369A1')
    sensor_labels = [
        "S1: Photoelectric Infeed (%I0.0)",
        "S2: Inductive Metallic (%I0.1)",
        "S3: Color/Contrast (%I0.2)",
        "S6: Optical Exit Barrier (%I0.3)",
        "S4: Ultrasonic Height (0-10V) ➔ AI0",
        "S5: Load Cell Amp (0-10V) ➔ AI1",
        "Wire Colors: BN=+24V, BU=0V, BK=Sig"
    ]
    for i, slab in enumerate(sensor_labels):
        col = '#0F172A' if i < 6 else '#0369A1'
        fnt = 6.8 if i == 6 else 7.2
        ax.text(0.55, 2.65 - i*0.35, slab, fontsize=fnt, color=col, family='monospace')

    # Section 3: Central PLC Controller (Middle, x=3.7 to 8.2)
    ax.add_patch(patches.FancyBboxPatch((3.7, 0.4), 4.5, 7.1, boxstyle="round,pad=0.06", facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.8))
    ax.text(5.95, 7.15, "SIEMENS SIMATIC S7-1200", fontsize=11, fontweight='bold', ha='center', color='#38BDF8')
    ax.text(5.95, 6.85, "CPU 1214C DC/DC/DC (6ES7214-1AG40-0XB0)", fontsize=8, ha='center', color='#94A3B8')

    # Power Terminals
    ax.text(4.0, 6.45, "POWER: L+ (24V DC), M (0V DC)", fontsize=7.5, color='#FCD34D', family='monospace')

    # Left: Digital & Analog Inputs
    ax.text(4.0, 6.0, "DIGITAL INPUTS (24V DC)", fontsize=7.5, fontweight='bold', color='#38BDF8')
    d_inputs = [
        ("%I0.0", "Infeed Presence (S1)"),
        ("%I0.1", "Metal Cap Verify (S2)"),
        ("%I0.2", "Color Label Verify (S3)"),
        ("%I0.3", "Exit Batch Barrier (S6)"),
        ("%I0.4", "Safety Relay Status (PNOZ)")
    ]
    for i, (pin, desc) in enumerate(d_inputs):
        yp = 5.6 - i*0.42
        ax.add_patch(patches.Circle((4.0, yp), 0.08, facecolor='#10B981', edgecolor='white'))
        ax.text(4.2, yp - 0.04, f"{pin}: {desc}", fontsize=6.8, color='#E2E8F0', family='monospace')

    ax.text(4.0, 3.3, "ANALOG INPUTS (0-10V DC Onboard)", fontsize=7.5, fontweight='bold', color='#F59E0B')
    a_inputs = [
        ("%IW64", "AI0: S4 Height (0-10V)"),
        ("%IW66", "AI1: S5 Load Cell (0-10V)")
    ]
    for i, (pin, desc) in enumerate(a_inputs):
        yp = 2.9 - i*0.42
        ax.add_patch(patches.Circle((4.0, yp), 0.08, facecolor='#F59E0B', edgecolor='white'))
        ax.text(4.2, yp - 0.04, f"{pin}: {desc}", fontsize=6.8, color='#E2E8F0', family='monospace')

    # Right: Digital Outputs (Solid-State Transistors 0.5A)
    ax.text(6.1, 6.0, "TRANSISTOR OUTPUTS (24V 0.5A)", fontsize=7.5, fontweight='bold', color='#38BDF8')
    d_outputs = [
        ("%Q0.0", "VFD Run Relay K1"),
        ("%Q0.1", "VFD Speed Select Relay K2"),
        ("%Q0.2", "Pneumatic Diverter Solenoid 1"),
        ("%Q0.3", "Pneumatic Diverter Solenoid 2"),
        ("%Q0.4", "Cartoner Heater SSR-25DA"),
        ("%Q0.5", "Stack Light Green Lamp"),
        ("%Q0.6", "Stack Light Red & Alarm Siren")
    ]
    for i, (pin, desc) in enumerate(d_outputs):
        yp = 5.6 - i*0.42
        ax.add_patch(patches.Circle((8.0, yp), 0.08, facecolor='#EF4444', edgecolor='white'))
        ax.text(7.85, yp - 0.04, f"{pin}: {desc}", fontsize=6.8, color='#E2E8F0', family='monospace', ha='right')

    ax.text(5.95, 0.8, "PROFINET Port (RJ45) ➔ Engineering HMI / SCADA", fontsize=7, color='#10B981', family='monospace', ha='center')

    # Section 4: Actuator Modules (Right, x=8.7 to 12.5)
    # VFD & Motor
    ax.add_patch(patches.FancyBboxPatch((8.7, 5.2), 3.8, 2.3, boxstyle="round,pad=0.04", facecolor='#F1F5F9', edgecolor='#475569', linewidth=1.3))
    ax.text(10.6, 7.2, "VFD & CONVEYOR MOTOR", fontsize=8.5, fontweight='bold', ha='center', color='#1E293B')
    ax.text(10.6, 6.8, "Siemens SINAMICS V20 (0.75 kW)", fontsize=7.5, ha='center', color='#334155')
    ax.text(10.6, 6.45, "• DI1 Terminal ➔ Run/Stop via K1 Contact\n• DI2 Terminal ➔ 50 Hz Preset via K2 Contact\n• STO Safety Interlock from Contactor K0", fontsize=7, ha='center', color='#475569')
    ax.text(10.6, 5.5, "➔ SEW-Eurodrive 3-Phase AC Motor WA30", fontsize=7.5, fontweight='bold', ha='center', color='#1E293B')

    # Pneumatic Solenoids
    ax.add_patch(patches.FancyBboxPatch((8.7, 2.9), 3.8, 2.1, boxstyle="round,pad=0.04", facecolor='#ECFDF5', edgecolor='#059669', linewidth=1.3))
    ax.text(10.6, 4.7, "PNEUMATIC ACTUATION (6.0 BAR)", fontsize=8, fontweight='bold', ha='center', color='#065F46')
    ax.text(10.6, 4.3, "Festo 5/2-Way Solenoid Valves (24V DC)", fontsize=7.5, ha='center', color='#047857')
    ax.text(10.6, 3.9, "• Solenoid 1 (%Q0.2) + 1N4007 Diode ➔ Pusher 1\n• Solenoid 2 (%Q0.3) + 1N4007 Diode ➔ Pusher 2", fontsize=7, ha='center', color='#065F46')
    ax.text(10.6, 3.25, "Dual-Action Air Cylinders (DSNU-25-100)", fontsize=7, ha='center', color='#047857')

    # Heater SSR & Annunciation
    ax.add_patch(patches.FancyBboxPatch((8.7, 0.4), 3.8, 2.3, boxstyle="round,pad=0.04", facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.3))
    ax.text(10.6, 2.4, "PACKAGING & ANNUNCIATION", fontsize=8, fontweight='bold', ha='center', color='#991B1B')
    ax.text(10.6, 2.0, "• SSR-25DA (%Q0.4) ➔ 230V Cartoner Heater Wire\n• %Q0.5 ➔ 24V Stack Light Green Lamp\n• %Q0.6 ➔ 24V Stack Light Red & 85dB Siren", fontsize=7, ha='center', color='#7F1D1D')
    ax.text(10.6, 0.8, "Flyback Diodes (1N4007) Suppress Inductive Spikes", fontsize=7, fontweight='bold', ha='center', color='#991B1B')

    # Clean connection lines (No overlaps)
    # Sensor field to PLC
    ax.plot([3.2, 3.9], [2.65, 5.6], color='#0284C7', linewidth=1.2, linestyle=':')
    ax.plot([3.2, 3.9], [1.25, 2.9], color='#F59E0B', linewidth=1.2, linestyle=':')

    # PLC outputs to actuators
    ax.plot([8.1, 8.7], [5.6, 6.4], color='#2563EB', linewidth=1.2)
    ax.plot([8.1, 8.7], [4.76, 4.1], color='#059669', linewidth=1.2)
    ax.plot([8.1, 8.7], [3.92, 1.8], color='#DC2626', linewidth=1.2)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Circuit schematic successfully generated: {save_path}")

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    draw_flowchart(os.path.join(here, "flowchart_packaging_system.png"))
    draw_circuit_schematic(os.path.join(here, "circuit_diagram_automation.png"))
