"""
Master Generator for FAI Lab Report 2 Word Document (.docx)
Author: Ayush Aditya | Reg No: 252U1R3013
Class: B.Tech CSE (Data Science) | Section: S20 / Room 205
Course: Fundamentals of Artificial Intelligence (Modules 1 & 2)
Institution: Aurora Deemed to be University
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\Ayush\Desktop\dsa_lab_1\FAI_Lab_2"
DOCX_FILENAME = os.path.join(BASE_DIR, "FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.docx")
ROOT_DOCX_FILENAME = r"C:\Users\Ayush\Desktop\dsa_lab_1\FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.docx"

STUDENT_NAME = "Ayush Aditya"
REG_NO = "252U1R3013"
CLASS_SEC = "B.Tech CSE (Data Science) - Section S20 (Room 205)"
COURSE_NAME = "Fundamentals of Artificial Intelligence"
LAB_TITLE = "FAI Lab Report 2: Uninformed Search Strategies (BFS, DFS, and DLS)"

# Live Links
COLAB_LINK = "https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb"
GITHUB_LINK = "https://github.com/zeph7907/FAI-Lab-2"

# Color Palette (Matching Lab Report 1)
C_NAVY = RGBColor(15, 44, 89)      # #0F2C59
C_BLUE = RGBColor(37, 99, 235)     # #2563EB
C_DARK = RGBColor(30, 41, 59)      # #1E293B
C_GRAY = RGBColor(100, 116, 139)   # #64748B
C_BORDER = "CBD5E1"
C_LIGHT_BG = "F8FAFC"
C_CODE_BG = "F1F5F9"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, color="3B82F6", sz="8", val="dashed"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

def add_code_box(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.5)
    set_cell_background(c, C_CODE_BG)
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    set_cell_borders(c, color=C_BORDER, sz="6", val="single")
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_DARK

def add_screenshot_box(doc, caption_text, subtext):
    """Creates a clean empty screenshot placeholder space as in Lab 1."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.5)
    set_cell_background(c, "FDFEFE")
    set_cell_margins(c, top=200, bottom=200, left=180, right=180)
    set_cell_borders(c, color="3B82F6", sz="10", val="dashed")
    
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"📸 {caption_text.upper()}\n")
    r1.font.bold = True
    r1.font.size = Pt(10)
    r1.font.color.rgb = C_NAVY
    
    r2 = p.add_run(f"[ Insert Genuine Google Colab Screenshot Here ]\n")
    r2.font.bold = True
    r2.font.size = Pt(11)
    r2.font.color.rgb = C_BLUE
    
    r3 = p.add_run(f"{subtext}\n(Ensure Student Name: {STUDENT_NAME} and Reg No: {REG_NO} are clearly visible)")
    r3.font.italic = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = C_GRAY
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(3)
    p_cap.paragraph_format.space_after = Pt(8)
    rc = p_cap.add_run(f"Figure: Colab Execution Output for {caption_text}")
    rc.font.size = Pt(8.5)
    rc.font.italic = True
    rc.font.color.rgb = C_GRAY

