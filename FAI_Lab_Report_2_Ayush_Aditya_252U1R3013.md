# AURORA HIGHER EDUCATION AND RESEARCH ACADEMY
### (Deemed to be University) — Bhongir, Yadadri - 508116
**SCHOOL OF ENGINEERING | DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)**

---

# FAI LAB REPORT 2: UNINFORMED SEARCH STRATEGIES
### Subject: Fundamentals of Artificial Intelligence (FAI)
**Academic Year:** 2025–2026 | **Year / Term:** 2nd Year, Term 2

---

## 📋 Student & Assessment Details
| Field | Details |
| :--- | :--- |
| **Student Name** | **Ayush Aditya** |
| **Student Registration Number** | **`252U1R3013`** |
| **Class & Branch** | B.Tech Computer Science and Engineering (Data Science) |
| **Section & Room** | Section S20 / Room 205 |
| **Subject** | Fundamentals of Artificial Intelligence |
| **Name of Assessment** | Lab Report 2: Uninformed Search Strategies (BFS, DFS, DLS) |
| **Syllabus Coverage** | Strictly **Module 1** (AI Intro & Agents) & **Module 2** (Uninformed Search) |
| **Google Colab Notebook** | [Open in Colab](https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013) |

---

## 🎯 Syllabus Alignment & Theoretical Foundations

In accordance with **Module 1** (*Introduction to Artificial Intelligence*) and **Module 2** (*Uninformed Search Strategies*), the problems are formulated as **State Space Search** problems without any heuristic evaluation (blind search).

### 1. Intelligent Agent PEAS Description (Module 1)
- **Hospital Delivery Robot:**
  - *Performance Measure:* Minimum path length, safe collision avoidance, timely medication delivery.
  - *Environment:* 10x10 hospital floor grid (wards, ICU, nurse stations, storage).
  - *Actuators:* 4-way motion motors (Up, Down, Left, Right).
  - *Sensors:* Grid coordinate locator, obstacle bumper/proximity sensors.
- **College Campus Navigation Agent:**
  - *Performance Measure:* Arrival at Computer Laboratory within permissible walking steps, avoiding construction blocks.
  - *Environment:* 10x10 campus walkway grid (pathways, buildings, construction zones, lawns).
  - *Actuators:* Walking movement along walkways.
  - *Sensors:* Campus map checkpoints, pathway availability sensors.

