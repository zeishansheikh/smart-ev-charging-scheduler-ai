# ⚡ Smart EV Scheduler — Complete Project Documentation

> **Project Name:** Smart EV Scheduler AI  
> **Language:** Python 3  
> **UI Framework:** Streamlit  
> **Algorithm:** Backtracking (Constraint Satisfaction Problem — CSP)  
> **Author:** Student Project  
> **Last Updated:** May 2026

---

## 📌 Table of Contents

1. [Project Overview](#1--project-overview)
2. [Problem Statement](#2--problem-statement)
3. [Solution Approach — Algorithm](#3--solution-approach--algorithm)
4. [Project Structure](#4--project-structure)
5. [Module-by-Module Explanation](#5--module-by-module-explanation)
   - [5.1 ev_data.py — Data Layer](#51-ev_datapy--data-layer)
   - [5.2 constraints.py — Constraint Logic](#52-constraintspy--constraint-logic)
   - [5.3 scheduler.py — Core Scheduling Engine](#53-schedulerpy--core-scheduling-engine)
   - [5.4 main.py — CLI Entry Point](#54-mainpy--cli-entry-point)
   - [5.5 app.py — Streamlit Web UI](#55-apppy--streamlit-web-ui)
6. [Data Flow Diagram](#6--data-flow-diagram)
7. [Constraint Satisfaction Explained](#7--constraint-satisfaction-explained)
8. [Backtracking Algorithm — Step by Step](#8--backtracking-algorithm--step-by-step)
9. [Web UI (Streamlit) Features](#9--web-ui-streamlit-features)
10. [How to Run the Project](#10--how-to-run-the-project)
11. [Example Output](#11--example-output)
12. [Technologies Used](#12--technologies-used)
13. [Future Improvements](#13--future-improvements)

---

## 1. 🔭 Project Overview

**Smart EV Scheduler AI** is an intelligent Electric Vehicle (EV) charging scheduler that uses a **Constraint Satisfaction Problem (CSP)** approach with a **Backtracking algorithm** to optimally assign EV vehicles to available chargers across different time slots — while respecting grid power limits and charger availability constraints.

The project has two interfaces:
- **CLI (Command Line)** — via `main.py`
- **Web UI (Streamlit Dashboard)** — via `app.py`

---

## 2. 🎯 Problem Statement

In a smart charging station:
- There are **multiple EVs** that need charging.
- There are **limited chargers** available.
- There are **fixed time slots** (Morning, Afternoon, Evening).
- Each time slot has a **maximum power limit** (grid capacity).
- **No two vehicles** can use the **same charger** in the **same time slot**.

### Goal:
> Find a valid assignment of every EV to a (time slot, charger) pair such that:
> 1. The total battery power consumed in any slot does not exceed the grid limit.
> 2. No charger is double-booked in the same slot.

This is a classic **Constraint Satisfaction Problem (CSP)**.

---

## 3. 🧠 Solution Approach — Algorithm

### Backtracking (Brute-Force with Pruning)

The project uses **Backtracking** — a systematic way to explore all possible combinations of (EV → slot, charger) assignments. At each step:

1. Pick the next unassigned EV.
2. Try assigning it to every possible (slot, charger) combination.
3. After each assignment, **check all constraints**.
4. If constraints are satisfied → move to the next EV (recursive call).
5. If constraints are violated → **backtrack** (undo the assignment) and try the next combination.
6. If all EVs are successfully assigned → solution found ✅
7. If no combination works for any EV → no valid schedule exists ❌

### Time Complexity
- **Worst case:** `O((S × C)^N)` where:
  - `S` = number of slots (3)
  - `C` = number of chargers (2)
  - `N` = number of vehicles (4)
- So worst case = `(3 × 2)^4 = 1296` combinations.
- But **constraint pruning** significantly reduces the actual search space.

---

## 4. 📁 Project Structure

```
SmartEVScheduler/
│
├── ev_data.py          # All data: vehicles, slots, chargers, power limits
├── constraints.py      # Constraint checking functions
├── scheduler.py        # Core scheduling engine (Backtracking CSP solver)
├── main.py             # CLI entry point (terminal-based execution)
├── app.py              # Streamlit Web Dashboard (premium UI)
├── __pycache__/        # Python compiled bytecode cache (auto-generated)
└── PROJECT_DOCUMENTATION.md   # This file
```

---

## 5. 📦 Module-by-Module Explanation

---

### 5.1 `ev_data.py` — Data Layer

**Purpose:** Stores all the input data for the scheduling problem.

#### Content:

| Variable | Type | Description |
|----------|------|-------------|
| `vehicles` | `dict` | Dictionary of all EVs with their battery needs and preferred slots |
| `slots` | `list` | List of available time slots: `["Morning", "Afternoon", "Evening"]` |
| `chargers` | `list` | List of available chargers: `["Charger1", "Charger2"]` |
| `max_power_per_slot` | `dict` | Maximum allowed power (kWh) per time slot |

#### Vehicle Data:

| Vehicle | Battery Needed (kWh) | Preferred Slot |
|---------|---------------------|----------------|
| EV1     | 20                  | Morning        |
| EV2     | 30                  | Afternoon      |
| EV3     | 25                  | Evening        |
| EV4     | 35                  | Morning        |

#### Grid Power Limits:

| Slot      | Max Power (kWh) |
|-----------|-----------------|
| Morning   | 60              |
| Afternoon | 60              |
| Evening   | 60              |

#### Key Point:
- The `preferred_slot` field is stored but **not enforced** as a hard constraint. The scheduler assigns vehicles purely based on power and charger constraints. The preferred slot can be used for future soft-constraint optimization.

---

### 5.2 `constraints.py` — Constraint Logic

**Purpose:** Defines the constraint-checking functions that validate whether a given schedule is valid.

#### Functions:

##### `check_power_constraint(schedule) → bool`
```
Logic:
  1. Initialize a dictionary to track total power usage per slot.
  2. For each EV in the schedule, add its battery_needed to the corresponding slot.
  3. If any slot's total usage exceeds max_power_per_slot → return False.
  4. Otherwise → return True.
```

**What it prevents:** Grid overload — ensures no time slot draws more power than the grid can supply.

##### `check_unique_charger(schedule) → bool`
```
Logic:
  1. Maintain a set of used (slot, charger) pairs.
  2. For each EV in the schedule, create a key = (slot, charger).
  3. If the key already exists in the set → return False (conflict!).
  4. Otherwise, add the key to the set → return True.
```

**What it prevents:** Charger double-booking — ensures no two vehicles use the same physical charger at the same time.

---

### 5.3 `scheduler.py` — Core Scheduling Engine

**Purpose:** The heart of the project — implements the **Backtracking CSP solver**.

#### Class: `EVScheduler`

##### `__init__(self)`
- Initializes the list of vehicle names from `ev_data.vehicles`.
- Creates an empty `schedule` dictionary.

##### `is_valid(self) → bool`
- Runs **both** constraint checks:
  - `check_power_constraint(self.schedule)`
  - `check_unique_charger(self.schedule)`
- Returns `True` only if **both** constraints pass.

##### `solve(self, index=0) → bool`
This is the **recursive backtracking function**:

```
solve(index):
    Base Case:
        If index == total number of vehicles → All assigned → return True

    current_ev = vehicles[index]

    For each slot in [Morning, Afternoon, Evening]:
        For each charger in [Charger1, Charger2]:
            
            Assign: schedule[current_ev] = {slot, charger}
            
            If is_valid():           ← Check constraints
                If solve(index + 1): ← Recurse for next EV
                    return True      ← Solution found!
            
            Backtrack: delete schedule[current_ev]  ← Undo assignment
    
    return False  ← No valid option for this EV
```

##### `display_schedule(self)`
- Prints the final schedule in a formatted manner to the terminal.

---

### 5.4 `main.py` — CLI Entry Point

**Purpose:** Simple terminal-based execution of the scheduler.

#### Flow:
1. **Import** `EVScheduler` and `vehicles` data.
2. **Display** all vehicle data (battery needs and preferred slots).
3. **Create** an `EVScheduler` instance.
4. **Run** `scheduler.solve()` to find a valid schedule.
5. **Output:**
   - If solution found → Display the optimized schedule.
   - If no solution → Print error message.

#### How to Run:
```bash
python main.py
```

---

### 5.5 `app.py` — Streamlit Web UI

**Purpose:** A premium, interactive web dashboard for the scheduling system with 4 tabs.

#### Tab 1: 📊 Dashboard & Data
- Displays all vehicle data in a **DataFrame table** (Vehicle ID, Battery Needed, Preferred Slot).
- Shows **metrics**: Total Vehicles, Total Chargers.
- Displays the **grid power limits** per time slot.
- Includes an info box explaining the AI Scheduler's purpose.

#### Tab 2: ⚙️ Constraints Settings
- Allows **dynamic editing** of the grid power limits per slot via number inputs.
- Changes apply to the **current session** and directly affect the scheduling engine.
- Fields: Morning Limit, Afternoon Limit, Evening Limit.

#### Tab 3: 🚀 AI Scheduler
- **"Run AI Scheduling Engine"** button triggers the backtracking solver.
- On success:
  - Shows **balloons animation** 🎈
  - Displays the schedule **grouped by time slot** in premium styled cards.
  - Each card shows: Vehicle Name, Battery (kWh), Assigned Charger.
  - Also shows a **raw data table** of the schedule.
- On failure:
  - Shows an error suggesting to increase power limits.

#### Tab 4: ⏱️ Find Free Slot
- **New feature** — Allows a user to input a new car name and battery requirement.
- The system:
  1. First solves the current schedule for existing vehicles.
  2. Calculates remaining power and charger availability per slot.
  3. Shows which slots the new car can use **without any waiting**.
- If no slots are available → Shows a "fully booked" message.

#### UI Design:
- **Dark mode** aesthetic with green accent colors (`#00E676`, `#69F0AE`, `#B2FF59`).
- Custom CSS for: headers, metric cards, schedule cards, buttons.
- Hover effects and gradient styling on buttons.
- Responsive layout using Streamlit columns.

---

## 6. 🔄 Data Flow Diagram

```
┌──────────────┐
│  ev_data.py  │  ← Source of truth: vehicles, slots, chargers, power limits
└──────┬───────┘
       │
       ▼
┌──────────────────┐      ┌──────────────────┐
│  constraints.py  │◄─────│   scheduler.py   │
│                  │      │                  │
│ • Power Check    │      │ • EVScheduler    │
│ • Charger Check  │      │ • Backtracking   │
└──────────────────┘      │ • solve()        │
                          └────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼               ▼
              ┌──────────┐  ┌───────────┐  ┌──────────────┐
              │ main.py  │  │  app.py   │  │   Output     │
              │  (CLI)   │  │(Streamlit)│  │  Schedule    │
              └──────────┘  └───────────┘  └──────────────┘
```

---

## 7. 🔒 Constraint Satisfaction Explained

This project models the EV charging problem as a **CSP** with:

| CSP Component | In This Project |
|---------------|-----------------|
| **Variables** | Each EV (EV1, EV2, EV3, EV4) |
| **Domains** | All possible (slot, charger) pairs = 3 slots × 2 chargers = 6 options per EV |
| **Constraints** | 1. Power limit per slot ≤ max_power_per_slot |
|                 | 2. Unique (slot, charger) pair — no double booking |

### Constraint Types:
- **Hard Constraint 1 (Power):** The sum of `battery_needed` for all EVs in a single slot must not exceed the slot's `max_power_per_slot`.
- **Hard Constraint 2 (Charger Uniqueness):** Each (slot, charger) pair can be assigned to **at most one** EV.

---

## 8. 🔁 Backtracking Algorithm — Step by Step

Let's trace through a possible execution:

```
Step 1: Assign EV1
  Try (Morning, Charger1) → Valid ✅ → Move to EV2

Step 2: Assign EV2
  Try (Morning, Charger1) → CONFLICT: Charger1 already used in Morning ❌
  Try (Morning, Charger2) → Check power: 20 + 30 = 50 ≤ 60 ✅ → Move to EV3

Step 3: Assign EV3
  Try (Morning, Charger1) → CONFLICT: Charger1 already used in Morning ❌
  Try (Morning, Charger2) → CONFLICT: Charger2 already used in Morning ❌
  Try (Afternoon, Charger1) → Valid ✅ → Move to EV4

Step 4: Assign EV4
  Try (Morning, Charger1) → CONFLICT ❌
  Try (Morning, Charger2) → CONFLICT ❌
  Try (Afternoon, Charger1) → CONFLICT ❌
  Try (Afternoon, Charger2) → Check power: 25 + 35 = 60 ≤ 60 ✅ → ALL ASSIGNED!

Final Schedule:
  EV1 → Morning, Charger1
  EV2 → Morning, Charger2
  EV3 → Afternoon, Charger1
  EV4 → Afternoon, Charger2
```

> **Note:** The actual output may differ because the algorithm finds the **first valid** solution, not necessarily this exact one.

---

## 9. 🖥️ Web UI (Streamlit) Features

| Feature | Tab | Description |
|---------|-----|-------------|
| Vehicle Data Table | Dashboard | Shows all EVs with battery needs and preferred slots |
| Metrics | Dashboard | Total vehicles and chargers count |
| Power Limits Table | Dashboard | Grid power limits per time slot |
| Dynamic Constraints | Constraints Settings | Modify Morning/Afternoon/Evening power limits live |
| AI Scheduler | AI Scheduler | Runs backtracking solver and displays results |
| Timeline View | AI Scheduler | Groups results by time slot in styled cards |
| Free Slot Finder | Find Free Slot | Check if a new car can be accommodated |
| Premium Dark UI | All Tabs | Custom CSS with green accents and hover effects |

---

## 10. 🚀 How to Run the Project

### Prerequisites
```bash
pip install streamlit pandas
```

### Run CLI Version:
```bash
python main.py
```

### Run Web Dashboard:
```bash
streamlit run app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`.

---

## 11. 📋 Example Output

### CLI Output (`main.py`):
```
========== EV VEHICLE DATA ==========
EV1 --> Battery Needed: 20 kWh | Preferred Slot: Morning
EV2 --> Battery Needed: 30 kWh | Preferred Slot: Afternoon
EV3 --> Battery Needed: 25 kWh | Preferred Slot: Evening
EV4 --> Battery Needed: 35 kWh | Preferred Slot: Morning

========== FINAL EV CHARGING SCHEDULE ==========
EV1 --> Slot: Morning | Charger: Charger1
EV2 --> Slot: Morning | Charger: Charger2
EV3 --> Slot: Afternoon | Charger: Charger1
EV4 --> Slot: Afternoon | Charger: Charger2
```

---

## 12. 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core programming language |
| **Streamlit** | Web-based interactive dashboard |
| **Pandas** | Data manipulation and table display |
| **Backtracking (CSP)** | Optimization algorithm for scheduling |
| **HTML/CSS** | Custom styling in Streamlit via `st.markdown()` |

---

## 13. 🔮 Future Improvements

| Improvement | Description |
|-------------|-------------|
| **Soft Constraints** | Use `preferred_slot` as a priority/preference instead of ignoring it |
| **More Vehicles** | Scale to 10+ EVs and test performance |
| **More Chargers** | Add dynamic charger addition |
| **Cost Optimization** | Add electricity pricing per slot and minimize total cost |
| **Priority Scheduling** | Give priority to vehicles with higher battery needs |
| **Database Integration** | Store vehicle data and schedules in a database (SQLite/Firebase) |
| **Real-time Updates** | Live updating dashboard with WebSocket integration |
| **Machine Learning** | Predict optimal slots based on historical charging patterns |

---

## 📝 Summary

This project demonstrates a **real-world AI application** by solving an **EV charging scheduling problem** using:

- **Constraint Satisfaction Problem (CSP)** modeling
- **Backtracking algorithm** for finding valid schedules
- **Streamlit** for an interactive, premium web dashboard
- **Modular architecture** with separate data, constraint, scheduler, and UI layers

The system ensures that all EVs are charged within grid capacity limits, no chargers are double-booked, and provides a user-friendly interface for both viewing and modifying the scheduling parameters.

---

> *Generated for SmartEVScheduler Project — Complete Documentation*
