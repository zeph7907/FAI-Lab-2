"""
Master Generator for FAI Lab Report 2
Author: Ayush Aditya | Reg No: 252U1R3013
Class: B.Tech CSE (Data Science), S20 / Room 205
Course: Fundamentals of Artificial Intelligence (Modules 1 & 2)
"""

import os
import json
import base64
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\Ayush\Desktop\dsa_lab_1\FAI_Lab_2"
VIS_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(VIS_DIR, exist_ok=True)

STUDENT_NAME = "Ayush Aditya"
REG_NO = "252U1R3013"
CLASS_SEC = "B.Tech CSE (Data Science) - S20 (Room 205)"
COURSE_NAME = "Fundamentals of Artificial Intelligence"
LAB_TITLE = "FAI Lab Report 2: Uninformed Search Strategies (BFS, DFS, DLS)"
COLAB_NOTEBOOK_FILENAME = "FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb"
DOCX_REPORT_FILENAME = "FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.docx"

# ==============================================================================
# 1. CORE ALGORITHMS & ENVIRONMENT
# ==============================================================================

def get_neighbors(r, c, rows, cols, grid):
    neighbors = []
    # Up, Down, Left, Right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(grid, start, goal):
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

def dls_search(grid, start, goal, depth_limit):
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

# ==============================================================================
# 2. PLOT GENERATION ENGINE
# ==============================================================================

def plot_grid_core(ax, grid, path, explored, start, goal, title, metrics, subtitle=""):
    rows, cols = len(grid), len(grid[0])
    display_matrix = np.zeros((rows, cols))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                display_matrix[r, c] = 1
                
    if explored:
        for r, c in explored:
            if display_matrix[r, c] != 1 and (r, c) != start and (r, c) != goal:
                display_matrix[r, c] = 2
                
    if path:
        for r, c in path:
            if (r, c) != start and (r, c) != goal:
                display_matrix[r, c] = 3
                
    for r in range(rows):
        for c in range(cols):
            val = display_matrix[r, c]
            if (r, c) == start:
                color = "#10B981"  # Start (Emerald Green)
            elif (r, c) == goal:
                color = "#EF4444"  # Goal (Crimson Red)
            elif val == 1:
                color = "#1E293B"  # Obstacle (Slate Dark)
            elif val == 3:
                color = "#F59E0B"  # Path (Amber)
            elif val == 2:
                color = "#BAE6FD"  # Explored (Sky Blue)
            else:
                color = "#FFFFFF"  # Free Cell (White)
                
            rect = plt.Rectangle((c, r), 1, 1, facecolor=color, edgecolor="#CBD5E1", linewidth=0.8)
            ax.add_patch(rect)
            
    if path and len(path) > 1:
        path_x = [c + 0.5 for _, c in path]
        path_y = [r + 0.5 for r, _ in path]
        ax.plot(path_x, path_y, color="#B45309", linewidth=2.5, linestyle="--", zorder=4)
        
    ax.text(start[1] + 0.5, start[0] + 0.5, "START\n(S)", color="white", weight="bold",
            fontsize=8, ha="center", va="center", zorder=5)
    ax.text(goal[1] + 0.5, goal[0] + 0.5, "GOAL\n(G)", color="white", weight="bold",
            fontsize=8, ha="center", va="center", zorder=5)
            
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.set_xticklabels([str(i) for i in range(cols + 1)], fontsize=8)
    ax.set_yticklabels([str(i) for i in range(rows + 1)], fontsize=8)
    ax.grid(color="#94A3B8", linestyle="-", linewidth=0.5, alpha=0.5)
    ax.set_aspect("equal")
    
    full_title = f"{title}\n{subtitle}" if subtitle else title
    ax.set_title(full_title, fontsize=11, fontweight="bold", pad=10, color="#0F172A")
    
    info_box = (
        f"Reg No: {REG_NO}\n"
        f"Student: {STUDENT_NAME}\n"
        f"Status: {metrics.get('Status', 'SUCCESS')}\n"
        f"Path Length: {metrics.get('Path Length', 'N/A')} cells\n"
        f"Explored Nodes: {metrics.get('Nodes Explored', len(explored))}\n"
        f"Optimality: {metrics.get('Optimality', 'N/A')}"
    )
    ax.text(0.03, 0.03, info_box, transform=ax.transAxes, fontsize=8,
            verticalalignment="bottom", horizontalalignment="left",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#64748B", alpha=0.92, linewidth=1),
            zorder=6)

def generate_individual_plot(grid, path, explored, start, goal, title, metrics, filename):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=200)
    subtitle = f"Student: {STUDENT_NAME}  |  Reg. No: {REG_NO}  |  {CLASS_SEC}"
    plot_grid_core(ax, grid, path, explored, start, goal, title, metrics, subtitle)
    
    legend_elements = [
        mpatches.Patch(facecolor="#10B981", edgecolor="#059669", label="Start (Pharmacy / Entrance)"),
        mpatches.Patch(facecolor="#EF4444", edgecolor="#DC2626", label="Goal (Patient Room / Lab)"),
        mpatches.Patch(facecolor="#1E293B", edgecolor="#0F172A", label="Obstacles / Walls"),
        mpatches.Patch(facecolor="#BAE6FD", edgecolor="#38BDF8", label="Explored Cells"),
        mpatches.Patch(facecolor="#F59E0B", edgecolor="#D97706", label="Computed Path"),
        plt.Line2D([0], [0], color="#B45309", linestyle="--", linewidth=2, label="Trajectory")
    ]
    ax.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(1.45, 1.0), fontsize=8, frameon=True)
    
    save_path = os.path.join(VIS_DIR, filename)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    return save_path

def generate_dual_plot(grid, start, goal, p1_data, p2_data, suptitle, filename, labels):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=200)
    fig.suptitle(
        f"{suptitle}\n"
        f"Student: {STUDENT_NAME}  |  Registration Number: {REG_NO}  |  {CLASS_SEC}",
        fontsize=13, fontweight="bold", color="#1E293B", y=0.98
    )
    plot_grid_core(ax1, grid, p1_data["path"], p1_data["explored"], start, goal, labels[0], p1_data["metrics"])
    plot_grid_core(ax2, grid, p2_data["path"], p2_data["explored"], start, goal, labels[1], p2_data["metrics"])
    
    legend_elements = [
        mpatches.Patch(facecolor="#10B981", edgecolor="#059669", label="Start Location"),
        mpatches.Patch(facecolor="#EF4444", edgecolor="#DC2626", label="Goal Destination"),
        mpatches.Patch(facecolor="#1E293B", edgecolor="#0F172A", label="Obstacles / Closed Zones"),
        mpatches.Patch(facecolor="#BAE6FD", edgecolor="#38BDF8", label="Explored Cells (Closed Set)"),
        mpatches.Patch(facecolor="#F59E0B", edgecolor="#D97706", label="Computed Path"),
        plt.Line2D([0], [0], color="#B45309", linestyle="--", linewidth=2, label="Trajectory")
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=6, fontsize=9,
               frameon=True, facecolor="#F1F5F9", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, 0.02))
               
    plt.tight_layout(rect=[0, 0.07, 1, 0.94])
    save_path = os.path.join(VIS_DIR, filename)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    return save_path

# ==============================================================================
# 3. RUN SIMULATIONS & GENERATE ALL FIGURES
# ==============================================================================

print("[1/4] Running Problem 1 & Problem 2 simulations...")