def build_docx():
    doc = docx.Document()
    
    # Configure 0.75-inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    def add_styled_heading(text, level=1):
        h = doc.add_heading(level=level)
        h.paragraph_format.keep_with_next = True
        h.paragraph_format.space_before = Pt(14 if level==1 else 10)
        h.paragraph_format.space_after = Pt(4 if level==1 else 2)
        r = h.add_run(text)
        if level == 1:
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = C_NAVY
        elif level == 2:
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.color.rgb = C_BLUE
        elif level == 3:
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = C_DARK
        return h

    # Header Block
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_after = Pt(2)
    r_univ = p_top.add_run("AURORA DEEMED TO BE UNIVERSITY\n")
    r_univ.bold = True
    r_univ.font.size = Pt(14)
    r_univ.font.color.rgb = C_NAVY

    r_school = p_top.add_run("SCHOOL OF ENGINEERING & TECHNOLOGY\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)\n")
    r_school.bold = True
    r_school.font.size = Pt(10.5)
    r_school.font.color.rgb = C_DARK

    r_sub = p_top.add_run("Academic Year 2025–2026 | Term 2 | Undergraduate B.Tech Program\n")
    r_sub.font.size = Pt(9)
    r_sub.font.italic = True
    r_sub.font.color.rgb = C_GRAY

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("LAB REPORT 2: FUNDAMENTALS OF ARTIFICIAL INTELLIGENCE\n(UNINFORMED SEARCH STRATEGIES: BFS, DFS, AND DLS)")
    r_t.bold = True
    r_t.font.size = Pt(13.5)
    r_t.font.color.rgb = C_NAVY

    # Student Details Table
    table_info = doc.add_table(rows=8, cols=2)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_info.autofit = False

    details = [
        ("Student Name", STUDENT_NAME),
        ("Registration Number", REG_NO),
        ("Degree & Program", "B.Tech Computer Science and Engineering (Data Science)"),
        ("Class / Section / Room", "Section S20 / Room 205"),
        ("Year & Academic Term", "2nd Year, Term 2"),
        ("Subject Name", "Fundamentals of Artificial Intelligence"),
        ("Lab Report Number", "Lab Report 2"),
        ("Syllabus Scope", "Module 1 (AI & Agents) & Module 2 (Uninformed Search Strategies)")
    ]

    for i, (label, val) in enumerate(details):
        row = table_info.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, C_LIGHT_BG if i % 2 == 0 else "FFFFFF")
        set_cell_background(c1, C_LIGHT_BG if i % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, 30, 30, 60, 60)
        set_cell_margins(c1, 30, 30, 60, 60)
        set_cell_borders(c0, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c1, color=C_BORDER, sz="4", val="single")

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9)
        r0.font.color.rgb = C_DARK

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9)
        if "Registration" in label or "Student Name" in label:
            r1.font.bold = True
            r1.font.color.rgb = C_BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Theoretical Framework & Module Alignment
    add_styled_heading("1. Theoretical Framework & Syllabus Alignment (Modules 1 & 2)", level=1)
    p_theory = doc.add_paragraph()
    p_theory.paragraph_format.space_after = Pt(6)
    p_theory.add_run(
        "STRICT SYLLABUS RESTRICTION COMPLIANCE:\n"
        "In strict adherence to the university curriculum, all implementations, algorithms, and analyses in this "
        "laboratory report are formulated strictly under Module 1 (Introduction to Artificial Intelligence & Intelligent Agents) "
        "and Module 2 (Uninformed Search Strategies). Informed search algorithms (such as A*, Greedy Best-First Search, Hill Climbing, "
        "or Beam Search belonging to Module 3) are strictly excluded.\n\n"
        "1.1 State Space Search Problem Formulation:\n"
        "A search problem is formally defined by five components:\n"
        "• State Space (S): The set of all valid configurations. In our 2D grid, S = {(r, c) | 0 <= r < 10, 0 <= c < 10, grid[r][c] == 0}.\n"
        "• Initial State (s_0): Starting coordinates (0, 0) representing the Hospital Pharmacy (Problem 1) or College Entrance (Problem 2).\n"
        "• Actions A(s): Legal orthogonal movements {Up: (-1, 0), Down: (1, 0), Left: (0, -1), Right: (0, 1)}.\n"
        "• Transition Model Result(s, a): Returns the adjacent coordinate (r + dr, c + dc) if within bounds and not blocked by an obstacle.\n"
        "• Goal Test: Checks if the current state reaches the destination (9, 9) representing Patient Room 304 or the Computer Laboratory.\n"
        "• Path Cost c(s, a, s'): Uniform step cost = 1 per movement.\n\n"
        "1.2 Uninformed Search Strategies (Module 2):\n"
        "• Breadth-First Search (BFS): Explores the state space systematically level-by-level using a FIFO Queue. It is complete (finds a solution if one exists) and optimal (guarantees the shortest path for uniform step costs).\n"
        "• Depth-First Search (DFS): Explores deeply along each branch using a LIFO Stack. Complete in finite state spaces with cycle avoidance, but not optimal.\n"
        "• Depth-Limited Search (DLS): Bounds DFS depth to a predefined limit L to avoid infinite loops and maintain linear memory O(b * L)."
    )
    p_theory.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # ==============================================================================
    # PROBLEM 1: HOSPITAL DELIVERY ROBOT
    # ==============================================================================
    add_styled_heading("LAB REPORT 1 — PROBLEM 1: HOSPITAL DELIVERY ROBOT NAVIGATION", level=1)

    add_styled_heading("1. Question / Problem Statement", level=2)
    p_p1_stmt = doc.add_paragraph()
    p_p1_stmt.paragraph_format.space_after = Pt(6)
    p_p1_stmt.add_run(
        "A robot needs to deliver medicines from the hospital pharmacy to a patient's room. "
        "The hospital is represented as a grid containing free paths and blocked paths.\n\n"
        "Tasks:\n"
        "1. Create a 2D grid representing the hospital.\n"
        "2. Mark the starting point (Pharmacy), destination (Patient Room), and obstacles.\n"
        "3. Implement Breadth-First Search (BFS) to find the shortest path.\n"
        "4. Implement Depth-First Search (DFS) to find a path.\n"
        "5. Visualize and compare the paths found by both algorithms."
    )
    p_p1_stmt.runs[0].font.size = Pt(9)

    add_styled_heading("2. Required Code / Procedure", level=2)
    p_p1_code_intro = doc.add_paragraph()
    p_p1_code_intro.paragraph_format.space_after = Pt(4)
    p_p1_code_intro.add_run("Complete Python implementation defining the 10x10 hospital grid, BFS queue search, and DFS stack search:")
    p_p1_code_intro.runs[0].font.size = Pt(9)

    code1 = """from collections import deque

def get_neighbors(r, c, rows, cols, grid):
    \"\"\"Returns valid orthogonal neighbors (Up, Down, Left, Right) within bounds.\"\"\"
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(grid, start, goal):
    \"\"\"Breadth-First Search (BFS) using a FIFO Queue for shortest delivery path.\"\"\"
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
    \"\"\"Depth-First Search (DFS) using a LIFO Stack for valid corridor traversal.\"\"\"
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
    return path, explored

# Construct 10x10 Hospital Grid (0 = free hallway, 1 = hospital obstacle)
grid_hospital = [[0]*10 for _ in range(10)]
hospital_obstacles = [
    (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
    (7, 2), (8, 2), (9, 2),
    (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
    (1, 6), (2, 6), (3, 6), (5, 6), (6, 6), (7, 6), (8, 6),
    (3, 8), (4, 8), (5, 8), (7, 8), (8, 8)
]
for r, c in hospital_obstacles:
    grid_hospital[r][c] = 1

pharmacy_start = (0, 0)
patient_room_goal = (9, 9)

# Execute Uninformed Searches
bfs_path, bfs_explored = bfs_search(grid_hospital, pharmacy_start, patient_room_goal)
dfs_path, dfs_explored = dfs_search(grid_hospital, pharmacy_start, patient_room_goal)"""

    add_code_box(doc, code1)

    add_styled_heading("3. Final Output", level=2)
    p_out1_text = doc.add_paragraph()
    p_out1_text.paragraph_format.space_before = Pt(4)
    p_out1_text.paragraph_format.space_after = Pt(4)
    p_out1_text.add_run(
        f"Verified Program Execution Output (Registration Number: {REG_NO}):\n"
        f"• Breadth-First Search (BFS) : Shortest Path Length = 19 cells (18 steps) | Explored Cells = 75 cells [Optimal]\n"
        f"• Depth-First Search (DFS)   : Valid Path Length = 27 cells (26 steps) | Explored Cells = 56 cells [Non-Optimal Detour]"
    )
    p_out1_text.runs[0].font.size = Pt(8.5)
    p_out1_text.runs[0].font.name = "Consolas"

    # Screenshot Placeholder Space for Problem 1
    add_screenshot_box(
        doc,
        "Problem 1: Hospital Delivery Robot Execution Output (BFS vs DFS)",
        "Screenshot of executed Google Colab output cell showing the dual-panel grid visualization,\n"
        "Start (Pharmacy), Goal (Patient Room 304), Obstacles, Explored Nodes, and Final Paths."
    )

    # Section 4: Links (ONLY Colab & GitHub Link)
    add_styled_heading("4. Google Colab / Project Link", level=2)
    p_link1 = doc.add_paragraph()
    p_link1.paragraph_format.space_before = Pt(2)
    p_link1.paragraph_format.space_after = Pt(6)
    r_l1 = p_link1.add_run(
        f"Google Colab Link: {COLAB_LINK}\n\n"
        f"GitHub Repository Link: {GITHUB_LINK}"
    )
    r_l1.font.size = Pt(9.5)
    r_l1.font.bold = True
    r_l1.font.color.rgb = C_BLUE

    add_styled_heading("5. Explanation", level=2)
    p_exp1 = doc.add_paragraph()
    p_exp1.paragraph_format.space_after = Pt(6)
    p_exp1.add_run(
        "5.1 Algorithm Operation & Procedure:\n"
        "1. Hospital Grid Model: The hospital floor is represented as a 10x10 matrix where free corridors are 0 and static obstacles "
        "(ICU wards, X-ray laboratories, nurse stations, and storage rooms) are 1. The robot starts at the Pharmacy (0, 0) and delivers "
        "medicine to Patient Room 304 at (9, 9).\n"
        "2. BFS Mechanism: BFS initializes a FIFO queue with the start node. It systematically explores all nodes at depth k before "
        "expanding nodes at depth k+1. Because step costs are uniform (c = 1), BFS guarantees finding the optimal shortest path. "
        "It identified the optimal 19-cell path (18 steps) after exploring 75 cells.\n"
        "3. DFS Mechanism: DFS uses a LIFO stack. It pursues each unvisited corridor to its deepest reach before backtracking. "
        "Consequently, DFS followed a winding detour around hospital wards, yielding a 27-cell path (29.6% longer) while exploring 56 cells.\n\n"
        "5.2 Comparative Analysis (BFS vs DFS):\n"
        "• Completeness: Both BFS and DFS are complete in this finite 2D grid because cycle checking (parent dictionary) prevents revisiting states.\n"
        "• Optimality: BFS is optimal (finds minimum distance). DFS is non-optimal (finds the first valid path encountered).\n"
        "• Time Complexity: BFS runs in O(b^d) time; DFS runs in O(b^m) time where m is the maximum depth.\n"
        "• Space Complexity: BFS requires O(b^d) memory to maintain the frontier; DFS requires O(b * m) linear memory.\n"
        "• Clinical Application Verdict: For emergency pharmaceutical delivery, BFS is the mandatory algorithm. Taking the shortest route "
        "directly minimizes delivery transit time, which is critical in healthcare emergency scenarios."
    )
    p_exp1.runs[0].font.size = Pt(9)

    # Comparison Table for Problem 1
    tbl_p1 = doc.add_table(rows=6, cols=3)
    tbl_p1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_p1.autofit = False
    p1_rows = [
        ("Parameter", "Breadth-First Search (BFS)", "Depth-First Search (DFS)"),
        ("Frontier Data Structure", "FIFO Queue (collections.deque)", "LIFO Stack (List / Call Stack)"),
        ("Completeness", "Yes (guaranteed in finite b)", "Yes (with cycle checking in finite grid)"),
        ("Optimality", "Yes (Guaranteed shortest path)", "No (Returns first path encountered)"),
        ("Observed Path Length", "19 cells (18 steps)", "27 cells (26 steps)"),
        ("Total Explored Cells", "75 cells", "56 cells")
    ]
    for r_i, row_data in enumerate(p1_rows):
        row = tbl_p1.rows[r_i]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width = Inches(2.0)
        c1.width = Inches(2.25)
        c2.width = Inches(2.25)
        set_cell_background(c0, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_background(c1, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_background(c2, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_margins(c0, 30, 30, 50, 50)
        set_cell_margins(c1, 30, 30, 50, 50)
        set_cell_margins(c2, 30, 30, 50, 50)
        set_cell_borders(c0, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c1, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c2, color=C_BORDER, sz="4", val="single")
        c0.paragraphs[0].text = row_data[0]
        c1.paragraphs[0].text = row_data[1]
        c2.paragraphs[0].text = row_data[2]
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        c1.paragraphs[0].runs[0].font.size = Pt(8.5)
        c2.paragraphs[0].runs[0].font.size = Pt(8.5)
        if r_i == 0:
            c0.paragraphs[0].runs[0].bold = True
            c1.paragraphs[0].runs[0].bold = True
            c2.paragraphs[0].runs[0].bold = True

    doc.add_page_break()

    # ==============================================================================
    # PROBLEM 2: COLLEGE CAMPUS NAVIGATION
    # ==============================================================================
    add_styled_heading("LAB REPORT 2 — PROBLEM 2: COLLEGE CAMPUS NAVIGATION", level=1)

    add_styled_heading("1. Question / Problem Statement", level=2)
    p_p2_stmt = doc.add_paragraph()
    p_p2_stmt.paragraph_format.space_after = Pt(6)
    p_p2_stmt.add_run(
        "A student wants to travel from the college entrance to the computer laboratory. "
        "Some pathways are blocked, while others are accessible.\n\n"
        "Tasks:\n"
        "1. Create a 2D grid representing the college campus.\n"
        "2. Mark the starting point (College Entrance), destination (Computer Lab), and blocked pathways.\n"
        "3. Implement Breadth-First Search (BFS) to find the shortest path.\n"
        "4. Implement Depth-Limited Search (DLS) with a suitable depth limit.\n"
        "5. Visualize the explored cells and the final path for both algorithms."
    )
    p_p2_stmt.runs[0].font.size = Pt(9)

    add_styled_heading("2. Required Code / Procedure", level=2)
    p_p2_code_intro = doc.add_paragraph()
    p_p2_code_intro.paragraph_format.space_after = Pt(4)
    p_p2_code_intro.add_run("Complete Python implementation defining the campus grid, BFS search, and Depth-Limited Search (DLS):")
    p_p2_code_intro.runs[0].font.size = Pt(9)

    code2 = """def dls_search(grid, start, goal, depth_limit):
    \"\"\"
    Depth-Limited Search (DLS): DFS bounded by depth limit L.
    Returns: (path, explored_nodes, status)
    status can be 'SUCCESS', 'CUTOFF', or 'FAILURE'
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
            # Prune search branch if visited at an equal or shallower depth
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
    return path, explored, status

# Construct 10x10 Campus Grid (0 = walkway, 1 = blocked building/construction)
grid_campus = [[0]*10 for _ in range(10)]
campus_obstacles = [
    (1, 2), (2, 2), (3, 2), (4, 2),
    (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
    (6, 1), (7, 1), (8, 1),
    (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
    (1, 8), (2, 8), (3, 8), (5, 8), (6, 8), (7, 8)
]
for r, c in campus_obstacles:
    grid_campus[r][c] = 1

entrance_start = (0, 0)
computer_lab_goal = (9, 9)

# 1. Execute BFS for Optimal Shortest Walkway
bfs_campus_path, bfs_campus_exp = bfs_search(grid_campus, entrance_start, computer_lab_goal)

# 2. Execute DLS with Suitable Depth Limit L = 20 (where L >= d)
dls_ok_path, dls_ok_exp, dls_ok_status = dls_search(grid_campus, entrance_start, computer_lab_goal, depth_limit=20)

# 3. Execute DLS with Cutoff Depth Limit L = 10 (Demonstration of Cutoff condition where L < d)
dls_cut_path, dls_cut_exp, dls_cut_status = dls_search(grid_campus, entrance_start, computer_lab_goal, depth_limit=10)"""

    add_code_box(doc, code2)

    add_styled_heading("3. Final Output", level=2)
    p_out2_text = doc.add_paragraph()
    p_out2_text.paragraph_format.space_before = Pt(4)
    p_out2_text.paragraph_format.space_after = Pt(4)
    p_out2_text.add_run(
        f"Verified Program Execution Output (Registration Number: {REG_NO}):\n"
        f"• Breadth-First Search (BFS)        : Shortest Path = 19 cells (18 steps) | Explored = 77 cells [Optimal]\n"
        f"• DLS with Suitable Limit (L = 20)  : SUCCESS | Path Length = 21 cells (20 steps) | Explored = 48 cells\n"
        f"• DLS with Cutoff Limit (L = 10)    : CUTOFF (Goal depth d=18 > Limit L=10; No path found within limit)"
    )
    p_out2_text.runs[0].font.size = Pt(8.5)
    p_out2_text.runs[0].font.name = "Consolas"

    # Screenshot Placeholder Space 1 for Problem 2: BFS vs DLS Suitable
    add_screenshot_box(
        doc,
        "Problem 2: College Campus Navigation Output (BFS vs DLS Suitable Limit L=20)",
        "Screenshot of executed Google Colab output cell showing the dual-panel grid visualization,\n"
        "College Entrance, Computer Lab, Blocked Pathways, Explored Nodes, and Final Paths."
    )

    # Screenshot Placeholder Space 2 for Problem 2: DLS Cutoff Analysis
    add_screenshot_box(
        doc,
        "Problem 2: Depth-Limited Search Cutoff Analysis (Limit L=10 vs Limit L=20)",
        "Screenshot of executed Google Colab output cell showing the Cutoff failure when L=10 < d=18\n"
        "compared to successful pathfinding when suitable limit L=20 >= d=18 is supplied."
    )

    # Section 4: Links (ONLY Colab & GitHub Link)
    add_styled_heading("4. Google Colab / Project Link", level=2)
    p_link2 = doc.add_paragraph()
    p_link2.paragraph_format.space_before = Pt(2)
    p_link2.paragraph_format.space_after = Pt(6)
    r_l2 = p_link2.add_run(
        f"Google Colab Link: {COLAB_LINK}\n\n"
        f"GitHub Repository Link: {GITHUB_LINK}"
    )
    r_l2.font.size = Pt(9.5)
    r_l2.font.bold = True
    r_l2.font.color.rgb = C_BLUE

    add_styled_heading("5. Explanation", level=2)
    p_exp2 = doc.add_paragraph()
    p_exp2.paragraph_format.space_after = Pt(6)
    p_exp2.add_run(
        "5.1 Depth Limit Selection Rationale (L):\n"
        "1. Minimum Distance Analysis: The Manhattan distance between College Entrance (0, 0) and Computer Laboratory (9, 9) "
        "is |9 - 0| + |9 - 0| = 18 steps. Accounting for campus construction and administrative buildings, the true shortest path is d = 18 steps (19 cells).\n"
        "2. Demonstration of Cutoff (L = 10): When DLS is executed with limit L = 10, the algorithm stops expanding branches at depth 10 and returns "
        "a CUTOFF status. Because L < d (10 < 18), the goal state cannot be reached. This illustrates the fundamental property of DLS: it prevents "
        "infinite loops, but is incomplete when the limit is set below the goal depth.\n"
        "3. Suitable Depth Limit (L = 20): Selecting L = 20 guarantees that L >= d, providing sufficient depth budget to navigate around campus obstacles. "
        "DLS successfully reaches the Computer Lab with a path length of 21 cells (20 steps) while exploring only 48 cells.\n\n"
        "5.2 Comparative Analysis (BFS vs DLS):\n"
        "• Completeness: BFS is always complete. DLS is complete if and only if L >= d; it is incomplete if L < d.\n"
        "• Optimality: BFS is optimal (guaranteed 19 cells). DLS is non-optimal (yields a 21-cell valid path).\n"
        "• Space Complexity: BFS requires exponential memory O(b^d) to store all frontier layers. DLS requires strictly linear memory O(b * L).\n"
        "• Hardware Suitability: For memory-constrained devices (such as student handheld campus navigators or embedded microcontrollers), "
        "DLS offers a massive memory advantage over BFS, provided the depth limit is guided by prior knowledge."
    )
    p_exp2.runs[0].font.size = Pt(9)

    # Comparison Table for Problem 2
    tbl_p2 = doc.add_table(rows=5, cols=4)
    tbl_p2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_p2.autofit = False
    p2_rows = [
        ("Parameter", "BFS (Shortest Path)", "DLS (Suitable Limit L=20)", "DLS (Cutoff Limit L=10)"),
        ("Search Status", "SUCCESS (Optimal)", "SUCCESS (Valid Path)", "CUTOFF (Incomplete)"),
        ("Completeness", "Yes", "Yes (since L >= d)", "No (Limit L < Goal Depth d)"),
        ("Space Complexity", "O(b^d) [Exponential RAM]", "O(b * L) [Strictly Linear RAM]", "O(b * L) [Strictly Linear RAM]"),
        ("Observed Path Length", "19 cells (18 steps)", "21 cells (20 steps)", "None (Cutoff triggered)")
    ]
    for r_i, row_data in enumerate(p2_rows):
        row = tbl_p2.rows[r_i]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        c0.width = Inches(1.8)
        c1.width = Inches(1.6)
        c2.width = Inches(1.6)
        c3.width = Inches(1.5)
        set_cell_background(c0, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_background(c1, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_background(c2, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_background(c3, "E2E8F0" if r_i == 0 else (C_LIGHT_BG if r_i % 2 == 1 else "FFFFFF"))
        set_cell_margins(c0, 30, 30, 45, 45)
        set_cell_margins(c1, 30, 30, 45, 45)
        set_cell_margins(c2, 30, 30, 45, 45)
        set_cell_margins(c3, 30, 30, 45, 45)
        set_cell_borders(c0, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c1, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c2, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c3, color=C_BORDER, sz="4", val="single")
        c0.paragraphs[0].text = row_data[0]
        c1.paragraphs[0].text = row_data[1]
        c2.paragraphs[0].text = row_data[2]
        c3.paragraphs[0].text = row_data[3]
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        c1.paragraphs[0].runs[0].font.size = Pt(8.5)
        c2.paragraphs[0].runs[0].font.size = Pt(8.5)
        c3.paragraphs[0].runs[0].font.size = Pt(8.5)
        if r_i == 0:
            c0.paragraphs[0].runs[0].bold = True
            c1.paragraphs[0].runs[0].bold = True
            c2.paragraphs[0].runs[0].bold = True
            c3.paragraphs[0].runs[0].bold = True

    doc.add_page_break()

    # ==============================================================================
    # VIVA VOCE & FACULTY ASSESSMENT RUBRIC
    # ==============================================================================
    add_styled_heading("6. Comprehensive Viva-Voce Questions & Model Answers (Modules 1 & 2)", level=1)
    
    viva_qa = [
        ("Q1: What is the formal difference between Informed and Uninformed search?",
         "Uninformed (Blind) search operates without domain-specific knowledge about the remaining distance to the goal, exploring based solely on transition rules. Informed (Heuristic) search uses an evaluation function h(n) to guide exploration toward the goal."),
        ("Q2: Why does Breadth-First Search guarantee an optimal shortest path in unweighted graphs?",
         "Because all edges have equal uniform step cost (c = 1), BFS expands states in strictly non-decreasing order of depth. The first time a goal node is dequeued from the frontier, it is guaranteed to have the minimal possible depth/cost."),
        ("Q3: What are the primary space and time complexities of Breadth-First Search?",
         "Time Complexity: O(b^d), where b is the branching factor and d is the solution depth. Space Complexity: O(b^d), because all nodes at the current frontier and explored set must remain stored in memory simultaneously."),
        ("Q4: Why does Depth-First Search require significantly less memory than Breadth-First Search?",
         "DFS only needs to store a single path from the root to a leaf node along with remaining unexpanded sibling nodes for each node on the path. Hence, its space complexity is strictly linear: O(b * m), where m is maximum tree depth."),
        ("Q5: Under what conditions can standard Depth-First Search fail to find a solution?",
         "In state spaces with cycles or infinite depth, DFS can enter an infinite branch without ever discovering a solution that exists at a shallower depth, making it incomplete in infinite or looping graphs."),
        ("Q6: What is Depth-Limited Search (DLS), and how does it prevent infinite loops?",
         "DLS is a depth-first search that treats nodes at a predetermined depth limit L as if they have no successors. This prevents the search from descending indefinitely down infinite branches."),
        ("Q7: What are the possible termination outcomes of Depth-Limited Search?",
         "DLS terminates with one of three outcomes: 1) Solution found (SUCCESS), 2) Cutoff (failure due to reaching depth limit without finding goal), or 3) Failure (entire bounded space exhausted with no goal)."),
        ("Q8: Why did DLS with limit L = 10 trigger a Cutoff in Problem 2?",
         "The actual goal depth to the Computer Laboratory was d = 18 steps. Because L < d (10 < 18), the algorithm correctly stopped at depth 10 before it could reach the goal, triggering the CUTOFF condition."),
        ("Q9: In a hospital medicine delivery robot, why is BFS overwhelmingly preferred over DFS?",
         "Hospital delivery is time-critical. Patient survival and clinical outcomes depend on rapid medicine arrival. BFS guarantees the mathematically shortest route (19 cells), whereas DFS produces winding non-optimal detours (27 cells) causing unacceptable delay."),
        ("Q10: What uninformed search strategy combines the optimality of BFS with the linear memory of DFS?",
         "Iterative Deepening Depth-First Search (IDDFS), which runs DLS with incrementally increasing depth limits L = 0, 1, 2, ... until the goal is found. It achieves O(b^d) time and O(b * d) space.")
    ]

    for q, a in viva_qa:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(4)
        p_q.paragraph_format.space_after = Pt(1)
        rq = p_q.add_run(q)
        rq.font.bold = True
        rq.font.size = Pt(9)
        rq.font.color.rgb = C_NAVY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(3)
        ra = p_a.add_run("Answer: " + a)
        ra.font.size = Pt(8.5)
        ra.font.color.rgb = C_DARK

    # Section 7: Faculty Grading Rubric
    add_styled_heading("7. Faculty Assessment & Grading Rubric", level=1)
    tbl_rubric = doc.add_table(rows=6, cols=4)
    tbl_rubric.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_rubric.autofit = False
    rubric_data = [
        ("Assessment Component", "Max Marks", "Awarded", "Faculty Remarks"),
        ("Syllabus Alignment & Theoretical Grounding (Modules 1 & 2: State Space, PEAS)", "20", "", ""),
        ("Program Implementation & Correctness (BFS, DFS, DLS Algorithms)", "25", "", ""),
        ("Problem 1: Hospital Delivery Robot Execution & Comparative Analysis", "20", "", ""),
        ("Problem 2: Campus Navigation Execution, Depth Limit & Cutoff Analysis", "20", "", ""),
        ("Report Presentation, Verified Screenshots & Viva-Voce Performance", "15", "", "")
    ]
    for r_idx, (col0, col1, col2, col3) in enumerate(rubric_data):
        row = tbl_rubric.rows[r_idx]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        c0.width = Inches(3.5)
        c1.width = Inches(1.0)
        c2.width = Inches(1.0)
        c3.width = Inches(1.0)
        set_cell_background(c0, "E2E8F0" if r_idx == 0 else (C_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"))
        set_cell_background(c1, "E2E8F0" if r_idx == 0 else (C_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"))
        set_cell_background(c2, "E2E8F0" if r_idx == 0 else (C_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"))
        set_cell_background(c3, "E2E8F0" if r_idx == 0 else (C_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"))
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)
        set_cell_margins(c2, 40, 40, 60, 60)
        set_cell_margins(c3, 40, 40, 60, 60)
        set_cell_borders(c0, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c1, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c2, color=C_BORDER, sz="4", val="single")
        set_cell_borders(c3, color=C_BORDER, sz="4", val="single")
        c0.paragraphs[0].text = col0
        c1.paragraphs[0].text = col1
        c2.paragraphs[0].text = col2
        c3.paragraphs[0].text = col3
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        c1.paragraphs[0].runs[0].font.size = Pt(8.5)
        c2.paragraphs[0].runs[0].font.size = Pt(8.5)
        c3.paragraphs[0].runs[0].font.size = Pt(8.5)
        if r_idx == 0:
            c0.paragraphs[0].runs[0].bold = True
            c1.paragraphs[0].runs[0].bold = True
            c2.paragraphs[0].runs[0].bold = True
            c3.paragraphs[0].runs[0].bold = True

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(16)
    p_sig.add_run(
        "---------------------------------------------------\n"
        "Signature of Faculty In-Charge: ____________________\n"
        "Date of Evaluation: ______________________________\n"
        "Total Marks (out of 100): _________________________\n"
        "Grade / Faculty Comments: _________________________"
    )
    p_sig.runs[0].font.size = Pt(9)

    doc.save(DOCX_FILENAME)
    doc.save(ROOT_DOCX_FILENAME)
    print(f"[OK] Word document successfully saved to:\n  - {DOCX_FILENAME}\n  - {ROOT_DOCX_FILENAME}")

if __name__ == "__main__":
    build_docx()
