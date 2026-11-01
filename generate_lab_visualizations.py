"""
FAI Lab Report 2: Uninformed Search Algorithms
Problem 1: Hospital Delivery Robot (BFS vs DFS)
Problem 2: College Campus Navigation (BFS vs DLS)

Author: Ayush Aditya
Registration Number: 252U1R3013
Class: B.Tech CSE (Data Science), S20 / Room 205
Course: Fundamentals of Artificial Intelligence (Modules 1 & 2)
"""

import os
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Create output directories for plots
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualizations")
os.makedirs(OUTPUT_DIR, exist_ok=True)

STUDENT_NAME = "Ayush Aditya"
REG_NO = "252U1R3013"
CLASS_INFO = "B.Tech CSE (Data Science) - S20 (Room 205)"

# ==============================================================================
# 1. CORE SEARCH ALGORITHMS (MODULE 2: UNINFORMED SEARCH STRATEGIES)
# ==============================================================================

def get_neighbors(r, c, rows, cols, grid):
    """
    Returns valid 4-directional neighboring cells (Up, Down, Left, Right).
    Ensures movements stay within boundaries and avoid obstacles.
    """
    neighbors = []
    # Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(grid, start, goal):
    """
    Breadth-First Search (BFS)
    - Data Structure: FIFO Queue
    - Completeness: Yes (finite branching factor)
    - Optimality: Yes (unweighted step cost)
    - Time Complexity: O(b^d)
    - Space Complexity: O(b^d)
    """
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
                
    # Path reconstruction
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
    """
    Depth-First Search (DFS)
    - Data Structure: LIFO Stack
    - Completeness: Yes (finite state space with cycle detection)
    - Optimality: No
    - Time Complexity: O(b^m)
    - Space Complexity: O(b*m)
    """
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
    """
    Depth-Limited Search (DLS)
    - Strategy: Depth-First Search with predetermined cutoff depth L
    - Completeness: Incomplete if depth_limit < d; Complete if depth_limit >= d
    - Optimality: No
    - Space Complexity: O(b * l)
    - Time Complexity: O(b^l)
    """
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
# 2. VISUALIZATION ENGINE (WITH REGISTRATION NUMBER 252U1R3013)
# ==============================================================================

def plot_single_search(ax, grid, path, explored, start, goal, title, metrics):
    """
    Plots a professional grid visualization of the search algorithm.
    """
    rows, cols = len(grid), len(grid[0])
    
    # 0 = free, 1 = obstacle, 2 = explored, 3 = path
    display_matrix = np.zeros((rows, cols))
    
    # Obstacles
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                display_matrix[r, c] = 1
                
    # Explored cells
    if explored:
        for r, c in explored:
            if display_matrix[r, c] != 1 and (r, c) != start and (r, c) != goal:
                display_matrix[r, c] = 2
                
    # Path
    if path:
        for r, c in path:
            if (r, c) != start and (r, c) != goal:
                display_matrix[r, c] = 3
                
    # Base background drawing
    for r in range(rows):
        for c in range(cols):
            val = display_matrix[r, c]
            if (r, c) == start:
                color = "#10B981"  # Emerald Green
            elif (r, c) == goal:
                color = "#EF4444"  # Crimson Red
            elif val == 1:
                color = "#1E293B"  # Dark Slate Obstacle
            elif val == 3:
                color = "#F59E0B"  # Amber Path
            elif val == 2:
                color = "#BAE6FD"  # Soft Sky Blue Explored
            else:
                color = "#FFFFFF"  # White Free Cell
                
            rect = plt.Rectangle((c, r), 1, 1, facecolor=color, edgecolor="#CBD5E1", linewidth=0.8)
            ax.add_patch(rect)
            
    # Draw path connecting line
    if path and len(path) > 1:
        path_x = [c + 0.5 for _, c in path]
        path_y = [r + 0.5 for r, _ in path]
        ax.plot(path_x, path_y, color="#B45309", linewidth=2.5, linestyle="--", zorder=4)
        
    # Annotate Start and Goal
    ax.text(start[1] + 0.5, start[0] + 0.5, "START\n(S)", color="white", weight="bold",
            fontsize=8, ha="center", va="center", zorder=5)
    ax.text(goal[1] + 0.5, goal[0] + 0.5, "GOAL\n(G)", color="white", weight="bold",
            fontsize=8, ha="center", va="center", zorder=5)
            
    # Configure axes
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)  # Invert so (0,0) is top-left
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.set_xticklabels([str(i) for i in range(cols + 1)], fontsize=8)
    ax.set_yticklabels([str(i) for i in range(rows + 1)], fontsize=8)
    ax.grid(color="#94A3B8", linestyle="-", linewidth=0.5, alpha=0.5)
    ax.set_aspect("equal")
    
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12, color="#0F172A")
    
    # Metrics textbox inside subplot
    info_box = (
        f"Status: {metrics.get('Status', 'SUCCESS')}\n"
        f"Path Length: {metrics.get('Path Length', 'N/A')} cells\n"
        f"Nodes Explored: {metrics.get('Nodes Explored', len(explored))}\n"
        f"Completeness: {metrics.get('Completeness', 'Yes')}\n"
        f"Optimality: {metrics.get('Optimality', 'N/A')}\n"
        f"Reg No: {REG_NO}"
    )
    ax.text(0.03, 0.03, info_box, transform=ax.transAxes, fontsize=8,
            verticalalignment="bottom", horizontalalignment="left",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#64748B", alpha=0.92, linewidth=1),
            zorder=6)

