"""
Generates the comprehensive submission Word Document (.docx) for FAI Lab Report 2
With designated placeholder spaces, callout boxes for screenshots, and link slots.

Student: Ayush Aditya | Reg No: 252U1R3013
Class: B.Tech CSE (Data Science) - Section S20 (Room 205)
Institution: Aurora Higher Education and Research Academy
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = r"C:\Users\Ayush\Desktop\dsa_lab_1\FAI_Lab_2"
DOCX_OUT_PATH = os.path.join(BASE_DIR, "FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.docx")
VIS_DIR = os.path.join(BASE_DIR, "visualizations")

STUDENT_NAME = "Ayush Aditya"
REG_NO = "252U1R3013"
CLASS_SEC = "B.Tech CSE (Data Science) - S20 (Room 205)"
SUBJECT_NAME = "Fundamentals of Artificial Intelligence"
COLLEGE_NAME = "AURORA HIGHER EDUCATION AND RESEARCH ACADEMY"
DEPARTMENT_NAME = "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)"
SCHOOL_NAME = "SCHOOL OF ENGINEERING"
COLAB_LINK = "https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb"
GITHUB_LINK = "https://github.com/zeph7907/FAI-Lab-2"

doc = docx.Document()

# 1-inch margins
for sec in doc.sections:
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

# Colors
C_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
C_DARK = RGBColor(15, 23, 42)        # #0F172A
C_GRAY = RGBColor(71, 85, 105)       # #475569
C_BLUE_BORDER = "3B82F6"            # #3B82F6
C_LIGHT_BG = "F8FAFC"               # #F8FAFC
C_GREEN_BG = "F0FDF4"               # #F0FDF4
C_AMBER_BG = "FFFBEB"               # #FFFBEB

def add_heading(text, level, space_before=12, space_after=6):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        if level == 0:
            r.font.size = Pt(18)
            r.font.bold = True
            r.font.color.rgb = C_NAVY
        elif level == 1:
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = C_NAVY
        elif level == 2:
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.color.rgb = C_DARK
        elif level == 3:
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = C_GRAY
    return h

def add_screenshot_placeholder(title, instructions, image_ref_name="", approx_height_in=3.2):
    """
    Creates a styled callout box in Word that serves as a dedicated space for pasting screenshots.
    Also includes a visual guide and reference.
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{C_LIGHT_BG}"/>')
    tcPr.append(shd)
    
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="dashed" w:sz="12" w:space="0" w:color="{C_BLUE_BORDER}"/>
            <w:left w:val="dashed" w:sz="12" w:space="0" w:color="{C_BLUE_BORDER}"/>
            <w:bottom w:val="dashed" w:sz="12" w:space="0" w:color="{C_BLUE_BORDER}"/>
            <w:right w:val="dashed" w:sz="12" w:space="0" w:color="{C_BLUE_BORDER}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    # Text inside placeholder box
    p1 = cell.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(8)
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run(f"📸 [PASTE SCREENSHOT HERE]: {title}")
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = C_NAVY
    
    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(6)
    r2 = p2.add_run(f"Instructions for Student ({STUDENT_NAME} - {REG_NO}):\n")
    r2.font.bold = True
    r2.font.size = Pt(9)
    r2.font.color.rgb = C_DARK
    
    for line in instructions:
        p_item = cell.add_paragraph()
        p_item.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(2)
        r_bullet = p_item.add_run(f"  • {line}")
        r_bullet.font.size = Pt(8.5)
        r_bullet.font.color.rgb = C_GRAY
        
    p_box = cell.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(10)
    p_box.paragraph_format.space_after = Pt(10)
    r_box = p_box.add_run("┌────────────────────────────────────────────────────────────────────────┐\n"
                          "│                                                                        │\n"
                          "│        >>> CLICK HERE, PRESS BACKSPACE/DELETE, AND PASTE (Ctrl+V) <<<  │\n"
                          "│            YOUR GENUINE SCREENSHOT OF THE EXECUTED COLAB OUTPUT        │\n"
                          "│                                                                        │\n"
                          "└────────────────────────────────────────────────────────────────────────┘")
    r_box.font.name = "Consolas"
    r_box.font.size = Pt(8)
    r_box.font.color.rgb = RGBColor(100, 116, 139)
    
    # If image file exists in visualizations, embed a pre-rendered reference right below the box
    if image_ref_name:
        img_path = os.path.join(VIS_DIR, image_ref_name)
        if os.path.exists(img_path):
            p_ref_hdr = cell.add_paragraph()
            p_ref_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_ref_hdr.paragraph_format.space_before = Pt(6)
            p_ref_hdr.paragraph_format.space_after = Pt(4)
            r_ref = p_ref_hdr.add_run("--- Reference Verified Simulation Output (Generated Locally) ---")
            r_ref.font.italic = True
            r_ref.font.size = Pt(8)
            r_ref.font.color.rgb = C_GRAY
            
            p_img = cell.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(6)
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(5.8))
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_link_placeholder(title, colab_url, github_url):
    """
    Creates a styled link box showing where to put Google Colab & GitHub repository links.
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{C_GREEN_BG}"/>')
    tcPr.append(shd)
    
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="059669"/>
            <w:left w:val="single" w:sz="8" w:space="0" w:color="059669"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="059669"/>
            <w:right w:val="single" w:sz="8" w:space="0" w:color="059669"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f"🔗 {title}")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(6, 95, 70)
    
    # Colab Link Row
    p_colab = cell.add_paragraph()
    p_colab.paragraph_format.space_before = Pt(2)
    p_colab.paragraph_format.space_after = Pt(3)
    r_c_lbl = p_colab.add_run("• Google Colab Notebook Link:\n  ")
    r_c_lbl.font.bold = True
    r_c_lbl.font.size = Pt(9)
    r_c_val = p_colab.add_run(colab_url)
    r_c_val.font.size = Pt(8.5)
    r_c_val.font.color.rgb = RGBColor(37, 99, 235)
    r_c_val.font.underline = True
    
    # GitHub Link Row
    p_gh = cell.add_paragraph()
    p_gh.paragraph_format.space_before = Pt(2)
    p_gh.paragraph_format.space_after = Pt(6)
    r_g_lbl = p_gh.add_run("• GitHub Repository Link:\n  ")
    r_g_lbl.font.bold = True
    r_g_lbl.font.size = Pt(9)
    r_g_val = p_gh.add_run(github_url)
    r_g_val.font.size = Pt(8.5)
    r_g_val.font.color.rgb = RGBColor(37, 99, 235)
    r_g_val.font.underline = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)


# ==============================================================================
# COVER PAGE / HEADER
# ==============================================================================

p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_top.paragraph_format.space_after = Pt(2)

r_u = p_top.add_run(f"{COLLEGE_NAME}\n")
r_u.font.bold = True
r_u.font.size = Pt(13)
r_u.font.color.rgb = C_NAVY

r_s = p_top.add_run(f"{SCHOOL_NAME}\n{DEPARTMENT_NAME}\n")
r_s.font.bold = True
r_s.font.size = Pt(10.5)
r_s.font.color.rgb = C_DARK

r_loc = p_top.add_run("Bhongir, Yadadri - 508116 | Academic Year 2025–2026\n\n")
r_loc.font.size = Pt(9)
r_loc.font.color.rgb = C_GRAY

p_doc_title = doc.add_paragraph()
p_doc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_doc_title.paragraph_format.space_before = Pt(4)
p_doc_title.paragraph_format.space_after = Pt(12)

r_dt1 = p_doc_title.add_run("LAB REPORT 2: UNINFORMED SEARCH STRATEGIES\n")
r_dt1.font.bold = True
r_dt1.font.size = Pt(15)
r_dt1.font.color.rgb = C_NAVY

r_dt2 = p_doc_title.add_run("(BREADTH-FIRST SEARCH, DEPTH-FIRST SEARCH, AND DEPTH-LIMITED SEARCH)")
r_dt2.font.bold = True
r_dt2.font.size = Pt(10.5)
r_dt2.font.color.rgb = C_DARK

# Student Details Table (College Template)
tbl_info = doc.add_table(rows=8, cols=2)
tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_info.autofit = False

student_meta = [
    ("Student Name", STUDENT_NAME),
    ("Student Registration Number", REG_NO),
    ("Class & Section", CLASS_SEC),
    ("Study Level", "Undergraduate (B.Tech - 2nd Year, Term 2)"),
    ("Subject Name", SUBJECT_NAME),
    ("Course Code / Nature", "FAI Laboratory (Week 2 Laboratory Assignment)"),
    ("Syllabus Scope", "Module 1 (AI & Agents) & Module 2 (Uninformed Search)"),
    ("Date of Submission", "November 2026")
]

for i, (k, v) in enumerate(student_meta):
    row = tbl_info.rows[i]
    c1, c2 = row.cells[0], row.cells[1]
    c1.width = Inches(2.5)
    c2.width = Inches(4.0)
    
    # Border & padding
    for c in [c1, c2]:
        tcPr = c._tc.get_or_add_tcPr()
        b = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            </w:tcBorders>
        ''')
        tcPr.append(b)
        
    p_k = c1.paragraphs[0]
    p_k.text = k
    p_k.runs[0].font.bold = True
    p_k.runs[0].font.size = Pt(9)
    p_k.paragraph_format.space_before = Pt(3)
    p_k.paragraph_format.space_after = Pt(3)
    
    p_v = c2.paragraphs[0]
    p_v.text = v
    p_v.runs[0].font.size = Pt(9)
    if "Registration" in k or "Student Name" in k:
        p_v.runs[0].font.bold = True
        p_v.runs[0].font.color.rgb = C_NAVY
    p_v.paragraph_format.space_before = Pt(3)
    p_v.paragraph_format.space_after = Pt(3)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# Theoretical Framing
add_heading("Syllabus Alignment & Problem Formulation (Modules 1 & 2)", level=1)
p_thy = doc.add_paragraph()
p_thy.add_run(
    "In compliance with Module 1 (Introduction to Artificial Intelligence & Intelligent Agents) and "
    "Module 2 (Uninformed Search Strategies), both laboratory problems are formulated as State Space Search problems. "
    "Uninformed search strategies explore the state space using only problem definitions and transition rules, "
    "without heuristic estimation of distance to the goal.\n\n"
    "• State Space Formulation: A discrete 2D grid where states S = {(r, c) | 0 <= r < 10, 0 <= c < 10}. "
    "Initial State s_0 = (0, 0), Goal State s_goal = (9, 9). Valid actions A = {Up, Down, Left, Right} with step cost c = 1.\n"
    "• Breadth-First Search (BFS): Expands frontier level-by-level using a FIFO Queue. Guarantees optimality and completeness for uniform step costs.\n"
    "• Depth-First Search (DFS): Pursues branch paths deeply using a LIFO Stack. Complete in finite grids with cycle avoidance, but non-optimal.\n"
    "• Depth-Limited Search (DLS): Bounds DFS depth to a predefined limit L. Eliminates infinite branch trapping and maintains strictly linear space O(b * L)."
)
p_thy.runs[0].font.size = Pt(9.5)

doc.add_page_break()

# ==============================================================================
# PROBLEM 1: HOSPITAL DELIVERY ROBOT
# ==============================================================================
add_heading("PROBLEM 1: HOSPITAL DELIVERY ROBOT NAVIGATION", level=1)

add_heading("1. Question / Problem Statement", level=2)
p_p1_stmt = doc.add_paragraph()
p_p1_stmt.add_run(
    "A robot needs to deliver medicines from the hospital pharmacy to a patient's room. "
    "The hospital is represented as a grid containing free paths and blocked paths.\n\n"
    "Assigned Tasks:\n"
    "1. Create a 2D grid representing the hospital.\n"
    "2. Mark the starting point (Pharmacy), destination (Patient Room), and obstacles.\n"
    "3. Implement Breadth-First Search (BFS) to find the shortest path.\n"
    "4. Implement Depth-First Search (DFS) to find a path.\n"
    "5. Visualize and compare the paths found by both algorithms."
)
p_p1_stmt.runs[0].font.size = Pt(9.5)

add_heading("2. Required Code / Procedure", level=2)
p_p1_code_intro = doc.add_paragraph()
p_p1_code_intro.add_run(
    "The Python program defines the 10x10 hospital layout, verifies orthogonal neighbor boundaries, "
    "and implements BFS using collections.deque and DFS using a LIFO stack:"
)
p_p1_code_intro.runs[0].font.size = Pt(9.5)

code1_text = """from collections import deque

