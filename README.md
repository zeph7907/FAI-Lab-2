# Fundamentals of Artificial Intelligence (FAI) - Lab Report 2
## Uninformed Search Strategies (BFS, DFS, and DLS)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/zeph7907/FAI-Lab-2)

### Student Credentials
- **Student Name:** Ayush Aditya
- **Registration Number:** **`252U1R3013`**
- **Class / Program:** B.Tech Computer Science and Engineering (Data Science)
- **Section & Room:** Section S20 / Room 205
- **Year & Academic Term:** 2nd Year, Term 2
- **Institution:** Aurora Deemed to be University
- **Subject:** Fundamentals of Artificial Intelligence
- **Lab Assessment:** Lab Report 2 (Week 2 Laboratory)
- **Syllabus Coverage:** Strictly restricted to **Module 1** (Introduction to AI & Intelligent Agents) and **Module 2** (Uninformed Search Strategies: State Space Search, BFS, DFS, DLS).

---

## 🔗 Official Submission Links
- **Google Colab Interactive Notebook:**  
  [https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb](https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)
- **GitHub Source Code Repository:**  
  [https://github.com/zeph7907/FAI-Lab-2](https://github.com/zeph7907/FAI-Lab-2)

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
- **State Space ($S$):** Coordinates $(r, c) \in [0, 9] \times [0, 9]$.
- **Initial State ($s_0$):** $(0, 0)$ (Pharmacy / College Entrance).
- **Goal State ($s_{\text{goal}}$):** $(9, 9)$ (Patient Room 304 / Computer Laboratory).
- **Actions ($A(s)$):** $\text{Up}: (-1, 0)$, $\text{Down}: (1, 0)$, $\text{Left}: (0, -1)$, $\text{Right}: (0, 1)$.
- **Transition Model:** $\text{Result}(s, a) = s'$ if within bounds and not an obstacle.
- **Step Cost:** Uniform cost $c(s, a, s') = 1$ per step.

---

## 2. Problem 1: Hospital Delivery Robot Navigation

A robot delivers medicines from the hospital pharmacy $(0, 0)$ to a patient's room $(9, 9)$.

### **Key Metrics & Comparison**
| Metric | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| :--- | :--- | :--- |
| **Data Structure** | FIFO Queue (`collections.deque`) | LIFO Stack (List) |
| **Path Length** | **19 cells (18 steps)** [Optimal] | **27 cells (26 steps)** [Non-optimal detour] |
| **Nodes Explored** | 75 cells | 56 cells |
| **Completeness** | Complete | Complete (in finite grid with visited set) |
| **Optimality** | **Optimal** (Guaranteed shortest path) | Non-optimal |
| **Time Complexity** | $O(b^d)$ | $O(b^m)$ |
| **Space Complexity** | $O(b^d)$ | $O(b \cdot m)$ |
| **Clinical Suitability** | **Mandatory / Preferred** (Emergency safety) | Not recommended (causes severe delays) |

---

## 3. Problem 2: College Campus Navigation

A student navigates from the campus entrance $(0, 0)$ to the computer laboratory $(9, 9)$ across walkways with construction and blocked pathways.

### **Depth Limit Analysis in Depth-Limited Search (DLS)**
- **Theoretical Shortest Distance:** $d = 18$ steps.
- **Sub-optimal Limit ($L = 10 < d$):** Terminated with **`CUTOFF`** (no path discovered), demonstrating DLS failure when the depth budget is insufficient.
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
| **BFS** | Yes | Yes (uniform cost) | $O(b^d)$ | $O(b^d)$ | Time-critical shortest paths (Hospital Emergency) |
| **DFS** | Yes (finite) | No | $O(b^m)$ | $O(b \cdot m)$ | Deep spaces with ample solutions and memory constraints |
| **DLS** | Yes (if $L \ge d$) | No | $O(b^L)$ | $O(b \cdot L)$ | Memory-constrained systems with known maximum depth bound |

---

## 5. Repository Structure

```plaintext
FAI_Lab_2/
├── FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb    # Interactive Google Colab Notebook
├── FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.md       # Complete Markdown Lab Report
├── generate_lab_visualizations.py                     # Visualization & algorithm implementation
├── run_experiments.py                                # Standalone runner script
└── README.md                                         # Project Documentation
```

---

## 6. How to Run

### **Option A: 1-Click Launch in Google Colab**
1. Click the **Open in Colab** badge above or open:  
   [https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb](https://colab.research.google.com/github/zeph7907/FAI-Lab-2/blob/main/FAI_Lab_Report_2_Ayush_Aditya_252U1R3013.ipynb)
2. In Google Colab, click **Runtime -> Run all** (`Ctrl + F9`).
3. All code cells execute sequentially, generating outputs and grid visualizations with registration number **`252U1R3013`** clearly visible.

### **Option B: Running on Local Machine**
```powershell
# Clone or navigate to the repository
git clone https://github.com/zeph7907/FAI-Lab-2.git
cd FAI-Lab-2

# Run standalone experiments
python run_experiments.py
```