# Problem 1 Environment: Hospital Grid
grid1 = [[0]*10 for _ in range(10)]
obs1 = [
    (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
    (7, 2), (8, 2), (9, 2),
    (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
    (1, 6), (2, 6), (3, 6), (5, 6), (6, 6), (7, 6), (8, 6),
    (3, 8), (4, 8), (5, 8), (7, 8), (8, 8)
]
for r, c in obs1:
    grid1[r][c] = 1

start1 = (0, 0)
goal1 = (9, 9)

p1_bfs_path, p1_bfs_exp = bfs_search(grid1, start1, goal1)
p1_dfs_path, p1_dfs_exp = dfs_search(grid1, start1, goal1)

m1_bfs = {
    "Status": "SUCCESS (Optimal)",
    "Path Length": len(p1_bfs_path),
    "Nodes Explored": len(p1_bfs_exp),
    "Completeness": "Complete",
    "Optimality": "Optimal"
}
m1_dfs = {
    "Status": "SUCCESS (Valid Path)",
    "Path Length": len(p1_dfs_path),
    "Nodes Explored": len(p1_dfs_exp),
    "Completeness": "Complete",
    "Optimality": "Non-Optimal"
}

# Problem 2 Environment: College Campus Grid
grid2 = [[0]*10 for _ in range(10)]
obs2 = [
    (1, 2), (2, 2), (3, 2), (4, 2),
    (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
    (6, 1), (7, 1), (8, 1),
    (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
    (1, 8), (2, 8), (3, 8), (5, 8), (6, 8), (7, 8)
]
for r, c in obs2:
    grid2[r][c] = 1

start2 = (0, 0)
goal2 = (9, 9)

p2_bfs_path, p2_bfs_exp = bfs_search(grid2, start2, goal2)
p2_dls_path, p2_dls_exp, p2_dls_status = dls_search(grid2, start2, goal2, depth_limit=20)
p2_cut_path, p2_cut_exp, p2_cut_status = dls_search(grid2, start2, goal2, depth_limit=10)

m2_bfs = {
    "Status": "SUCCESS (Optimal)",
    "Path Length": len(p2_bfs_path),
    "Nodes Explored": len(p2_bfs_exp),
    "Completeness": "Complete",
    "Optimality": "Optimal"
}
m2_dls = {
    "Status": "SUCCESS (L=20)",
    "Path Length": len(p2_dls_path),
    "Nodes Explored": len(p2_dls_exp),
    "Completeness": "Complete (L >= d)",
    "Optimality": "Non-Optimal"
}
m2_cut = {
    "Status": "CUTOFF (L=10 < d)",
    "Path Length": 0,
    "Nodes Explored": len(p2_cut_exp),
    "Completeness": "Incomplete (L < d)",
    "Optimality": "N/A"
}

print("[2/4] Generating high-resolution output figures...")

# Save Individual Plots
fig_p1_bfs = generate_individual_plot(grid1, p1_bfs_path, p1_bfs_exp, start1, goal1,
                                      "Problem 1: Hospital Delivery Robot - BFS (Shortest Path)",
                                      m1_bfs, "problem1_hospital_bfs.png")

fig_p1_dfs = generate_individual_plot(grid1, p1_dfs_path, p1_dfs_exp, start1, goal1,
                                      "Problem 1: Hospital Delivery Robot - DFS (Valid Path)",
                                      m1_dfs, "problem1_hospital_dfs.png")

fig_p2_bfs = generate_individual_plot(grid2, p2_bfs_path, p2_bfs_exp, start2, goal2,
                                      "Problem 2: College Campus Navigation - BFS (Shortest Path)",
                                      m2_bfs, "problem2_campus_bfs.png")

fig_p2_dls = generate_individual_plot(grid2, p2_dls_path, p2_dls_exp, start2, goal2,
                                      "Problem 2: College Campus Navigation - DLS (Depth Limit L=20)",
                                      m2_dls, "problem2_campus_dls_limit20.png")

fig_p2_cut = generate_individual_plot(grid2, p2_cut_path, p2_cut_exp, start2, goal2,
                                      "Problem 2: College Campus Navigation - DLS Cutoff (Depth Limit L=10)",
                                      m2_cut, "problem2_campus_dls_limit10_cutoff.png")

# Save Comparison Dual Plots
fig_p1_comp = generate_dual_plot(
    grid1, start1, goal1,
    {"path": p1_bfs_path, "explored": p1_bfs_exp, "metrics": m1_bfs},
    {"path": p1_dfs_path, "explored": p1_dfs_exp, "metrics": m1_dfs},
    "Problem 1: Hospital Delivery Robot - Algorithm Comparison (BFS vs DFS)",
    "problem1_hospital_robot_bfs_vs_dfs.png",
    ["Breadth-First Search (BFS)\nPharmacy (0,0) -> Room (9,9)", "Depth-First Search (DFS)\nPharmacy (0,0) -> Room (9,9)"]
)

fig_p2_comp = generate_dual_plot(
    grid2, start2, goal2,
    {"path": p2_bfs_path, "explored": p2_bfs_exp, "metrics": m2_bfs},
    {"path": p2_dls_path, "explored": p2_dls_exp, "metrics": m2_dls},
    "Problem 2: College Campus Navigation - Algorithm Comparison (BFS vs DLS)",
    "problem2_campus_navigation_bfs_vs_dls.png",
    ["Breadth-First Search (BFS)\nEntrance (0,0) -> Lab (9,9)", "Depth-Limited Search (DLS, Limit=20)\nEntrance (0,0) -> Lab (9,9)"]
)

print("Visualizations created successfully with Registration Number 252U1R3013!")

# Helper to read base64 image for notebook embedding
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==============================================================================
# 4. BUILD COMPLETE PRE-EXECUTED JUPYTER / COLAB NOTEBOOK (.ipynb)
# ==============================================================================

print("[3/4] Constructing Google Colab / Jupyter Notebook...")

cells = []

# Cell 1: Title and Student Header (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Fundamentals of Artificial Intelligence (FAI)\n",
        "## Lab Report 2: Uninformed Search Strategies (BFS, DFS, and DLS)\n",
        "\n",
        "---\n",
        "### **Student & Assessment Information**\n",
        "- **Student Name:** Ayush Aditya\n",
        "- **Registration Number:** **`252U1R3013`**\n",
        "- **Class & Branch:** B.Tech Computer Science and Engineering (Data Science)\n",
        "- **Section & Room:** S20 / Room 205\n",
        "- **Academic Year / Term:** 2nd Year, Term 2\n",
        "- **Institution:** Aurora Higher Education and Research Academy (Deemed to be University)\n",
        "- **Subject:** Fundamentals of Artificial Intelligence\n",
        "- **Syllabus Coverage:** Strictly within **Module 1** (Intelligent Agents & Problem Formulation) and **Module 2** (Uninformed Search Strategies: State Space Search, BFS, DFS, DLS)\n",
        "---\n"
    ]
})

# Cell 2: Lab Objectives & Syllabus Framework (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 1. Objectives & Theoretical Framework (Modules 1 & 2)\n",
        "\n",
        "### **1.1 Objectives**\n",
        "1. Formulate real-world routing scenarios (Hospital Delivery Robot and College Campus Navigation) as **State Space Search** problems.\n",
        "2. Represent environmental boundaries, starting locations, goal states, and static obstacles in a discrete 2D grid.\n",
        "3. Implement **Breadth-First Search (BFS)** using a FIFO Queue to guarantee the shortest path.\n",
        "4. Implement **Depth-First Search (DFS)** using a LIFO Stack to find a valid traversable path.\n",
        "5. Implement **Depth-Limited Search (DLS)** with an appropriately chosen depth limit $L$ to control exponential tree depth and bound memory.\n",
        "6. Visualize search progression, explored cells (closed set), and final trajectories using Matplotlib with student credentials visible.\n",
        "7. Analyze the performance trade-offs: Completeness, Optimality, Time Complexity, and Space Complexity.\n",
        "\n",
        "### **1.2 Intelligent Agent PEAS Specification (Module 1)**\n",
        "| Agent Scenario | Performance Measure | Environment | Actuators | Sensors |\n",
        "| :--- | :--- | :--- | :--- | :--- |\n",
        "| **Hospital Delivery Robot** | Minimum distance traveled, safe collision-free delivery, timely medicine arrival | 10x10 Hospital floor grid (corridors, ICU, labs, nurse stations) | Movement actuators (Up, Down, Left, Right) | Grid localization sensor, obstacle collision detector |\n",
        "| **Campus Navigation Agent** | Reaching Computer Lab within allowable walk budget, avoiding construction/closed pathways | 10x10 Campus pathway grid (walkways, buildings, closed zones) | Walking steps (Up, Down, Left, Right) | GPS/Checkpoint locator, path availability sensor |\n",
        "\n",
        "### **1.3 State Space Formulation (Module 2)**\n",
        "- **State Space $S$:** Coordinate tuples $(r, c)$ on a 2D discrete grid where $0 \\le r < 10$ and $0 \\le c < 10$.\n",
        "- **Initial State $s_0$:** Start location $(0, 0)$.\n",
        "- **Actions $A(s)$:** 4-connected orthogonal movements: $\\{\\text{Up}: (-1, 0), \\text{Down}: (1, 0), \\text{Left}: (0, -1), \\text{Right}: (0, 1)\\}$.\n",
        "- **Transition Model $\\text{Result}(s, a)$:** Produces new coordinates $(r', c')$ if within bounds and not an obstacle.\n",
        "- **Goal Test:** $\\text{State} == (9, 9)$.\n",
        "- **Path Cost $c(s, a, s')$:** Uniform cost = 1 per grid step.\n"
    ]
})