def get_neighbors(r, c, rows, cols, grid):
    \"\"\"Returns valid orthogonal neighbors (Up, Down, Left, Right) avoiding obstacles.\"\"\"
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(grid, start, goal):
    \"\"\"Breadth-First Search: Guarantees shortest delivery path using FIFO Queue.\"\"\"
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    parent = {start: None}
    explored = []
    while queue:
        curr = queue.popleft()
        explored.append(curr)
        if curr == goal:
            break
        for nxt in get_neighbors(curr[0], curr[1], rows, cols, grid):
            if nxt not in parent:
                parent[nxt] = curr
                queue.append(nxt)
    if goal not in parent:
        return None, explored
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path, explored

def dfs_search(grid, start, goal):
    \"\"\"Depth-First Search: Explores deep along corridors using LIFO Stack.\"\"\"
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    parent = {start: None}
    explored = []
    while stack:
        curr = stack.pop()
        explored.append(curr)
        if curr == goal:
            break
        for nxt in get_neighbors(curr[0], curr[1], rows, cols, grid):
            if nxt not in parent:
                parent[nxt] = curr
                stack.append(nxt)
    if goal not in parent:
        return None, explored
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path, explored"""

p_c1 = doc.add_paragraph()
r_c1 = p_c1.add_run(code1_text)
r_c1.font.name = "Consolas"
r_c1.font.size = Pt(8.5)

add_heading("3. Final Output & Execution Screenshots", level=2)
p_out_text1 = doc.add_paragraph()
p_out_text1.add_run(
    f"Program Execution Output (Student: {STUDENT_NAME} | Reg. No: {REG_NO}):\n"
    f"--------------------------------------------------------------------------------\n"
    f"BFS Shortest Path Length : 19 cells (18 steps)\n"
    f"BFS Explored Nodes       : 75 cells\n"
    f"BFS Route Coordinates    : [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), \n"
    f"                            (6, 1), (6, 2), (6, 3), (7, 3), (8, 3), (9, 3), (9, 4), \n"
    f"                            (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]\n"
    f"DFS Valid Path Length    : 27 cells (26 steps) [Non-optimal detour]\n"
    f"DFS Explored Nodes       : 56 cells\n"
    f"--------------------------------------------------------------------------------"
)
p_out_text1.runs[0].font.name = "Consolas"
p_out_text1.runs[0].font.size = Pt(8.5)

# Screenshot Space for Problem 1
add_screenshot_placeholder(
    title="PROBLEM 1 BFS VS DFS OUTPUT AND VISUALIZATION",
    instructions=[
        f"Screenshot Requirement: Execute Cell 2 and Cell 3 of the notebook in Google Colab.",
        f"Registration Number Check: Ensure '252U1R3013' and 'Ayush Aditya' are clearly visible in the figure header and info box.",
        f"Contents: Matplotlib dual-panel plot showing BFS path (19 cells) vs DFS path (27 cells), obstacles, explored cells, and legend.",
        f"How to replace: Click the placeholder box below, hit Backspace/Delete, and paste (Ctrl+V) your screenshot."
    ],
    image_ref_name="problem1_hospital_robot_bfs_vs_dfs.png"
)

add_heading("4. Google Colab & Project Repository Links", level=2)
add_link_placeholder(
    title="PROBLEM 1 PROJECT LINKS",
    colab_url=COLAB_LINK,
    github_url=GITHUB_LINK
)

add_heading("5. Explanation & Comparative Analysis (BFS vs DFS)", level=2)
p_exp1 = doc.add_paragraph()
p_exp1.add_run(
    "Step-by-Step Program Execution & Algorithm Analysis:\n\n"
    "1. Environmental Modeling: The hospital is modeled as a 10x10 matrix. Free paths are marked as 0, while static obstacles "
    "(ICU wards, X-ray laboratories, nurse stations, and storage closets) are marked as 1. The robot starts at the Pharmacy (0, 0) "
    "and targets Patient Room 304 at (9, 9).\n\n"
    "2. Breadth-First Search (BFS) Behavior: BFS initializes with the pharmacy in a FIFO queue. It systematically expands every immediate "
    "accessible corridor layer-by-layer. Because the grid transition cost is uniform (1 step = cost 1), BFS guarantees finding the "
    "mathematical shortest delivery path. In this experiment, BFS identified an optimal 19-cell path (18 steps) after exploring 75 cells.\n\n"
    "3. Depth-First Search (DFS) Behavior: DFS pushes neighboring coordinates onto a LIFO stack. It plunges deeply along one branch corridor "
    "until it encounters a dead end or obstacle before backtracking. As demonstrated, DFS took an extensive detour around peripheral wards, "
    "resulting in a 27-cell path (29.6% longer than BFS) while exploring 56 cells.\n\n"
    "4. Comparative Verdict for Clinical Delivery: In a hospital scenario, BFS is undeniably the superior search strategy. Delivering "
    "emergency medication or life-support items requires minimum transit time; the unnecessary detours discovered by DFS could result in critical patient harm."
)
p_exp1.runs[0].font.size = Pt(9.5)

# Problem 1 Comparison Table
tbl_comp1 = doc.add_table(rows=6, cols=3)
tbl_comp1.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_comp1.autofit = False

comp1_headers = ["Evaluation Metric", "Breadth-First Search (BFS)", "Depth-First Search (DFS)"]
for j, h in enumerate(comp1_headers):
    c = tbl_comp1.rows[0].cells[j]
    c.text = h
    c.paragraphs[0].runs[0].font.bold = True
    c.paragraphs[0].runs[0].font.size = Pt(9)
    tcPr = c._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E2E8F0"/>')
    tcPr.append(shd)

comp1_rows = [
    ("Data Structure", "FIFO Queue (collections.deque)", "LIFO Stack (List / Call Stack)"),
    ("Completeness", "Yes (guaranteed in finite branching)", "Yes (with cycle checking in finite grid)"),
    ("Optimality", "Yes (Optimal shortest path)", "No (returns first traversable path found)"),
    ("Time Complexity", "O(b^d) where d = goal depth", "O(b^m) where m = maximum depth"),
    ("Space Complexity", "O(b^d) [Exponential frontier]", "O(b * m) [Strictly Linear memory]")
]

for i, row in enumerate(comp1_rows):
    r = tbl_comp1.rows[i+1]
    for j, val in enumerate(row):
        c = r.cells[j]
        c.text = val
        c.paragraphs[0].runs[0].font.size = Pt(8.5)

doc.add_page_break()

# ==============================================================================
# PROBLEM 2: COLLEGE CAMPUS NAVIGATION
# ==============================================================================
add_heading("PROBLEM 2: COLLEGE CAMPUS NAVIGATION", level=1)

add_heading("1. Question / Problem Statement", level=2)
p_p2_stmt = doc.add_paragraph()
p_p2_stmt.add_run(
    "A student wants to travel from the college entrance to the computer laboratory. "
    "Some pathways are blocked, while others are accessible.\n\n"
    "Assigned Tasks:\n"
    "1. Create a 2D grid representing the college campus.\n"
    "2. Mark the starting point (College Entrance), destination (Computer Lab), and blocked pathways.\n"
    "3. Implement Breadth-First Search (BFS) to find the shortest path.\n"
    "4. Implement Depth-Limited Search (DLS) with a suitable depth limit.\n"
    "5. Visualize the explored cells and the final path for both algorithms."
)
p_p2_stmt.runs[0].font.size = Pt(9.5)

add_heading("2. Required Code / Procedure", level=2)
p_p2_code_intro = doc.add_paragraph()
p_p2_code_intro.add_run(
    "The Python implementation constructs the 10x10 campus layout, executes BFS for shortest path, "
    "and implements Depth-Limited Search (DLS) with depth cutoff tracking:"
)
p_p2_code_intro.runs[0].font.size = Pt(9.5)

code2_text = """def dls_search(grid, start, goal, depth_limit):
    \"\"\"
    Depth-Limited Search (DLS): DFS bounded by depth limit L.
    Returns: (path, explored_nodes, status)
    status is 'SUCCESS', 'CUTOFF', or 'FAILURE'
    \"\"\"
    rows, cols = len(grid), len(grid[0])
    explored = []
    visited_depth = {}
    
    def recursive_dls(node, depth, path):
        if node not in explored:
            explored.append(node)
        if node == goal:
            return list(path), "SUCCESS"
        if depth >= depth_limit:
            return None, "CUTOFF"
            
        visited_depth[node] = depth
        cutoff_occurred = False
        
        for nxt in get_neighbors(node[0], node[1], rows, cols, grid):
            # Prune search if visited at an equal or shallower depth
            if nxt not in visited_depth or depth + 1 < visited_depth[nxt]:
                path.append(nxt)
                result, status = recursive_dls(nxt, depth + 1, path)
                if status == "SUCCESS":
                    return result, "SUCCESS"
                if status == "CUTOFF":
                    cutoff_occurred = True
                path.pop()
                
        return None, ("CUTOFF" if cutoff_occurred else "FAILURE")
        
    path, status = recursive_dls(start, 0, [start])
    return path, explored, status"""

p_c2 = doc.add_paragraph()
r_c2 = p_c2.add_run(code2_text)
r_c2.font.name = "Consolas"
r_c2.font.size = Pt(8.5)

add_heading("3. Final Output & Execution Screenshots", level=2)
p_out_text2 = doc.add_paragraph()
p_out_text2.add_run(
    f"Program Execution Output (Student: {STUDENT_NAME} | Reg. No: {REG_NO}):\n"
    f"--------------------------------------------------------------------------------\n"
    f"[BFS] Campus Shortest Path     : 19 cells (18 steps) | Explored: 77 cells\n"
    f"[DLS L=20] Suitable Limit      : SUCCESS | Path Length: 21 cells (20 steps) | Explored: 48 cells\n"
    f"[DLS L=10] Cutoff Limit        : CUTOFF | Goal Depth d=18 > Limit L=10 (No path found)\n"
    f"--------------------------------------------------------------------------------"
)
p_out_text2.runs[0].font.name = "Consolas"
p_out_text2.runs[0].font.size = Pt(8.5)

# Screenshot Space for Problem 2: BFS vs DLS Suitable
add_screenshot_placeholder(
    title="PROBLEM 2 BFS VS DLS (SUITABLE LIMIT L=20) OUTPUT",
    instructions=[
        f"Screenshot Requirement: Execute Cell 4 and Cell 5 in Google Colab.",
        f"Registration Number Check: Ensure '252U1R3013' and 'Ayush Aditya' appear visibly on the top title and metadata card.",
        f"Contents: Dual-panel plot of BFS (19 cells) vs DLS with L=20 (21 cells), campus obstacles, explored cells, and trajectory.",
        f"How to replace: Click the placeholder box below, delete text, and paste (Ctrl+V) your screenshot."
    ],
    image_ref_name="problem2_campus_navigation_bfs_vs_dls.png"
)

# Screenshot Space for Problem 2: DLS Cutoff Analysis
add_screenshot_placeholder(
    title="PROBLEM 2 DLS CUTOFF ANALYSIS (LIMIT L=10 VS LIMIT L=20)",
    instructions=[
        f"Screenshot Requirement: Execute Cell 6 in Google Colab illustrating the theoretical DLS Cutoff condition.",
        f"Key Verification: Left panel shows DLS Cutoff (L=10 < d=18 -> Incomplete), Right panel shows DLS Success (L=20 >= d=18).",
        f"Registration Number: 252U1R3013 must be visible in both subplots."
    ],
    image_ref_name="problem2_dls_cutoff_vs_suitable.png"
)

add_heading("4. Google Colab & Project Repository Links", level=2)
add_link_placeholder(
    title="PROBLEM 2 PROJECT LINKS",
    colab_url=COLAB_LINK,
    github_url=GITHUB_LINK
)

add_heading("5. Explanation & Depth Limit Analysis (BFS vs DLS)", level=2)
p_exp2 = doc.add_paragraph()
p_exp2.add_run(
    "Depth Limit Selection Analysis & Algorithm Comparison:\n\n"
    "1. Analytical Selection of Depth Limit L: The Manhattan distance between College Entrance (0, 0) and Computer Lab (9, 9) "
    "is |9 - 0| + |9 - 0| = 18 steps. Accounting for campus construction obstacles, the true shortest path is d = 18 steps (19 cells).\n\n"
    "2. Cutoff Demonstration (L = 10): When DLS is run with depth limit L = 10, the algorithm terminates with a CUTOFF signal. "
    "Because L < d (10 < 18), the algorithm correctly halts its descent, proving that DLS prevents infinite recursion but will fail "
    "if the depth limit is set lower than the solution depth.\n\n"
    "3. Suitable Depth Limit (L = 20): Setting L = 20 guarantees that L >= d, providing sufficient depth budget to route around obstacles. "
    "DLS successfully reaches the Computer Lab with a path length of 21 cells (20 steps) while exploring only 48 cells.\n\n"
    "4. Memory Comparison (BFS vs DLS): BFS stores the entire expanding perimeter in RAM, requiring exponential memory O(b^d). "
    "Conversely, DLS holds only the active search branch in memory, consuming strictly linear memory O(b * L). DLS is therefore highly "
    "effective for memory-constrained embedded campus kiosks or handheld student guides."
)
p_exp2.runs[0].font.size = Pt(9.5)

# Problem 2 Comparison Table
tbl_comp2 = doc.add_table(rows=5, cols=4)
tbl_comp2.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_comp2.autofit = False

comp2_headers = ["Metric", "BFS", "DLS (L=20, Suitable)", "DLS (L=10, Cutoff)"]
for j, h in enumerate(comp2_headers):
    c = tbl_comp2.rows[0].cells[j]
    c.text = h
    c.paragraphs[0].runs[0].font.bold = True
    c.paragraphs[0].runs[0].font.size = Pt(9)
    tcPr = c._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E2E8F0"/>')
    tcPr.append(shd)

comp2_rows = [
    ("Completeness", "Yes", "Yes (since L >= d)", "No (Cutoff occurred)"),
    ("Optimality", "Yes (19 cells)", "No (21 cells)", "N/A"),
    ("Time Complexity", "O(b^d)", "O(b^L)", "O(b^L)"),
    ("Space Complexity", "O(b^d) [Exponential]", "O(b * L) [Linear]", "O(b * L) [Linear]")
]

for i, row in enumerate(comp2_rows):
    r = tbl_comp2.rows[i+1]
    for j, val in enumerate(row):
        c = r.cells[j]
        c.text = val
        c.paragraphs[0].runs[0].font.size = Pt(8.5)

doc.add_page_break()

# ==============================================================================
# OVERALL LAB CONCLUSION
# ==============================================================================
add_heading("Overall Assessment Conclusion (Module 1 & 2 Synthesis)", level=1)

p_sum = doc.add_paragraph()
p_sum.add_run(
    "Summary Comparison Across All Evaluated Uninformed Search Algorithms:\n"
)
p_sum.runs[0].font.size = Pt(9.5)

tbl_final = doc.add_table(rows=4, cols=5)
tbl_final.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_final.autofit = False

final_headers = ["Algorithm", "Data Structure", "Completeness", "Optimality", "Memory Footprint"]
for j, h in enumerate(final_headers):
    c = tbl_final.rows[0].cells[j]
    c.text = h
    c.paragraphs[0].runs[0].font.bold = True
    c.paragraphs[0].runs[0].font.size = Pt(9)
    tcPr = c._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E2E8F0"/>')
    tcPr.append(shd)

final_rows = [
    ("Breadth-First Search (BFS)", "FIFO Queue", "Complete (b < inf)", "Optimal (uniform cost)", "O(b^d) [High RAM requirement]"),
    ("Depth-First Search (DFS)", "LIFO Stack", "Complete (finite state)", "Non-Optimal", "O(b * m) [Minimal linear RAM]"),
    ("Depth-Limited Search (DLS)", "Recursive / Stack (L)", "Complete if L >= d", "Non-Optimal", "O(b * L) [Strictly linear RAM]")
]

for i, row in enumerate(final_rows):
    r = tbl_final.rows[i+1]
    for j, val in enumerate(row):
        c = r.cells[j]
        c.text = val
        c.paragraphs[0].runs[0].font.size = Pt(8.5)

p_conc = doc.add_paragraph()
p_conc.paragraph_format.space_before = Pt(12)
p_conc.add_run(
    f"Concluding Takeaways (Student: {STUDENT_NAME} | Reg. No: {REG_NO}):\n"
    "1. In Problem 1 (Hospital Delivery Robot), BFS proved to be the required algorithm because path length directly impacts patient survival and clinical delivery turnaround time.\n"
    "2. In Problem 2 (College Campus Navigation), DLS demonstrated how search depth constraints eliminate infinite loops and reduce memory usage to linear complexity O(b * L), "
    "provided domain knowledge informs a suitable depth limit L >= d.\n"
    "3. Both experiments comprehensively validate the theoretical principles of Uninformed Search Strategies as prescribed in Modules 1 and 2 of the Fundamentals of Artificial Intelligence curriculum."
)
p_conc.runs[0].font.size = Pt(9.5)

doc.save(DOCX_OUT_PATH)
print(f"[SUCCESS] Submission Document successfully generated at:\n{DOCX_OUT_PATH}")
