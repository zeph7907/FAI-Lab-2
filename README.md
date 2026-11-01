# Fundamentals of Artificial Intelligence (FAI) - Lab Report 2
## Uninformed Search Strategies (BFS, DFS, and DLS)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/zeph7907/FAI-Lab-2)


### Student Credentials
- **Student Name:** Ayush Aditya
- **Registration Number:** **`252U1R3013`**
- **Class / Program:** B.Tech Computer Science and Engineering (Data Science)
- **Section & Room:** Section S20 / Room 205
- **Year & Term:** 2nd Year, Term 2
- **Institution:** Aurora Higher Education and Research Academy (Deemed to be University)
- **Subject:** Fundamentals of Artificial Intelligence (FAI)
- **Course Code / Type:** Lab Report 2 (Week 2 Laboratory)
- **Syllabus Coverage:** Strictly restricted to **Module 1** (Introduction to AI & Intelligent Agents) and **Module 2** (Uninformed Search Strategies: State Space Search, BFS, DFS, DLS).

---

## 📋 Table of Contents
1. [Overview & Syllabus Mapping](#overview--syllabus-mapping)
2. [Problem 1: Hospital Delivery Robot Navigation](#problem-1-hospital-delivery-robot-navigation)
3. [Problem 2: College Campus Navigation](#problem-2-college-campus-navigation)
4. [Search Algorithm Complexities & Comparisons](#search-algorithm-complexities--comparisons)
5. [Directory Structure](#directory-structure)
6. [How to Run (Google Colab & Local Machine)](#how-to-run-google-colab--local-machine)
7. [Visualizations & Verification (Reg No: 252U1R3013)](#visualizations--verification-reg-no-252u1r3013)
8. [Submission Artifacts Checklist](#submission-artifacts-checklist)

---

## 1. Overview & Syllabus Mapping

This laboratory experiment implements, visualizes, and evaluates **Uninformed (Blind) Search Strategies** on discrete 2D grid environments without using heuristic functions, adhering strictly to **Modules 1 & 2** of the FAI curriculum.

### **Module 1: Introduction to Artificial Intelligence & Agents**
- **Intelligent Agent Formulation (PEAS):**
  - **Hospital Delivery Robot:**
    - *Performance Measure:* Shortest travel path, collision-free movement, timely delivery of urgent medicine.
    - *Environment:* 10x10 hospital floor grid (ICU, nurse station, diagnostic labs, patient rooms).
    - *Actuators:* 4-way orthogonal movement motors (Up, Down, Left, Right).
    - *Sensors:* Grid coordinate locator, obstacle bumper/proximity sensors.
  - **College Campus Navigation Agent:**
    - *Performance Measure:* Reach Computer Laboratory within allowable walking step budget, avoid blocked construction zones.
    - *Environment:* 10x10 campus walkway grid (pathways, administration buildings, construction zones, lawns).
    - *Actuators:* Walking step direction.
    - *Sensors:* Checkpoint reader, blocked pathway detector.

### **Module 2: Uninformed Search Strategies**
- **State Space:** Coordinates $(r, c) \in [0, 9] \times [0, 9]$.
- **Initial State:** $(0, 0)$ (Pharmacy / College Entrance).
- **Goal State:** $(9, 9)$ (Patient Room 304 / Computer Laboratory).
- **Actions:** $\text{Up}: (-1, 0)$, $\text{Down}: (1, 0)$, $\text{Left}: (0, -1)$, $\text{Right}: (0, 1)$.
- **Transition Model:** $\text{Result}(s, a) = s'$ if within bounds and not an obstacle.
- **Step Cost:** Uniform cost $c(s, a, s') = 1$ per step.

---

## 2. Problem 1: Hospital Delivery Robot Navigation

A robot delivers medicines from the hospital pharmacy to a patient's room.

### **Key Metrics & Comparison**
| Metric | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| :--- | :--- | :--- |
| **Data Structure** | FIFO Queue (`collections.deque`) | LIFO Stack (List) |
| **Path Length** | **19 cells (18 steps)** [Optimal] | **27 cells (26 steps)** [Non-optimal] |
| **Nodes Explored** | 75 cells | 56 cells |
| **Completeness** | Complete | Complete (in finite grid with visited set) |
| **Optimality** | **Optimal** (Guaranteed shortest path) | Non-optimal |
| **Time Complexity** | $O(b^d)$ | $O(b^m)$ |
| **Space Complexity** | $O(b^d)$ | $O(b \cdot m)$ |
| **Clinical Suitability** | **Highly Recommended** (Emergency safety) | Not recommended (causes severe delays) |

---

## 3. Problem 2: College Campus Navigation

A student navigates from the campus entrance to the computer laboratory across walkways with construction and blocked pathways.

### **Depth Limit Analysis in Depth-Limited Search (DLS)**
- **Theoretical Shortest Distance:** $d = 18$ steps.
- **Sub-optimal Limit ($L = 10 < d$):** Terminated with **`CUTOFF`** (no path discovered), demonstrating DLS failure when depth budget is insufficient.
- **Suitable Limit ($L = 20 \ge d$):** Successfully found a valid path of 21 cells (20 steps) exploring 48 cells.

| Metric | Breadth-First Search (BFS) | Depth-Limited Search (DLS, $L=20$) | Depth-Limited Search (DLS, $L=10$) |
| :--- | :--- | :--- | :--- |
| **Completeness** | Complete | Complete (since $L \ge d$) | Incomplete (`CUTOFF`) |
| **Optimality** | **Optimal (19 cells)** | Non-optimal (21 cells) | N/A |
| **Explored Cells** | 77 cells | **48 cells** | 48 cells |
| **Space Complexity** | $O(b^d)$ (Exponential) | **$O(b \cdot L)$ (Linear)** | $O(b \cdot L)$ (Linear) |

---

## 4. Search Algorithm Complexities & Comparisons

| Algorithm | Completeness | Optimality | Time Complexity | Space Complexity | Best Use Case |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **BFS** | Yes | Yes (uniform cost) | $O(b^d)$ | $O(b^d)$ | Time-critical shortest paths (e.g., hospital emergency) |
| **DFS** | Yes (finite) | No | $O(b^m)$ | $O(b \cdot m)$ | Deep spaces with ample solutions and memory constraints |
| **DLS** | Yes (if $L \ge d$) | No | $O(b^L)$ | $O(b \cdot L)$ | Memory-constrained systems with known maximum depth bound |

---

## 5. Directory Structure

```plaintext
FAI_Lab_2/
├── FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb    # Complete Google Colab / Jupyter Notebook
├── FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.docx     # Formal Word report formatted per college template
├── generate_lab_visualizations.py                     # Visualization generation script
├── build_lab_package.py                              # Master builder script for all artifacts
├── run_experiments.py                                # Standalone runner script
├── README.md                                         # This documentation
└── visualizations/                                   # High-resolution (200 DPI) output screenshots
    ├── problem1_hospital_bfs.png                     # BFS individual plot (Reg No: 252U1R3013)
    ├── problem1_hospital_dfs.png                     # DFS individual plot (Reg No: 252U1R3013)
    ├── problem1_hospital_robot_bfs_vs_dfs.png        # Problem 1 Dual Comparison Plot
    ├── problem2_campus_bfs.png                       # BFS campus individual plot
    ├── problem2_campus_dls_limit20.png               # DLS L=20 suitable limit plot
    ├── problem2_campus_dls_limit10_cutoff.png        # DLS L=10 cutoff plot
    ├── problem2_campus_navigation_bfs_vs_dls.png     # Problem 2 Dual Comparison Plot
    └── problem2_dls_cutoff_vs_suitable.png           # DLS Cutoff vs Suitable Comparison
```

---

## 6. How to Run (Google Colab & Local Machine)

### **Option A: Running on Google Colab**
1. Open [Google Colab](https://colab.research.google.com/).
2. Click **File -> Upload notebook** and select:
   `FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb`
3. Click **Runtime -> Run all** (or press `Ctrl + F9`).
4. All code executes sequentially, generating stdout metrics and Matplotlib visualizations with **`252U1R3013`** clearly visible.

### **Option B: Running on Local Machine**
```powershell
# Navigate to the lab folder
cd C:\Users\Ayush\Desktop\dsa_lab_1\FAI_Lab_2

# Run standalone experiments
python run_experiments.py

# Or regenerate all plots and documents
python build_lab_package.py
```

---

## 7. Visualizations & Verification (Reg No: 252U1R3013)

Every visualization generated includes:
1. **Header Annotation:** Student Name, Class, and **Registration Number: 252U1R3013**.
2. **Metadata HUD Box:** Real-time search status, path length, nodes explored, optimality verdict, and **Reg No: 252U1R3013**.
3. **Color-Coded Semantic Grid:**
   - 🟢 **Start:** Emerald Green with label (`Pharmacy` / `Entrance`)
   - 🔴 **Goal:** Crimson Red with label (`Room 304` / `Computer Lab`)
   - ⬛ **Obstacles:** Dark Slate `#1E293B`
   - 🔵 **Explored Closed Set:** Sky Blue `#BAE6FD`
   - 🟠 **Computed Trajectory:** Vivid Amber `#F59E0B` dashed line

---

## 8. Submission Artifacts Checklist

- [x] Complete Python Google Colab notebook (.ipynb) with Module 1 & 2 only.
- [x] Problem 1 (Hospital Delivery Robot) BFS and DFS implemented and visualized.
- [x] Problem 2 (College Campus Navigation) BFS and DLS ($L=20$ & $L=10$) implemented and visualized.
- [x] Registration number **252U1R3013** prominently included in all output cells and plots.
- [x] Official Microsoft Word `.docx` report prepared according to college template.
- [x] All code tested and verified locally without errors.
- [x] Complete documentation in README.md.