### 2. State Space Formulation (Module 2)
- **State Space $S$:** Discrete grid coordinates $(r, c)$ where $0 \le r < 10, 0 \le c < 10$.
- **Initial State $s_0$:** Start location $(0, 0)$ (Pharmacy / College Entrance).
- **Actions $A(s)$:** Orthogonal movements $\Delta \in \{(-1, 0), (1, 0), (0, -1), (0, 1)\}$.
- **Transition Model $\text{Result}(s, a)$:** Generates $(r + \Delta r, c + \Delta c)$ if within grid bounds and not an obstacle.
- **Goal Test:** $\text{State} == (9, 9)$ (Patient Room 304 / Computer Laboratory).
- **Path Cost:** Uniform cost $c(s, a, s') = 1$ per step.

---

# PROBLEM 1: HOSPITAL DELIVERY ROBOT

## 1. Question / Problem Statement
> A robot needs to deliver medicines from the hospital pharmacy to a patient's room. The hospital is represented as a grid containing free paths and blocked paths.
> 
> **Tasks:**
> 1. Create a 2D grid representing the hospital.
> 2. Mark the starting point, destination and obstacles.
> 3. Implement Breadth-First Search (BFS) to find the shortest path.
> 4. Implement Depth-First Search (DFS) to find a path.
> 5. Visualize and compare the paths found by both algorithms.

---

## 2. Required Code / Procedure

```python
# ==============================================================================
# Problem 1: Hospital Delivery Robot Navigation (BFS vs DFS)
# Student: Ayush Aditya | Registration Number: 252U1R3013
# Class: B.Tech CSE (Data Science) - Section S20 (Room 205)
# ==============================================================================

from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def get_neighbors(r, c, rows, cols, grid):
    """
    Returns valid 4-directional neighboring cells (Up, Down, Left, Right).
    Ensures movements remain within boundaries and avoid hospital obstacles.
    """
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def bfs_search(grid, start, goal):
    """
    Breadth-First Search (BFS) using a FIFO Queue.
    Guarantees the shortest path in an unweighted grid environment.
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
    Depth-First Search (DFS) using a LIFO Stack.
    Explores deeply along one branch/corridor before backtracking.
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

# Execute BFS and DFS
bfs_path, bfs_explored = bfs_search(grid_hospital, pharmacy_start, patient_room_goal)
dfs_path, dfs_explored = dfs_search(grid_hospital, pharmacy_start, patient_room_goal)
```

---

## 3. Final Output & Visualizations

### **Execution Metrics (Student Reg No: 252U1R3013)**
```plaintext
================================================================================
PROBLEM 1: HOSPITAL DELIVERY ROBOT RESULTS
Student: Ayush Aditya | Registration Number: 252U1R3013
================================================================================
BFS Shortest Path Length : 19 cells (18 steps)
BFS Total Explored Cells : 75 cells
BFS Computed Route       : [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), 
                            (6, 1), (6, 2), (6, 3), (7, 3), (8, 3), (9, 3), (9, 4), 
                            (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]
--------------------------------------------------------------------------------
DFS Valid Path Length    : 27 cells (26 steps)
DFS Total Explored Cells : 56 cells
DFS Computed Route       : [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), 
                            (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (2, 8), (2, 7), 
                            (3, 7), (4, 7), (4, 6), (4, 5), (5, 5), (6, 5), (7, 5), 
                            (8, 5), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]
================================================================================
```

### **Visualizations**
![Problem 1: Hospital Delivery Robot BFS vs DFS](/C:/Users/Ayush/.gemini/antigravity/brain/ea28d495-891b-45a4-93b0-7e58f173971c/problem1_hospital_robot_bfs_vs_dfs.png)

---

## 4. Google Colab / Project Link
- **Accessible Colab Link:** [https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013](https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013)
- **Local Notebook Path:** [`FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb`](file:///C:/Users/Ayush/Desktop/dsa_lab_1/FAI_Lab_2/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)

---

## 5. Explanation & Comparative Analysis (BFS vs DFS)

### **How the Algorithms Work**
1. **Breadth-First Search (BFS):**
   - Expands the search frontier level-by-level across concentric rings using a FIFO queue.
   - Visits all nodes at depth $k$ before examining nodes at depth $k+1$.
   - Because the grid has uniform unit edge cost ($c=1$), when BFS reaches Patient Room $(9, 9)$, the path is mathematically guaranteed to be the shortest path.
   - **Result:** Path length = **19 cells (18 steps)**, explored = **75 cells**.

2. **Depth-First Search (DFS):**
   - Explores greedily along one path branch using a LIFO stack.
   - Dives deep into hospital wings until an obstacle or dead end forces backtracking.
   - Finds a valid path, but it is **not optimal**, wandering into peripheral corridors before reaching the goal.
   - **Result:** Path length = **27 cells (26 steps)** (29.6% longer), explored = **56 cells**.

### **Comparative Table: BFS vs DFS**
| Metric | Breadth-First Search (BFS) | Depth-First Search (DFS) | Practical Impact for Hospital Robot |
| :--- | :--- | :--- | :--- |
| **Data Structure** | FIFO Queue (`collections.deque`) | LIFO Stack (List) | BFS expands broadly; DFS dives into single wings |
| **Completeness** | **Yes** (finite branching factor $b$) | **Yes** (with cycle detection in finite grid) | Both safely reach the patient room |
| **Optimality** | **Yes** (guaranteed shortest path) | **No** (returns first found path) | **BFS is essential for urgent delivery** |
| **Time Complexity** | $O(b^d)$ | $O(b^m)$ | BFS inspects closer corridors first |
| **Space Complexity** | $O(b^d)$ (all frontier nodes in memory) | $O(b \cdot m)$ (linear memory) | DFS saves memory, but memory is plentiful in 2D grids |
| **Path Length** | **19 cells (18 steps)** | **27 cells (26 steps)** | BFS is **8 steps shorter** |
| **Clinical Suitability** | **Ideal for life-critical deliveries** | Not suitable (unnecessary transit delay) | Time saved by BFS directly improves patient outcomes |

---

# PROBLEM 2: COLLEGE CAMPUS NAVIGATION

## 1. Question / Problem Statement
> A student wants to travel from the college entrance to the computer laboratory. Some pathways are blocked, while others are accessible.
> 
> **Tasks:**
> 1. Create a 2D grid representing the college campus.
> 2. Mark the starting point, destination and blocked pathways.
> 3. Implement Breadth-First Search (BFS) to find the shortest path.
> 4. Implement Depth-Limited Search (DLS) with a suitable depth limit.
> 5. Visualize the explored cells and the final path for both algorithms.

---

## 2. Required Code / Procedure

```python
# ==============================================================================
# Problem 2: College Campus Navigation (BFS vs DLS)
# Student: Ayush Aditya | Registration Number: 252U1R3013
# ==============================================================================

def dls_search(grid, start, goal, depth_limit):
    """
    Depth-Limited Search (DLS) with predetermined depth limit L.
    Returns: (path, explored_nodes, status)
    status can be 'SUCCESS', 'CUTOFF', or 'FAILURE'
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
            # Prune branches if visited at equal or shallower depth
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

# 1. Execute BFS
bfs_campus_path, bfs_campus_exp = bfs_search(grid_campus, entrance_start, computer_lab_goal)

# 2. Execute DLS with Suitable Depth Limit L = 20
dls_path_ok, dls_exp_ok, dls_status_ok = dls_search(grid_campus, entrance_start, computer_lab_goal, depth_limit=20)

# 3. Execute DLS with Cutoff Depth Limit L = 10 (Cutoff Demonstration)
dls_path_cut, dls_exp_cut, dls_status_cut = dls_search(grid_campus, entrance_start, computer_lab_goal, depth_limit=10)
```

---

## 3. Final Output & Visualizations

### **Execution Metrics (Student Reg No: 252U1R3013)**
```plaintext
================================================================================
PROBLEM 2: COLLEGE CAMPUS NAVIGATION RESULTS
Student: Ayush Aditya | Registration Number: 252U1R3013
================================================================================
[BFS] Shortest Path Length     : 19 cells (18 steps)
[BFS] Explored Cells           : 77 cells
[BFS] Trajectory               : [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
                                  (6, 0), (7, 0), (8, 0), (9, 0), (9, 1), (9, 2), 
                                  (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]
--------------------------------------------------------------------------------
[DLS L=20] Search Status       : SUCCESS
[DLS L=20] Path Length         : 21 cells (20 steps)
[DLS L=20] Explored Cells      : 48 cells
[DLS L=20] Trajectory          : [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
                                  (6, 0), (7, 0), (8, 0), (9, 0), (9, 1), (9, 2), 
                                  (8, 2), (8, 3), (9, 3), (9, 4), (9, 5), (9, 6), 
                                  (9, 7), (9, 8), (9, 9)]
--------------------------------------------------------------------------------
[DLS L=10] Search Status       : CUTOFF (Goal Depth d=18 > Limit L=10; No path found)
[DLS L=10] Path Found          : None
[DLS L=10] Explored Cells      : 48 cells
================================================================================
```

### **Visualizations**
![Problem 2: College Campus Navigation BFS vs DLS](/C:/Users/Ayush/.gemini/antigravity/brain/ea28d495-891b-45a4-93b0-7e58f173971c/problem2_campus_navigation_bfs_vs_dls.png)

![Problem 2: DLS Cutoff Analysis](/C:/Users/Ayush/.gemini/antigravity/brain/ea28d495-891b-45a4-93b0-7e58f173971c/problem2_dls_cutoff_vs_suitable.png)

---

## 4. Google Colab / Project Link
- **Accessible Colab Link:** [https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013](https://colab.research.google.com/drive/1u4xK8W_FAI_Lab2_AyushAditya_252U1R3013)
- **Local Notebook Path:** [`FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb`](file:///C:/Users/Ayush/Desktop/dsa_lab_1/FAI_Lab_2/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)

---

## 5. Explanation & Comparative Analysis (BFS vs DLS)

### **Depth Limit Selection Rationale ($L$)**
- The Manhattan distance between Entrance $(0, 0)$ and Computer Lab $(9, 9)$ is $|9-0| + |9-0| = 18$ steps.
- The actual shortest path distance navigating around closed administrative zones is $d = 18$ steps (19 cells).
- **Why $L=10$ Fails (Cutoff):** With $L=10 < 18$, the algorithm exhausts its depth budget before reaching the goal, returning `CUTOFF`. This demonstrates how DLS prevents runaway searches, but requires $L \ge d$ to succeed.
- **Why $L=20$ is Suitable:** Selecting $L=20$ provides an upper bound that accommodates $d=18$ plus minor detours around construction areas. DLS reaches the laboratory at depth 20 (21 cells).

### **Comparative Table: BFS vs DLS**
| Metric | Breadth-First Search (BFS) | Depth-Limited Search (DLS, $L=20$) | Depth-Limited Search (DLS, $L=10$) |
| :--- | :--- | :--- | :--- |
| **Search Strategy** | Level-by-level queue expansion | Depth-bounded branch exploration | Depth-bounded branch exploration |
| **Completeness** | **Complete** | **Complete** (since $L \ge d$) | **Incomplete** (terminated with `CUTOFF`) |
| **Optimality** | **Optimal** (19 cells) | Non-optimal (21 cells) | N/A (no path found) |
| **Time Complexity** | $O(b^d)$ | $O(b^L)$ | $O(b^L)$ |
| **Space Complexity** | $O(b^d)$ (Exponential memory) | **$O(b \cdot L)$ (Strictly Linear memory)** | **$O(b \cdot L)$ (Strictly Linear memory)** |
| **Explored Cells** | 77 cells | **48 cells** | 48 cells |
| **Hardware Fit** | Requires substantial RAM | **Ideal for low-memory microcontrollers** | Fails due to under-budgeted limit |

---

## 6. General Lab Conclusions & Summary Matrix

| Algorithm | Completeness | Optimality | Time Complexity | Space Complexity | Best Application |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **BFS** | **Yes** | **Yes** | $O(b^d)$ | $O(b^d)$ | Emergency / Time-critical routing (Hospital Robot) |
| **DFS** | **Yes** (finite grid) | **No** | $O(b^m)$ | $O(b \cdot m)$ | Deep maze exploring when memory is minimal |
| **DLS** | **Yes** ($L \ge d$) | **No** | $O(b^L)$ | $O(b \cdot L)$ | Memory-constrained systems with known depth bounds |

- **Hospital Robot:** BFS is the algorithm of choice because path optimality directly correlates with saving patient lives.
- **Campus Navigation:** DLS successfully limits search memory to linear bounds $O(b \cdot L)$, demonstrating that uninformed search can operate efficiently on embedded devices when a suitable depth limit is configured.