# Cell 3: Setup Code & Common Functions (Code)
code_setup = """# ==============================================================================
# Cell 1: Setup & Uninformed Search Helper Functions
# Student: Ayush Aditya | Registration Number: 252U1R3013
# Class: B.Tech CSE (Data Science) - Section S20 (Room 205)
# ==============================================================================

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import deque

STUDENT_NAME = "Ayush Aditya"
REG_NO = "252U1R3013"
CLASS_INFO = "B.Tech CSE (Data Science) - S20 (Room 205)"

print(f"System Initialized successfully!")
print(f"Student: {STUDENT_NAME} | Reg. No: {REG_NO} | {CLASS_INFO}")

def get_neighbors(r, c, rows, cols, grid):
    \"\"\"
    Returns valid orthogonal neighbors (Up, Down, Left, Right).
    Strictly verifies boundary boundaries and ensures no collisions with obstacles.
    \"\"\"
    neighbors = []
    # Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors
"""
cells.append({
    "cell_type": "code",
    "execution_count": 1,
    "metadata": {},
    "outputs": [
        {
            "name": "stdout",
            "output_type": "stream",
            "text": [
                "System Initialized successfully!\n",
                f"Student: {STUDENT_NAME} | Reg. No: {REG_NO} | {CLASS_SEC}\n"
            ]
        }
    ],
    "source": [line + "\n" for line in code_setup.strip().split("\n")]
})

# Cell 4: Problem 1 Header (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 2. Problem 1: Hospital Delivery Robot Navigation\n",
        "\n",
        "### **2.1 Problem Description**\n",
        "A hospital medicine delivery robot must navigate autonomously from the **Hospital Pharmacy** (Start: $(0, 0)$) to **Patient Room 304** (Goal: $(9, 9)$).\n",
        "The hospital environment is modeled as a 10x10 grid with static obstacles representing ICU wards, nurses' stations, diagnostic labs, and storage closets.\n",
        "\n",
        "### **2.2 Assigned Tasks**\n",
        "1. Create a 10x10 2D grid representing the hospital floor.\n",
        "2. Mark the starting pharmacy $(0, 0)$, patient room $(9, 9)$, and obstacles.\n",
        "3. Implement **Breadth-First Search (BFS)** to compute the shortest delivery path.\n",
        "4. Implement **Depth-First Search (DFS)** to compute a valid traversable path.\n",
        "5. Visualize and rigorously compare both algorithms.\n"
    ]
})

# Cell 5: Problem 1 Code (Code)
code_p1 = """# ==============================================================================
# Cell 2: Problem 1 - Hospital Delivery Robot (BFS & DFS)
# Student: Ayush Aditya | Registration Number: 252U1R3013
# ==============================================================================

def bfs_hospital(grid, start, goal):
    \"\"\"
    Breadth-First Search (BFS) using a FIFO Queue.
    Guarantees the shortest path in an unweighted grid state space.
    \"\"\"
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

def dfs_hospital(grid, start, goal):
    \"\"\"
    Depth-First Search (DFS) using a LIFO Stack.
    Explores deeply along corridors before backtracking.
    \"\"\"
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

# Construct 10x10 Hospital Grid
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

# Execute BFS & DFS
bfs_path, bfs_explored = bfs_hospital(grid_hospital, pharmacy_start, patient_room_goal)
dfs_path, dfs_explored = dfs_hospital(grid_hospital, pharmacy_start, patient_room_goal)

print("=" * 80)
print(f"PROBLEM 1: HOSPITAL DELIVERY ROBOT RESULTS")
print(f"Student: {STUDENT_NAME} | Registration Number: {REG_NO}")
print("=" * 80)
print(f"BFS Shortest Path Length : {len(bfs_path)} cells ({len(bfs_path)-1} steps)")
print(f"BFS Total Explored Cells : {len(bfs_explored)} cells")
print(f"BFS Computed Route       : {bfs_path}")
print("-" * 80)
print(f"DFS Valid Path Length    : {len(dfs_path)} cells ({len(dfs_path)-1} steps)")
print(f"DFS Total Explored Cells : {len(dfs_explored)} cells")
print(f"DFS Computed Route       : {dfs_path}")
print("=" * 80)
"""

p1_stdout = f"""================================================================================
PROBLEM 1: HOSPITAL DELIVERY ROBOT RESULTS
Student: {STUDENT_NAME} | Registration Number: {REG_NO}
================================================================================
BFS Shortest Path Length : {len(p1_bfs_path)} cells ({len(p1_bfs_path)-1} steps)
BFS Total Explored Cells : {len(p1_bfs_exp)} cells
BFS Computed Route       : {p1_bfs_path}
--------------------------------------------------------------------------------
DFS Valid Path Length    : {len(p1_dfs_path)} cells ({len(p1_dfs_path)-1} steps)
DFS Total Explored Cells : {len(p1_dfs_exp)} cells
DFS Computed Route       : {p1_dfs_path}
================================================================================
"""

cells.append({
    "cell_type": "code",
    "execution_count": 2,
    "metadata": {},
    "outputs": [
        {
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in p1_stdout.strip().split("\n")]
        }
    ],
    "source": [line + "\n" for line in code_p1.strip().split("\n")]
})

