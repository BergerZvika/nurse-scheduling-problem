# Nurse Scheduling Problem

An interactive optimization sandbox that solves the **Nurse Scheduling Problem (NSP)** using seven different algorithms — from exact integer programming to genetic algorithms — all behind a browser-based GUI, plus a bonus single-file **3D Visualization Lab** for exploring solutions in real time.

The NSP assigns nurses to shifts across a week while respecting a mix of **hard constraints** (coverage, legal rest, weekly caps) and **soft constraints** (individual shift preferences). It is a classic NP-hard combinatorial optimization problem, and this project compares how different algorithmic families attack it on the same instance.

---

## Features

- **Seven algorithms** implemented end-to-end, each runnable from the same web UI:
  1. **Maximum Shift** — Integer Programming formulation
  2. **CSP** — pure Constraint Satisfaction
  3. **CSP + Minimum Unrequested Shifts** — CSP with an objective function
  4. **Hill Climbing**
  5. **Hill Climbing with Random Restarts**
  6. **Simulated Annealing**
  7. **Genetic Algorithm**
- **Web GUI** (Flask + vanilla JS) to configure nurses, days, shifts per day, weekly caps, and shift preferences, then run any algorithm and inspect the schedule it produced.
- **Cost / iteration plots** generated per run so you can compare convergence behaviour across algorithms.
- **3D Visualization Lab** (`visualization_lab.html`) — a self-contained Three.js page that runs the heuristic algorithms **live in the browser** on a rotating 3D cube grid, with real-time cost curves, hover tooltips, and cinematic camera controls. No server needed.

---

## Project layout

```
nurse-scheduling-problem/
├── README.md
├── visualization_lab.html        ← single-file 3D lab (open directly in a browser)
├── nsp presentation.pptx
├── nsp report.pdf
└── OptimizationGui/
    ├── server.py                 ← Flask entry point (port 80)
    ├── main.py
    ├── nurse_class.py            ← core NSP model: cost, constraints, violations
    ├── MaxShifts.py              ← algo 1 — Integer Programming
    ├── csp.py                    ← algo 2 — Constraint Satisfaction
    ├── shift_min.py              ← algo 3 — CSP + objective
    ├── hill_climbing.py          ← algo 4
    ├── new_starts_hill_climbing.py ← algo 5 — random restarts
    ├── simulated_annealing.py    ← algo 6
    ├── genetic.py                ← algo 7
    ├── cp.py, function.py, DataToSend.py
    ├── requirements.txt
    ├── static/                   ← JS, CSS, generated plots
    └── templates/                ← NspGui.html, result_output.html
```

---

## Problem model

Each candidate schedule is a flat binary vector of length `nurses × days × shifts_per_day`, where `1` means "this nurse works this shift." The cost function (see `OptimizationGui/nurse_class.py`) counts:

**Hard violations** (weighted by `HARD_CONSTRAINT_PENALTY`):
- **Consecutive shifts** — a nurse working two back-to-back shifts.
- **Weekly shift cap** — deviation from a target number of shifts per nurse per week.
- **Per-shift staffing** — too few or too many nurses covering a given shift.

**Soft violations:**
- **Preference breaks** — a nurse is scheduled on a shift they requested off.

The total cost is `HARD_CONSTRAINT_PENALTY × hard + soft`, so algorithms must first eliminate hard violations before trimming preference breaks.

---

## Running the web GUI

### 1. Install dependencies

```bash
cd OptimizationGui
pip install -r requirements.txt
```

### 2. Start the server

```bash
python server.py
```

### 3. Open the GUI

Navigate to <http://localhost:80/> in your browser. You can:

- Set the number of nurses, days, and shifts per day.
- Configure each nurse's target weekly shifts and shift-off requests.
- Pick an algorithm and run it.
- Inspect the produced schedule and the cost-vs-iteration plot for heuristic methods.

> **Port 80** typically requires elevated privileges on Linux/macOS. If launching fails, change the port inside `server.py` (e.g. to `8080`) and open <http://localhost:8080/>.

---

## Running the 3D Visualization Lab

The lab is a **single HTML file** — no server, no build step, no dependencies beyond a modern browser.

```bash
# Open directly
xdg-open visualization_lab.html    # Linux
open    visualization_lab.html     # macOS
start   visualization_lab.html     # Windows
```

Or double-click the file in your file manager.

### What you can do in the lab

- Pick any of the seven algorithms from the left panel and watch it optimise **live**.
- Drag to orbit the 3D schedule grid; scroll to zoom; hit `A` to toggle auto-rotate.
- Hover any cube to see which nurse / day / shift it represents and whether it was requested off.
- Adjust problem size (nurses, days, shifts/day, weekly cap) and regenerate random preferences.
- Tune the animation speed while an algorithm is running.
- Read real-time telemetry: current cost, best cost, hard violations, preference breaks, iteration counter, and elapsed time.
- Watch the **cost trajectory** render at the bottom as the search progresses.

### Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Space` | Run / pause the selected algorithm |
| `R` | Reset the problem instance |
| `A` | Toggle camera auto-rotate |

### Axes

- **X** — days of the week (Mon → Sun)
- **Y** — shifts in the day (Morning / Evening / Night)
- **Z** — individual nurses

A glowing cyan cube is an assigned shift; a magenta-tinted glow marks a shift that violates that nurse's off-request.

---

## Algorithm cheat sheet

| # | Algorithm | Family | Strengths | Weaknesses |
|---|-----------|--------|-----------|------------|
| 1 | Max Shift | Integer Programming | Optimal under its objective | Does not model preferences |
| 2 | CSP | Constraint Satisfaction | Finds feasible solutions fast | No quality ranking |
| 3 | CSP + Min Unrequested | CSP + objective | Feasible *and* preference-aware | Slower than pure CSP |
| 4 | Hill Climbing | Local Search | Simple, fast descent | Gets stuck in local minima |
| 5 | HC + Random Restart | Stochastic Local Search | Escapes local minima | No memory across restarts |
| 6 | Simulated Annealing | Metropolis-Hastings | Escapes minima, tunable | Cooling schedule matters a lot |
| 7 | Genetic Algorithm | Evolutionary | Explores broadly | Slower per iteration, more knobs |

See `nsp report.pdf` and `nsp presentation.pptx` for the full write-up, experimental comparison, and design decisions.

---

## Requirements

See `OptimizationGui/requirements.txt`. The main libraries are:

- `Flask` — web server for the GUI
- `numpy` — vector math
- `matplotlib` — cost / iteration plots
- `ortools` — CP-SAT and integer programming backend used by algorithms 1–3
- `deap` (or equivalent evolutionary library, see requirements) — genetic algorithm

The 3D lab loads Three.js from a CDN and needs no Python at all.

---

## License

Academic project — released for educational use. Feel free to read, fork, and learn from it.

Enjoy scheduling your nurses.
