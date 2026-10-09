import os
import re
import pypdf

def run_qa():
    print("=" * 80)
    print("MANDATORY FINAL QA & COMPLIANCE VERIFICATION RUN")
    print("=" * 80)

    # 1. Check Task 1
    t1_pdf = "Task_1_Research_Report/Task_1_Research_Report_Robotics_Industry_4.0.pdf"
    assert os.path.exists(t1_pdf), f"Missing {t1_pdf}"
    r1 = pypdf.PdfReader(t1_pdf)
    t1_pages = len(r1.pages)
    t1_text = "".join(p.extract_text() or "" for p in r1.pages)
    
    # Import Task 1 word count function
    import Task_1_Research_Report.generate_report as g1
    wc1, _ = g1.calculate_word_count()
    print(f"Task 1: {t1_pages} pages, {wc1} words body text (Target: 1700-1900)")
    assert 1700 <= wc1 <= 1900, f"Task 1 word count {wc1} out of bounds!"
    assert not re.search(r'\$[a-zA-Z\\_^{}]', t1_text), "Raw LaTeX in Task 1!"
    assert '■' not in t1_text and '\u25a0' not in t1_text, "Broken glyph in Task 1!"
    assert 'TODO' not in t1_text, "TODO in Task 1!"

    # 2. Check Task 2
    t2_pdf = "Task_2_Robotic_Arm_Simulation/Task_2_Robotic_Arm_Simulation_Report.pdf"
    assert os.path.exists(t2_pdf), f"Missing {t2_pdf}"
    r2 = pypdf.PdfReader(t2_pdf)
    t2_pages = len(r2.pages)
    t2_text = "".join(p.extract_text() or "" for p in r2.pages)
    print(f"Task 2: {t2_pages} pages (Target: <= 4 pages)")
    assert t2_pages <= 4, f"Task 2 page count {t2_pages} exceeds 4!"
    assert not re.search(r'\$[a-zA-Z\\_^{}]', t2_text), "Raw LaTeX in Task 2!"
    assert '■' not in t2_text and '\u25a0' not in t2_text, "Broken glyph in Task 2!"
    assert 'TODO' not in t2_text, "TODO in Task 2!"

    # Check CAD models
    cad_files = [
        "Task_2_Robotic_Arm_Simulation/cad_models/01_base_pedestal.stl",
        "Task_2_Robotic_Arm_Simulation/cad_models/02_shoulder_turret_link.stl",
        "Task_2_Robotic_Arm_Simulation/cad_models/03_upper_arm_link.stl",
        "Task_2_Robotic_Arm_Simulation/cad_models/04_forearm_link.stl",
        "Task_2_Robotic_Arm_Simulation/cad_models/05_end_effector_gripper.stl",
        "Task_2_Robotic_Arm_Simulation/cad_models/robotic_arm_assembly.stl",
        "Task_2_Robotic_Arm_Simulation/cad_models/robotic_arm_assembly.obj"
    ]
    for cf in cad_files:
        assert os.path.exists(cf) and os.path.getsize(cf) > 1000, f"CAD file {cf} missing or empty!"
    print(f"Task 2: All 7 CAD solid files verified (non-zero size).")

    # Check kinematics verification script
    import Task_2_Robotic_Arm_Simulation.verify_kinematics as vk
    results_tbl, max_err_mm, steps, violations = vk.run_kinematics_verification()
    assert max_err_mm < 1.0, f"Max error {max_err_mm} >= 1.0 mm!"
    assert violations == 0, f"Limit violations {violations} > 0!"
    print(f"Task 2: Kinematics verified ({steps} steps, 0 limit violations, max error {max_err_mm:.4f} mm).")

    # 3. Check Task 3
    t3_pdf = "Task_3_Automation_System_Design/Task_3_Automation_System_Design_Report.pdf"
    assert os.path.exists(t3_pdf), f"Missing {t3_pdf}"
    r3 = pypdf.PdfReader(t3_pdf)
    t3_pages = len(r3.pages)
    t3_text = "".join(p.extract_text() or "" for p in r3.pages)
    print(f"Task 3: {t3_pages} pages (Target: 2-3 pages)")
    assert 2 <= t3_pages <= 3, f"Task 3 page count {t3_pages} not in [2, 3]!"
    assert not re.search(r'\$[a-zA-Z\\_^{}]', t3_text), "Raw LaTeX in Task 3!"
    assert '■' not in t3_text and '\u25a0' not in t3_text, "Broken glyph in Task 3!"
    assert 'TODO' not in t3_text, "TODO in Task 3!"

    # 4. Check Task 4
    t4_pdf = "Task_4_Mini_Project_Proposal/Task_4_AI_Robotics_Proposal.pdf"
    assert os.path.exists(t4_pdf), f"Missing {t4_pdf}"
    r4 = pypdf.PdfReader(t4_pdf)
    t4_pages = len(r4.pages)
    t4_text = "".join(p.extract_text() or "" for p in r4.pages)
    print(f"Task 4: {t4_pages} pages (Target: 5-6 pages)")
    assert 5 <= t4_pages <= 6, f"Task 4 page count {t4_pages} not in [5, 6]!"
    assert not re.search(r'\$[a-zA-Z\\_^{}]', t4_text), "Raw LaTeX in Task 4!"
    assert '■' not in t4_text and '\u25a0' not in t4_text, "Broken glyph in Task 4!"
    assert 'TODO' not in t4_text, "TODO in Task 4!"

    # 5. Check No Absolute Windows file:/// paths in markdown/html files
    md_html_files = [
        "SUBMISSION_GUIDE_AND_SUMMARY.md",
        "FIX_REPORT.md",
        "index.html",
        "Task_1_Research_Report/Research_Report_Industry_4_0.md",
        "Task_2_Robotic_Arm_Simulation/README_Task2.md",
        "Task_2_Robotic_Arm_Simulation/interactive_3d_arm.html",
        "Task_3_Automation_System_Design/README_Task3.md",
        "Task_4_Mini_Project_Proposal/README_Task4.md"
    ]
    for mhf in md_html_files:
        with open(mhf, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "file:///c:" not in content.lower() and "file:///C:" not in content, f"Absolute path found in {mhf}!"
        assert "users/abdullah" not in content.lower(), f"Personal path found in {mhf}!"
    print(f"Global: 0 absolute file:/// URIs across all documentation files.")

    print("\n" + "=" * 80)
    print("ALL MANDATORY QA CHECKS PASSED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == '__main__':
    run_qa()