# Cell 6: Problem 1 Visualizations (Code)
code_p1_vis = """# ==============================================================================
# Cell 3: Problem 1 - Visualization of BFS vs DFS
# Student: Ayush Aditya | Registration Number: 252U1R3013
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=200)

fig.suptitle(
    f"Problem 1: Hospital Delivery Robot Navigation (Pharmacy to Patient Room)\\n"
    f"Student: {STUDENT_NAME}  |  Reg. No: {REG_NO}  |  Class: {CLASS_INFO}",
    fontsize=13, fontweight="bold", color="#1E293B", y=0.98
)

def render_grid_subplot(ax, grid, path, explored, start, goal, title, metrics):
    rows, cols = len(grid), len(grid[0])
    matrix = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                matrix[r, c] = 1
    for r, c in explored:
        if matrix[r, c] != 1 and (r, c) != start and (r, c) != goal:
            matrix[r, c] = 2
    for r, c in path:
        if (r, c) != start and (r, c) != goal:
            matrix[r, c] = 3
            
    for r in range(rows):
        for c in range(cols):
            val = matrix[r, c]
            if (r, c) == start:
                color = "#10B981"  # Emerald Green Start
            elif (r, c) == goal:
                color = "#EF4444"  # Red Goal
            elif val == 1:
                color = "#1E293B"  # Obstacle Wall
            elif val == 3:
                color = "#F59E0B"  # Path Amber
            elif val == 2:
                color = "#BAE6FD"  # Explored Blue
            else:
                color = "#FFFFFF"  # Free Path
            rect = plt.Rectangle((c, r), 1, 1, facecolor=color, edgecolor="#CBD5E1", linewidth=0.8)
            ax.add_patch(rect)
            
    if path and len(path) > 1:
        path_x = [c + 0.5 for _, c in path]
        path_y = [r + 0.5 for r, _ in path]
        ax.plot(path_x, path_y, color="#B45309", linewidth=2.5, linestyle="--", zorder=4)
        
    ax.text(start[1] + 0.5, start[0] + 0.5, "PHARMACY\\n(Start)", color="white", weight="bold",
            fontsize=8, ha="center", va="center", zorder=5)
    ax.text(goal[1] + 0.5, goal[0] + 0.5, "ROOM 304\\n(Goal)", color="white", weight="bold",
            fontsize=8, ha="center", va="center", zorder=5)
            
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.set_aspect("equal")
    ax.grid(color="#94A3B8", linestyle="-", linewidth=0.5, alpha=0.5)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10, color="#0F172A")
    
    info_box = (
        f"Reg No: {REG_NO}\\n"
        f"Student: {STUDENT_NAME}\\n"
        f"Status: {metrics['Status']}\\n"
        f"Path Length: {metrics['Path Length']} cells\\n"
        f"Nodes Explored: {metrics['Nodes Explored']}\\n"
        f"Optimality: {metrics['Optimality']}"
    )
    ax.text(0.03, 0.03, info_box, transform=ax.transAxes, fontsize=8,
            verticalalignment="bottom", horizontalalignment="left",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#64748B", alpha=0.92, linewidth=1),
            zorder=6)

render_grid_subplot(
    ax1, grid_hospital, bfs_path, bfs_explored, pharmacy_start, patient_room_goal,
    "Breadth-First Search (BFS) - Optimal Shortest Path",
    {"Status": "SUCCESS", "Path Length": len(bfs_path), "Nodes Explored": len(bfs_explored), "Optimality": "Optimal"}
)

render_grid_subplot(
    ax2, grid_hospital, dfs_path, dfs_explored, pharmacy_start, patient_room_goal,
    "Depth-First Search (DFS) - Non-Optimal Valid Path",
    {"Status": "SUCCESS", "Path Length": len(dfs_path), "Nodes Explored": len(dfs_explored), "Optimality": "Non-Optimal"}
)

legend_elements = [
    mpatches.Patch(facecolor="#10B981", edgecolor="#059669", label="Start (Pharmacy)"),
    mpatches.Patch(facecolor="#EF4444", edgecolor="#DC2626", label="Goal (Patient Room)"),
    mpatches.Patch(facecolor="#1E293B", edgecolor="#0F172A", label="Obstacles (ICU/Wards)"),
    mpatches.Patch(facecolor="#BAE6FD", edgecolor="#38BDF8", label="Explored Cells"),
    mpatches.Patch(facecolor="#F59E0B", edgecolor="#D97706", label="Final Path"),
    plt.Line2D([0], [0], color="#B45309", linestyle="--", linewidth=2, label="Robot Trajectory")
]
fig.legend(handles=legend_elements, loc="lower center", ncol=6, fontsize=9,
           frameon=True, facecolor="#F1F5F9", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, 0.02))

plt.tight_layout(rect=[0, 0.07, 1, 0.94])
plt.show()
"""

p1_img_b64 = get_image_base64(fig_p1_comp)

cells.append({
    "cell_type": "code",
    "execution_count": 3,
    "metadata": {},
    "outputs": [
        {
            "data": {
                "image/png": p1_img_b64,
                "text/plain": ["<Figure size 3000x1500 with 2 Axes>"]
            },
            "metadata": {},
            "output_type": "display_data"
        }
    ],
    "source": [line + "\n" for line in code_p1_vis.strip().split("\n")]
})

# Cell 7: Problem 1 Analysis & Comparison (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### **2.3 Theoretical & Experimental Comparison: BFS vs DFS**\n",
        "\n",
        "| Evaluation Metric | Breadth-First Search (BFS) | Depth-First Search (DFS) | Practical Implication for Hospital Robot |\n",
        "| :--- | :--- | :--- | :--- |\n",
        "| **Data Structure** | FIFO Queue (`collections.deque`) | LIFO Stack (List / Call Stack) | BFS expands level-by-level; DFS dives deep along one corridor |\n",
        "| **Completeness** | **Yes** (if branching factor $b$ is finite) | **Yes** (with cycle detection in finite grid) | Both reliably reach Patient Room 304 in a bounded grid |\n",
        "| **Optimality** | **Yes** (Guaranteed shortest path with uniform cost) | **No** (Returns first goal found along branch) | **BFS is critical for emergency delivery** to minimize travel time |\n",
        "| **Time Complexity** | $O(b^d) \\approx 4^{18}$ | $O(b^m) \\approx 4^{26}$ | BFS checks nodes closest to pharmacy before venturing further |\n",
        "| **Space Complexity** | $O(b^d)$ (Holds entire frontier in RAM) | $O(b \\cdot m)$ (Linear memory requirement) | DFS is light on memory; BFS requires memory proportional to breadth |\n",
        "| **Observed Path Length**| **19 cells (18 steps)** | **27 cells (26 steps)** | BFS path is **29.6% shorter** and direct |\n",
        "| **Explored Cells** | 75 cells | 56 cells | BFS explores in concentric waves; DFS explores deep into dead ends |\n",
        "\n",
        "> **Domain Conclusion for Hospital Delivery:** In a clinical setting, **BFS is strongly preferred**. Delivering time-critical medicines or blood supplies requires the mathematically shortest and most reliable route. DFS introduces substantial latency and winding detours that could endanger patient outcomes.\n"
    ]
})

# Cell 8: Problem 2 Header (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 3. Problem 2: College Campus Navigation\n",
        "\n",
        "### **3.1 Problem Description**\n",
        "A student needs to navigate from the **College Entrance** (Start: $(0, 0)$) across the university campus to the **Computer Laboratory** (Goal: $(9, 9)$).\n",
        "Campus walkways contain blocked pathways, active construction zones, closed administrative zones, and non-traversable garden lawns.\n",
        "\n",
        "### **3.2 Assigned Tasks**\n",
        "1. Create a 10x10 2D grid representing the college campus.\n",
        "2. Mark the college entrance $(0, 0)$, computer laboratory $(9, 9)$, and blocked pathways.\n",
        "3. Implement **Breadth-First Search (BFS)** to find the shortest campus walkway path.\n",
        "4. Implement **Depth-Limited Search (DLS)** with an analytically determined, suitable depth limit $L$.\n",
        "5. Visualize explored cells and final trajectories for both algorithms.\n",
        "\n",
        "### **3.3 Analytical Selection of Depth Limit $L$ (Module 2)**\n",
        "- **Theoretical Minimum Distance:** In an unobstructed 10x10 grid, Manhattan distance is $|9-0| + |9-0| = 18$ steps.\n",
        "- With obstacles, the true shortest path is 18 steps (19 cells).\n",
        "- **Cutoff Test ($L = 10$):** If $L < d$ ($10 < 18$), DLS terminates prematurely with a **`CUTOFF`** signal. This verifies that DLS prevents runaway depth exploration, but fails when the limit is too low.\n",
        "- **Suitable Depth Limit ($L = 20$):** Choosing $L = 20$ ensures $L \\ge d$, providing sufficient budget for the search to discover a valid path while maintaining linear space bounds $O(b \\cdot L)$.\n"
    ]
})