def generate_comparison_plot(grid, start, goal, p1_data, p2_data, suptitle, filename, labels):
    """
    Creates a dual-panel comparison figure with full annotations, legends, and student details.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=200)
    
    # Main Header with Student Credentials
    fig.suptitle(
        f"{suptitle}\n"
        f"Student: {STUDENT_NAME}  |  Reg. No: {REG_NO}  |  Class: {CLASS_INFO}",
        fontsize=13, fontweight="bold", color="#1E293B", y=0.98
    )
    
    plot_single_search(ax1, grid, p1_data["path"], p1_data["explored"], start, goal, labels[0], p1_data["metrics"])
    plot_single_search(ax2, grid, p2_data["path"], p2_data["explored"], start, goal, labels[1], p2_data["metrics"])
    
    # Global Legend
    legend_elements = [
        mpatches.Patch(facecolor="#10B981", edgecolor="#059669", label="Start Location"),
        mpatches.Patch(facecolor="#EF4444", edgecolor="#DC2626", label="Goal Destination"),
        mpatches.Patch(facecolor="#1E293B", edgecolor="#0F172A", label="Obstacles / Closed Zones"),
        mpatches.Patch(facecolor="#BAE6FD", edgecolor="#38BDF8", label="Explored Cells (Closed Set)"),
        mpatches.Patch(facecolor="#F59E0B", edgecolor="#D97706", label="Final Computed Path"),
        plt.Line2D([0], [0], color="#B45309", linestyle="--", linewidth=2, label="Path Trajectory")
    ]
    
    fig.legend(handles=legend_elements, loc="lower center", ncol=6, fontsize=9,
               frameon=True, facecolor="#F1F5F9", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, 0.02))
               
    plt.tight_layout(rect=[0, 0.07, 1, 0.94])
    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Saved figure: {save_path}")
    return save_path

# ==============================================================================
# 3. PROBLEM 1 EXECUTION: HOSPITAL DELIVERY ROBOT
# ==============================================================================

def run_problem_1():
    print("=" * 80)
    print("PROBLEM 1: HOSPITAL DELIVERY ROBOT (BFS vs DFS)")
    print(f"Student: {STUDENT_NAME} | Reg. No: {REG_NO} | {CLASS_INFO}")
    print("=" * 80)
    
    # 10x10 Hospital Floor Grid
    grid_hosp = [[0]*10 for _ in range(10)]
    
    # Realistic Hospital Obstacles (ICU wards, X-ray labs, nurses' station, storage)
    obstacles = [
        (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
        (7, 2), (8, 2), (9, 2),
        (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
        (1, 6), (2, 6), (3, 6), (5, 6), (6, 6), (7, 6), (8, 6),
        (3, 8), (4, 8), (5, 8), (7, 8), (8, 8)
    ]
    for r, c in obstacles:
        grid_hosp[r][c] = 1
        
    start_pos = (0, 0)   # Hospital Pharmacy
    goal_pos = (9, 9)    # Patient Room 304
    
    # Execute BFS
    bfs_path, bfs_exp = bfs_search(grid_hosp, start_pos, goal_pos)
    bfs_metrics = {
        "Status": "SUCCESS (Optimal Path Found)",
        "Path Length": len(bfs_path) if bfs_path else 0,
        "Nodes Explored": len(bfs_exp),
        "Completeness": "Complete",
        "Optimality": "Optimal (Shortest Path)"
    }
    
    # Execute DFS
    dfs_path, dfs_exp = dfs_search(grid_hosp, start_pos, goal_pos)
    dfs_metrics = {
        "Status": "SUCCESS (Valid Path Found)",
        "Path Length": len(dfs_path) if dfs_path else 0,
        "Nodes Explored": len(dfs_exp),
        "Completeness": "Complete (Finite Grid)",
        "Optimality": "Non-Optimal"
    }
    
    print(f"\n[BFS Results]")
    print(f"Path Length: {len(bfs_path)} cells | Nodes Explored: {len(bfs_exp)}")
    print(f"Path: {bfs_path}")
    
    print(f"\n[DFS Results]")
    print(f"Path Length: {len(dfs_path)} cells | Nodes Explored: {len(dfs_exp)}")
    print(f"Path: {dfs_path}")
    
    # Comparison Data
    p1_data = {"path": bfs_path, "explored": bfs_exp, "metrics": bfs_metrics}
    p2_data = {"path": dfs_path, "explored": dfs_exp, "metrics": dfs_metrics}
    
    labels = [
        f"Breadth-First Search (BFS)\nPharmacy (0,0) -> Room (9,9)",
        f"Depth-First Search (DFS)\nPharmacy (0,0) -> Room (9,9)"
    ]
    
    fig_file = generate_comparison_plot(
        grid_hosp, start_pos, goal_pos, p1_data, p2_data,
        "Problem 1: Hospital Delivery Robot Navigation (Pharmacy to Patient Room)",
        "problem1_hospital_robot_bfs_vs_dfs.png", labels
    )
    
    return {
        "grid": grid_hosp, "start": start_pos, "goal": goal_pos,
        "bfs_path": bfs_path, "bfs_exp": bfs_exp,
        "dfs_path": dfs_path, "dfs_exp": dfs_exp,
        "fig_file": fig_file
    }

# ==============================================================================
# 4. PROBLEM 2 EXECUTION: COLLEGE CAMPUS NAVIGATION
# ==============================================================================

def run_problem_2():
    print("\n" + "=" * 80)
    print("PROBLEM 2: COLLEGE CAMPUS NAVIGATION (BFS vs DLS)")
    print(f"Student: {STUDENT_NAME} | Reg. No: {REG_NO} | {CLASS_INFO}")
    print("=" * 80)
    
    # 10x10 Campus Grid
    grid_campus = [[0]*10 for _ in range(10)]
    
    # Blocked Pathways & Campus Buildings
    campus_obstacles = [
        (1, 2), (2, 2), (3, 2), (4, 2),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
        (6, 1), (7, 1), (8, 1),
        (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
        (1, 8), (2, 8), (3, 8), (5, 8), (6, 8), (7, 8)
    ]
    for r, c in campus_obstacles:
        grid_campus[r][c] = 1
        
    start_pos = (0, 0)   # College Entrance
    goal_pos = (9, 9)    # Computer Laboratory
    
    # 1. Execute BFS
    bfs_path, bfs_exp = bfs_search(grid_campus, start_pos, goal_pos)
    bfs_metrics = {
        "Status": "SUCCESS (Optimal Path Found)",
        "Path Length": len(bfs_path) if bfs_path else 0,
        "Nodes Explored": len(bfs_exp),
        "Completeness": "Complete",
        "Optimality": "Optimal (Shortest Path)"
    }
    
    # 2. Execute DLS with Depth Limit = 20 (Suitable Depth Limit >= d)
    dls_path, dls_exp, dls_status = dls_search(grid_campus, start_pos, goal_pos, depth_limit=20)
    dls_metrics = {
        "Status": f"{dls_status} (Depth Limit L=20)",
        "Path Length": len(dls_path) if dls_path else 0,
        "Nodes Explored": len(dls_exp),
        "Completeness": "Complete (since L >= d)",
        "Optimality": "Non-Optimal"
    }
    
    # 3. Also test DLS with Cutoff Depth Limit = 10 for demonstration
    dls_cut_path, dls_cut_exp, dls_cut_status = dls_search(grid_campus, start_pos, goal_pos, depth_limit=10)
    
    print(f"\n[BFS Campus Results]")
    print(f"Path Length: {len(bfs_path)} cells | Nodes Explored: {len(bfs_exp)}")
    print(f"Path: {bfs_path}")
    
    print(f"\n[DLS Campus Results (Limit = 20)]")
    print(f"Status: {dls_status} | Path Length: {len(dls_path) if dls_path else 0} | Nodes Explored: {len(dls_exp)}")
    print(f"Path: {dls_path}")
    
    print(f"\n[DLS Demonstration (Limit = 10 - Sub-optimal cutoff)]")
    print(f"Status: {dls_cut_status} | Path: {dls_cut_path} | Nodes Explored: {len(dls_cut_exp)}")
    
    p1_data = {"path": bfs_path, "explored": bfs_exp, "metrics": bfs_metrics}
    p2_data = {"path": dls_path, "explored": dls_exp, "metrics": dls_metrics}
    
    labels = [
        f"Breadth-First Search (BFS)\nCollege Entrance (0,0) -> Computer Lab (9,9)",
        f"Depth-Limited Search (DLS, Limit=20)\nCollege Entrance (0,0) -> Computer Lab (9,9)"
    ]
    
    fig_file = generate_comparison_plot(
        grid_campus, start_pos, goal_pos, p1_data, p2_data,
        "Problem 2: College Campus Navigation (Entrance to Computer Laboratory)",
        "problem2_campus_navigation_bfs_vs_dls.png", labels
    )
    
    # Generate Cutoff Comparison plot to clearly illustrate cutoff vs success
    p_cut_data = {
        "path": dls_cut_path, "explored": dls_cut_exp,
        "metrics": {
            "Status": "CUTOFF (Limit L=10 < d)",
            "Path Length": 0,
            "Nodes Explored": len(dls_cut_exp),
            "Completeness": "Incomplete (L < d)",
            "Optimality": "N/A"
        }
    }
    cutoff_labels = [
        f"DLS with Cutoff Limit (L=10)\nGoal Not Reachable (Limit Exceeded)",
        f"DLS with Suitable Limit (L=20)\nGoal Successfully Reached"
    ]
    fig_cutoff = generate_comparison_plot(
        grid_campus, start_pos, goal_pos, p_cut_data, p2_data,
        "Problem 2 Analysis: Depth-Limited Search (DLS) Cutoff (L=10) vs Suitable Limit (L=20)",
        "problem2_dls_cutoff_vs_suitable.png", cutoff_labels
    )
    
    return {
        "grid": grid_campus, "start": start_pos, "goal": goal_pos,
        "bfs_path": bfs_path, "bfs_exp": bfs_exp,
        "dls_path": dls_path, "dls_exp": dls_exp,
        "fig_file": fig_file, "fig_cutoff": fig_cutoff
    }

if __name__ == "__main__":
    res1 = run_problem_1()
    res2 = run_problem_2()
    print("\n" + "=" * 80)
    print("ALL TESTS AND VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print(f"Verified Student Reg. No: {REG_NO}")
    print("=" * 80)