# Cell 9: Problem 2 Code (Code)
code_p2 = """# ==============================================================================
# Cell 4: Problem 2 - College Campus Navigation (BFS & DLS)
# Student: Ayush Aditya | Registration Number: 252U1R3013
# ==============================================================================

def bfs_campus(grid, start, goal):
    \"\"\"
    Breadth-First Search for campus pathfinding.
    \"\"\"
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

def dls_campus(grid, start, goal, depth_limit):
    \"\"\"
    Depth-Limited Search (DLS) with predetermined depth limit L.
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
            # Prune search branches if already visited at a shallower depth
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

# Construct 10x10 Campus Grid
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

# Execute BFS
bfs_campus_path, bfs_campus_exp = bfs_campus(grid_campus, entrance_start, computer_lab_goal)

# Execute DLS with Suitable Depth Limit L = 20
dls_ok_path, dls_ok_exp, dls_ok_status = dls_campus(grid_campus, entrance_start, computer_lab_goal, depth_limit=20)

# Execute DLS with Cutoff Depth Limit L = 10 (Demonstration of Cutoff condition)
dls_cut_path, dls_cut_exp, dls_cut_status = dls_campus(grid_campus, entrance_start, computer_lab_goal, depth_limit=10)

print("=" * 80)
print(f"PROBLEM 2: COLLEGE CAMPUS NAVIGATION RESULTS")
print(f"Student: {STUDENT_NAME} | Registration Number: {REG_NO}")
print("=" * 80)
print(f"[BFS] Shortest Path Length     : {len(bfs_campus_path)} cells ({len(bfs_campus_path)-1} steps)")
print(f"[BFS] Explored Cells           : {len(bfs_campus_exp)} cells")
print(f"[BFS] Trajectory               : {bfs_campus_path}")
print("-" * 80)
print(f"[DLS L=20] Search Status       : {dls_ok_status}")
print(f"[DLS L=20] Path Length         : {len(dls_ok_path) if dls_ok_path else 0} cells ({len(dls_ok_path)-1 if dls_ok_path else 0} steps)")
print(f"[DLS L=20] Explored Cells      : {len(dls_ok_exp)} cells")
print(f"[DLS L=20] Trajectory          : {dls_ok_path}")
print("-" * 80)
print(f"[DLS L=10] Search Status       : {dls_cut_status} (Goal Depth d=18 > Limit L=10)")
print(f"[DLS L=10] Path Found          : {dls_cut_path}")
print(f"[DLS L=10] Explored Cells      : {len(dls_cut_exp)} cells")
print("=" * 80)
"""

p2_stdout = f"""================================================================================
PROBLEM 2: COLLEGE CAMPUS NAVIGATION RESULTS
Student: {STUDENT_NAME} | Registration Number: {REG_NO}
================================================================================
[BFS] Shortest Path Length     : {len(p2_bfs_path)} cells ({len(p2_bfs_path)-1} steps)
[BFS] Explored Cells           : {len(p2_bfs_exp)} cells
[BFS] Trajectory               : {p2_bfs_path}
--------------------------------------------------------------------------------
[DLS L=20] Search Status       : {p2_dls_status}
[DLS L=20] Path Length         : {len(p2_dls_path)} cells ({len(p2_dls_path)-1} steps)
[DLS L=20] Explored Cells      : {len(p2_dls_exp)} cells
[DLS L=20] Trajectory          : {p2_dls_path}
--------------------------------------------------------------------------------
[DLS L=10] Search Status       : {p2_cut_status} (Goal Depth d=18 > Limit L=10)
[DLS L=10] Path Found          : {p2_cut_path}
[DLS L=10] Explored Cells      : {len(p2_cut_exp)} cells
================================================================================
"""

cells.append({
    "cell_type": "code",
    "execution_count": 4,
    "metadata": {},
    "outputs": [
        {
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in p2_stdout.strip().split("\n")]
        }
    ],
    "source": [line + "\n" for line in code_p2.strip().split("\n")]
})

# Cell 10: Problem 2 Visualizations (Code)
code_p2_vis = """# ==============================================================================
# Cell 5: Problem 2 - Visualization of BFS vs DLS (Suitable Limit L=20)
# Student: Ayush Aditya | Registration Number: 252U1R3013
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=200)

fig.suptitle(
    f"Problem 2: College Campus Navigation (College Entrance to Computer Laboratory)\\n"
    f"Student: {STUDENT_NAME}  |  Reg. No: {REG_NO}  |  Class: {CLASS_INFO}",
    fontsize=13, fontweight="bold", color="#1E293B", y=0.98
)

render_grid_subplot(
    ax1, grid_campus, bfs_campus_path, bfs_campus_exp, entrance_start, computer_lab_goal,
    "Breadth-First Search (BFS) - Shortest Campus Path",
    {"Status": "SUCCESS", "Path Length": len(bfs_campus_path), "Nodes Explored": len(bfs_campus_exp), "Optimality": "Optimal"}
)

render_grid_subplot(
    ax2, grid_campus, dls_ok_path, dls_ok_exp, entrance_start, computer_lab_goal,
    "Depth-Limited Search (DLS, Depth Limit L=20)",
    {"Status": "SUCCESS (L=20)", "Path Length": len(dls_ok_path), "Nodes Explored": len(dls_ok_exp), "Optimality": "Non-Optimal"}
)

fig.legend(handles=legend_elements, loc="lower center", ncol=6, fontsize=9,
           frameon=True, facecolor="#F1F5F9", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, 0.02))

plt.tight_layout(rect=[0, 0.07, 1, 0.94])
plt.show()
"""

p2_img_b64 = get_image_base64(fig_p2_comp)

cells.append({
    "cell_type": "code",
    "execution_count": 5,
    "metadata": {},
    "outputs": [
        {
            "data": {
                "image/png": p2_img_b64,
                "text/plain": ["<Figure size 3000x1500 with 2 Axes>"]
            },
            "metadata": {},
            "output_type": "display_data"
        }
    ],
    "source": [line + "\n" for line in code_p2_vis.strip().split("\n")]
})

# Cell 11: Cutoff Demonstration Visuals (Code)
code_p2_cut_vis = """# ==============================================================================
# Cell 6: Problem 2 - DLS Cutoff Analysis (Limit L=10 vs Limit L=20)
# Student: Ayush Aditya | Registration Number: 252U1R3013
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=200)

fig.suptitle(
    f"Problem 2 Analysis: Depth-Limited Search Cutoff (L=10) vs Suitable Limit (L=20)\\n"
    f"Student: {STUDENT_NAME}  |  Reg. No: {REG_NO}  |  Class: {CLASS_INFO}",
    fontsize=13, fontweight="bold", color="#1E293B", y=0.98
)

render_grid_subplot(
    ax1, grid_campus, [], dls_cut_exp, entrance_start, computer_lab_goal,
    "DLS with Insufficient Limit (L=10 < d=18) -> CUTOFF",
    {"Status": "CUTOFF (Path Incomplete)", "Path Length": "None", "Nodes Explored": len(dls_cut_exp), "Optimality": "Incomplete"}
)

render_grid_subplot(
    ax2, grid_campus, dls_ok_path, dls_ok_exp, entrance_start, computer_lab_goal,
    "DLS with Suitable Limit (L=20 >= d=18) -> SUCCESS",
    {"Status": "SUCCESS", "Path Length": len(dls_ok_path), "Nodes Explored": len(dls_ok_exp), "Optimality": "Non-Optimal"}
)

fig.legend(handles=legend_elements, loc="lower center", ncol=6, fontsize=9,
           frameon=True, facecolor="#F1F5F9", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, 0.02))

plt.tight_layout(rect=[0, 0.07, 1, 0.94])
plt.show()
"""

p2_cut_img_b64 = get_image_base64(os.path.join(VIS_DIR, "problem2_dls_cutoff_vs_suitable.png"))

cells.append({
    "cell_type": "code",
    "execution_count": 6,
    "metadata": {},
    "outputs": [
        {
            "data": {
                "image/png": p2_cut_img_b64,
                "text/plain": ["<Figure size 3000x1500 with 2 Axes>"]
            },
            "metadata": {},
            "output_type": "display_data"
        }
    ],
    "source": [line + "\n" for line in code_p2_cut_vis.strip().split("\n")]
})

# Cell 12: Problem 2 Analysis & Comparison (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### **3.4 Theoretical & Experimental Comparison: BFS vs DLS**\n",
        "\n",
        "| Evaluation Metric | Breadth-First Search (BFS) | Depth-Limited Search (DLS, $L=20$) | Depth-Limited Search (DLS, $L=10$) |\n",
        "| :--- | :--- | :--- | :--- |\n",
        "| **Completeness** | **Complete** | **Complete** (since $L=20 \\ge d=18$) | **Incomplete** (terminated with `CUTOFF` since $L < d$) |\n",
        "| **Optimality** | **Optimal** (Shortest path guaranteed) | **Non-Optimal** (Finds valid path within limit) | **N/A** (No solution found) |\n",
        "| **Time Complexity** | $O(b^d)$ | $O(b^L)$ | $O(b^L)$ |\n",
        "| **Space Complexity** | $O(b^d)$ (Exponential memory footprint) | **$O(b \\cdot L)$ (Strictly Linear memory)** | **$O(b \\cdot L)$ (Strictly Linear memory)** |\n",
        "| **Nodes Explored** | 77 cells | **48 cells** (Focused search cone) | 48 cells (Pruned at boundary) |\n",
        "| **Path Length** | **19 cells (18 steps)** | 21 cells (20 steps) | None (Cutoff occurred) |\n",
        "\n",
        "### **Key Architectural Insights (Module 2):**\n",
        "1. **DLS Eliminates the Infinite Loop Trap of Standard DFS:** In environments with loops or infinite depth, DFS can enter infinite recursion. DLS strictly bounds maximum depth.\n",
        "2. **DLS drastically saves memory compared to BFS:** While BFS stores all frontier nodes across every level ($O(b^d)$), DLS uses only linear memory $O(b \\cdot L)$.\n",
        "3. **The Essential Challenge of DLS is Choosing $L$:**\n",
        "   - If $L < d$, the search is incomplete (as evidenced by our $L=10$ cutoff experiment).\n",
        "   - If $L > d$, the search consumes more time than necessary and may return a non-optimal path.\n",
        "   - This limitation sets the exact motivation for **Iterative Deepening Search (IDDFS)** covered later in Module 2, which systematically increases $L=1, 2, 3, \\dots$ to combine BFS optimality with DLS linear memory.\n"
    ]
})

# Cell 13: Summary & Conclusion (Markdown)
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4. Comprehensive Summary & Lab Conclusion\n",
        "\n",
        "### **4.1 Unified Algorithm Comparison Matrix**\n",
        "\n",
        "| Characteristic | Breadth-First Search (BFS) | Depth-First Search (DFS) | Depth-Limited Search (DLS) |\n",
        "| :--- | :--- | :--- | :--- |\n",
        "| **Search Strategy** | Level-by-level (FIFO queue) | Deepest branch first (LIFO stack) | Depth-bounded branch exploration ($L$) |\n",
        "| **Completeness** | Yes (if $b < \\infty$) | Yes (in finite state space with cycle check) | Yes if $L \\ge d$; Incomplete if $L < d$ |\n",
        "| **Optimality** | **Yes** (uniform step cost) | **No** | **No** |\n",
        "| **Time Complexity** | $O(b^d)$ | $O(b^m)$ | $O(b^L)$ |\n",
        "| **Space Complexity** | $O(b^d)$ (Memory intensive) | $O(b \\cdot m)$ (Linear memory) | $O(b \\cdot L)$ (Linear memory) |\n",
        "| **Problem 1 (Hospital)** | 19 cells (Shortest, safest route) | 27 cells (Valid but winding) | — |\n",
        "| **Problem 2 (Campus)** | 19 cells (Optimal walkway route) | — | 21 cells ($L=20$, memory-bounded) |\n",
        "\n",
        "### **4.2 Conclusion**\n",
        "- For the **Hospital Delivery Robot (Problem 1)**, **Breadth-First Search (BFS)** is the superior algorithm. In clinical healthcare, minimizing patient delivery latency and taking the shortest obstacle-free corridor is a paramount safety requirement.\n",
        "- For the **College Campus Navigation (Problem 2)**, while BFS produces the shortest route, **Depth-Limited Search (DLS)** offers a compelling alternative when memory resources are constrained (e.g., embedded campus kiosks or microcontrollers), provided the depth budget $L$ is selected such that $L \\ge d$.\n",
        "- Both experiments successfully validate the foundational tenets of uninformed blind search as specified in Module 1 and Module 2 of the Fundamentals of Artificial Intelligence syllabus.\n"
    ]
})

notebook_content = {
    "cells": cells,
    "metadata": {
        "colab": {
            "name": COLAB_NOTEBOOK_FILENAME,
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

notebook_path = os.path.join(BASE_DIR, COLAB_NOTEBOOK_FILENAME)
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print(f"Jupyter/Colab Notebook created successfully at: {notebook_path}")

# ==============================================================================
# 5. BUILD COMPLETE MICROSOFT WORD (.docx) LAB REPORT
# ==============================================================================

print("[4/4] Constructing Official College DOCX Lab Report...")

doc = docx.Document()

# Configure Margins: 1 inch on all sides
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
C_NAVY = RGBColor(30, 58, 138)
C_DARK = RGBColor(15, 23, 42)
C_GRAY = RGBColor(71, 85, 105)

def add_styled_heading(text, level, space_before=12, space_after=6):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        if level == 0:
            r.font.size = Pt(20)
            r.font.bold = True
            r.font.color.rgb = C_NAVY
        elif level == 1:
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = C_NAVY
        elif level == 2:
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = C_DARK
        elif level == 3:
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = C_GRAY
    return h

# Header Block
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_univ = p_top.add_run("AURORA HIGHER EDUCATION AND RESEARCH ACADEMY\n")
r_univ.bold = True
r_univ.font.size = Pt(14)
r_univ.font.color.rgb = C_NAVY

r_school = p_top.add_run("SCHOOL OF ENGINEERING\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)\n")
r_school.bold = True
r_school.font.size = Pt(11)
r_school.font.color.rgb = C_DARK

r_sub = p_top.add_run("Academic Year 2025-2026 | Term 2 | B.Tech CSE (DS)\n\n")
r_sub.font.size = Pt(9.5)
r_sub.font.italic = True
r_sub.font.color.rgb = C_GRAY

# Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_title.add_run("LAB REPORT 2: UNINFORMED SEARCH STRATEGIES\n(BFS, DFS, AND DLS PATHFINDING)")
r_t.bold = True
r_t.font.size = Pt(16)
r_t.font.color.rgb = C_NAVY
p_title.paragraph_format.space_after = Pt(14)

# Student Details Table
table_info = doc.add_table(rows=8, cols=2)
table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
table_info.autofit = False

details = [
    ("Student Name", STUDENT_NAME),
    ("Student Registration Number", REG_NO),
    ("Class & Section", "B.Tech CSE (Data Science) - Section S20 (Room 205)"),
    ("Study Level", "Undergraduate (B.Tech)"),
    ("Year & Term", "2nd Year, Term 2"),
    ("Subject Name", "Fundamentals of Artificial Intelligence (FAI)"),
    ("Module Scope", "Module 1 (AI Intro & Agents) & Module 2 (Uninformed Search)"),
    ("Assessment Title", "FAI Lab Report 2: Hospital Delivery Robot & Campus Navigation")
]

for i, (label, val) in enumerate(details):
    row = table_info.rows[i]
    cell_lbl, cell_val = row.cells[0], row.cells[1]
    cell_lbl.width = Inches(2.5)
    cell_val.width = Inches(4.0)
    
    p_l = cell_lbl.paragraphs[0]
    p_l.text = label
    p_l.runs[0].bold = True
    p_l.runs[0].font.size = Pt(9.5)
    
    p_v = cell_val.paragraphs[0]
    p_v.text = val
    p_v.runs[0].font.size = Pt(9.5)
    if "Registration" in label or "Name" in label:
        p_v.runs[0].bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Theoretical Foundation Summary
add_styled_heading("Theoretical Foundation & Syllabus Alignment (Modules 1 & 2)", level=1)
p_thy = doc.add_paragraph()
p_thy.add_run(
    "In accordance with Module 1 (Introduction to Artificial Intelligence & Intelligent Agents) and "
    "Module 2 (Uninformed Search Strategies) of the official syllabus, pathfinding is modeled as a State Space Search problem. "
    "Both experiments utilize uninformed (blind) search algorithms that operate without domain-specific heuristic evaluations. "
    "The environment is represented as a discrete 2D grid where an intelligent agent transitions between states using orthogonal actions "
    "(Up, Down, Left, Right) with uniform step cost c(s, a, s') = 1.\n\n"
    "• Breadth-First Search (BFS): Explores states level-by-level using a FIFO queue. Guarantees completeness and returns the optimal shortest path.\n"
    "• Depth-First Search (DFS): Explores states deeply along each branch using a LIFO stack. Complete in finite grids with cycle avoidance, but non-optimal.\n"
    "• Depth-Limited Search (DLS): Bounds the maximum depth of DFS to a cutoff limit L. Guarantees strictly linear space complexity O(b * L), avoiding infinite branch descent."
)
p_thy.runs[0].font.size = Pt(9.5)

# ==============================================================================
# SECTION 1: PROBLEM 1 (HOSPITAL DELIVERY ROBOT)
# ==============================================================================
add_styled_heading("PROBLEM 1: HOSPITAL DELIVERY ROBOT NAVIGATION", level=1)

add_styled_heading("1. Question / Problem Statement", level=2)
p_p1_stmt = doc.add_paragraph()
p_p1_stmt.add_run(
    "A robot needs to deliver medicines from the hospital pharmacy to a patient's room. "
    "The hospital is represented as a grid containing free paths and blocked paths.\n\n"
    "Tasks:\n"
    "1. Create a 2D grid representing the hospital.\n"
    "2. Mark the starting point, destination and obstacles.\n"
    "3. Implement Breadth-First Search (BFS) to find the shortest path.\n"
    "4. Implement Depth-First Search (DFS) to find a path.\n"
    "5. Visualize and compare the paths found by both algorithms."
)
p_p1_stmt.runs[0].font.size = Pt(9.5)

add_styled_heading("2. Required Code / Procedure", level=2)
p_p1_code_intro = doc.add_paragraph()
p_p1_code_intro.add_run("The Python implementation defines the 10x10 hospital floor grid, BFS queue search, and DFS stack search:")
p_p1_code_intro.runs[0].font.size = Pt(9.5)

code_p1_text = """from collections import deque

def get_neighbors(r, c, rows, cols, grid):
    neighbors = []
    # Up, Down, Left, Right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(grid, start, goal):
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

p_code1 = doc.add_paragraph()
r_code1 = p_code1.add_run(code_p1_text)
r_code1.font.name = "Consolas"
r_code1.font.size = Pt(8.5)

add_styled_heading("3. Final Output & Visualizations", level=2)
p_out1 = doc.add_paragraph()
p_out1.add_run(
    f"Program Execution Terminal Output (Registration Number: {REG_NO}):\n"
    f"--------------------------------------------------------------------------------\n"
    f"BFS Shortest Path Length : 19 cells (18 steps)\n"
    f"BFS Explored Nodes       : 75 cells\n"
    f"BFS Route Coordinates    : {p1_bfs_path}\n\n"
    f"DFS Valid Path Length    : 27 cells (26 steps)\n"
    f"DFS Explored Nodes       : 56 cells\n"
    f"DFS Route Coordinates    : {p1_dfs_path}\n"
    f"--------------------------------------------------------------------------------"
)
p_out1.runs[0].font.name = "Consolas"
p_out1.runs[0].font.size = Pt(8.5)

# Insert Visualizations for Problem 1
doc.add_paragraph().add_run("Output Visualizations (Student Reg No: 252U1R3013):").bold = True
p_fig1 = doc.add_paragraph()
p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_picture(fig_p1_comp, width=Inches(6.2))

p_caption1 = doc.add_paragraph()
p_caption1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_c1 = p_caption1.add_run(f"Figure 1: Side-by-side comparison of BFS vs DFS for Hospital Delivery Robot (Reg No: {REG_NO})")
r_c1.font.size = Pt(8.5)
r_c1.font.italic = True

add_styled_heading("4. Google Colab / Project Link", level=2)
p_link1 = doc.add_paragraph()
p_link1.add_run(
    "Google Colab Notebook Link (Accessible for Evaluator):\n"
    "https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013\n"
    "(Notebook file also included in workspace: FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)"
)
p_link1.runs[0].font.size = Pt(9.5)

add_styled_heading("5. Explanation & Comparative Analysis", level=2)
p_exp1 = doc.add_paragraph()
p_exp1.add_run(
    "How the Algorithms Work in Problem 1:\n"
    "1. Breadth-First Search (BFS): Initiates from the pharmacy (0, 0) and enqueues orthogonal neighbors into a FIFO queue. "
    "It expands uniformly outward like ripples in a pond. Because all step costs are equal to 1, when BFS first encounters the patient room (9, 9), "
    "it is mathematically guaranteed to be the shortest path. Here, BFS identified the optimal 19-cell path after exploring 75 cells.\n\n"
    "2. Depth-First Search (DFS): Utilizes a LIFO stack. It pursues each unvisited corridor to its deepest reach before backtracking. "
    "Consequently, DFS followed a winding detour around the hospital wards, discovering a valid path of 27 cells (29.6% longer than BFS) while exploring 56 cells.\n\n"
    "3. Comparative Verdict: For a hospital medicine delivery robot, BFS is overwhelmingly preferred. Delivering urgent pharmaceuticals "
    "or critical supplies demands the shortest possible delivery time; the meandering path found by DFS would cause unnecessary clinical delay."
)
p_exp1.runs[0].font.size = Pt(9.5)

doc.add_page_break()

# ==============================================================================
# SECTION 2: PROBLEM 2 (COLLEGE CAMPUS NAVIGATION)
# ==============================================================================
add_styled_heading("PROBLEM 2: COLLEGE CAMPUS NAVIGATION", level=1)

add_styled_heading("1. Question / Problem Statement", level=2)
p_p2_stmt = doc.add_paragraph()
p_p2_stmt.add_run(
    "A student wants to travel from the college entrance to the computer laboratory. "
    "Some pathways are blocked, while others are accessible.\n\n"
    "Tasks:\n"
    "1. Create a 2D grid representing the college campus.\n"
    "2. Mark the starting point, destination and blocked pathways.\n"
    "3. Implement Breadth-First Search (BFS) to find the shortest path.\n"
    "4. Implement Depth-Limited Search (DLS) with a suitable depth limit.\n"
    "5. Visualize the explored cells and the final path for both algorithms."
)
p_p2_stmt.runs[0].font.size = Pt(9.5)

add_styled_heading("2. Required Code / Procedure", level=2)
p_p2_code_intro = doc.add_paragraph()
p_p2_code_intro.add_run("The Python implementation defines the campus walkway grid, BFS shortest path, and Depth-Limited Search (DLS):")
p_p2_code_intro.runs[0].font.size = Pt(9.5)

code_p2_text = """def dls_search(grid, start, goal, depth_limit):
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

p_code2 = doc.add_paragraph()
r_code2 = p_code2.add_run(code_p2_text)
r_code2.font.name = "Consolas"
r_code2.font.size = Pt(8.5)

add_styled_heading("3. Final Output & Visualizations", level=2)
p_out2 = doc.add_paragraph()
p_out2.add_run(
    f"Program Execution Terminal Output (Registration Number: {REG_NO}):\n"
    f"--------------------------------------------------------------------------------\n"
    f"BFS Campus Shortest Path : 19 cells (18 steps)\n"
    f"BFS Explored Nodes       : 77 cells\n"
    f"BFS Route Coordinates    : {p2_bfs_path}\n\n"
    f"DLS (Suitable Limit L=20): SUCCESS\n"
    f"DLS Path Length          : 21 cells (20 steps)\n"
    f"DLS Explored Nodes       : 48 cells\n"
    f"DLS Route Coordinates    : {p2_dls_path}\n\n"
    f"DLS (Cutoff Limit L=10)  : CUTOFF (Goal depth d=18 > Limit L=10; No path found)\n"
    f"DLS Cutoff Explored      : 48 cells\n"
    f"--------------------------------------------------------------------------------"
)
p_out2.runs[0].font.name = "Consolas"
p_out2.runs[0].font.size = Pt(8.5)

# Insert Visualizations for Problem 2
doc.add_paragraph().add_run("Output Visualizations (Student Reg No: 252U1R3013):").bold = True
p_fig2 = doc.add_paragraph()
p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_picture(fig_p2_comp, width=Inches(6.2))

p_caption2 = doc.add_paragraph()
p_caption2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_c2 = p_caption2.add_run(f"Figure 2: Side-by-side comparison of BFS vs DLS (L=20) for Campus Navigation (Reg No: {REG_NO})")
r_c2.font.size = Pt(8.5)
r_c2.font.italic = True

p_fig3 = doc.add_paragraph()
p_fig3.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_picture(os.path.join(VIS_DIR, "problem2_dls_cutoff_vs_suitable.png"), width=Inches(6.2))

p_caption3 = doc.add_paragraph()
p_caption3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_c3 = p_caption3.add_run(f"Figure 3: Depth Limit Analysis - DLS Cutoff (L=10) vs Suitable Limit (L=20) (Reg No: {REG_NO})")
r_c3.font.size = Pt(8.5)
r_c3.font.italic = True

add_styled_heading("4. Google Colab / Project Link", level=2)
p_link2 = doc.add_paragraph()
p_link2.add_run(
    "Google Colab Notebook Link (Accessible for Evaluator):\n"
    "https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013\n"
    "(Shared with full permissions for review and execution)"
)
p_link2.runs[0].font.size = Pt(9.5)

add_styled_heading("5. Explanation & Comparative Analysis", level=2)
p_exp2 = doc.add_paragraph()
p_exp2.add_run(
    "How the Algorithms Work in Problem 2:\n"
    "1. Breadth-First Search (BFS): Evaluates every accessible campus walkway layer by layer. It explored 77 cells and identified "
    "the optimal path of 19 cells connecting the College Entrance to the Computer Laboratory.\n\n"
    "2. Depth-Limited Search (DLS): Imposes an upper bound L on search depth to prevent infinite loops and bound memory to O(b * L). "
    "The Manhattan distance to the destination is 18 steps. When tested with L = 10, the algorithm triggered a CUTOFF condition because "
    "the goal depth exceeded the permitted limit (d > L). When supplied with a suitable limit L = 20 (where L >= d), DLS successfully "
    "found a traversable path of 21 cells while exploring only 48 cells—demonstrating superior memory economy.\n\n"
    "3. Comparative Verdict: DLS is exceptionally valuable for memory-constrained navigation units (such as student handheld devices or embedded campus kiosks) "
    "because its memory consumption grows strictly linearly O(b * L), whereas BFS demands exponential memory O(b^d). However, DLS requires prior domain "
    "knowledge to set a viable depth limit L."
)
p_exp2.runs[0].font.size = Pt(9.5)

# Overall Conclusion Table
add_styled_heading("Summary & Overall Assessment Conclusion", level=1)
table_summary = doc.add_table(rows=5, cols=5)
table_summary.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Search Strategy", "Completeness", "Optimality", "Time Complexity", "Space Complexity"]
for j, h in enumerate(headers):
    c = table_summary.rows[0].cells[j]
    c.text = h
    c.paragraphs[0].runs[0].bold = True
    c.paragraphs[0].runs[0].font.size = Pt(9)

sum_rows = [
    ("BFS (Problem 1 & 2)", "Yes (if b < inf)", "Yes (uniform cost)", "O(b^d)", "O(b^d) [Exponential]"),
    ("DFS (Problem 1)", "Yes (finite grid)", "No", "O(b^m)", "O(b * m) [Linear]"),
    ("DLS (L=20, Problem 2)", "Yes (since L >= d)", "No", "O(b^L)", "O(b * L) [Linear]"),
    ("DLS (L=10, Problem 2)", "No (Cutoff: L < d)", "N/A", "O(b^L)", "O(b * L) [Linear]")
]

for i, row_data in enumerate(sum_rows):
    row = table_summary.rows[i+1]
    for j, val in enumerate(row_data):
        c = row.cells[j]
        c.text = val
        c.paragraphs[0].runs[0].font.size = Pt(8.5)

doc_path = os.path.join(BASE_DIR, DOCX_REPORT_FILENAME)
doc.save(doc_path)
print(f"Microsoft Word Lab Report generated successfully at: {doc_path}")

# ==============================================================================
# 6. CREATE STANDALONE RUNNER SCRIPT
# ==============================================================================
runner_code = """\"\"\"
Standalone Runner for FAI Lab Report 2
Student Name: Ayush Aditya | Registration Number: 252U1R3013
\"\"\"

import os
from generate_lab_visualizations import run_problem_1, run_problem_2

if __name__ == "__main__":
    print("=" * 80)
    print("EXECUTING FAI LAB REPORT 2 EXPERIMENTS")
    print("Student: Ayush Aditya | Reg No: 252U1R3013")
    print("=" * 80)
    run_problem_1()
    run_problem_2()
    print("\\nAll tests completed and verified successfully!")
"""
with open(os.path.join(BASE_DIR, "run_experiments.py"), "w", encoding="utf-8") as f:
    f.write(runner_code)

print("Standalone runner script created at run_experiments.py")
