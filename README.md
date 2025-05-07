**Author**  
This codebase was created by **Maxence Cailleteau** for the GRIPIT reserch group (@HEIG-VD).
GRIPIT - Groupe de Recherche Interdisciplinaire en Projet Innovant de Transport


# GRIPIT_Ohwaboo_simulations
A compact, end‑to‑end Python framework that simulates and analyses the non‑linear flight dynamics of the Ohwaboo pod, the passive‑maglev demonstrator developed under the GRIPIT project (HES‑SO, Axis 2). 


This repository simulates the non-linear dynamics of the Ohwaboo maglev demonstrator, part of GRIPIT axis 2 at HES‑SO.


### What it is

A compact, end‑to‑end Python framework that **simulates and analyses the non‑linear flight dynamics of the Ohwaboo pod**, the passive‑maglev demonstrator developed under the GRIPIT project (HES‑SO, Axis 2). From a single entry‑point it

* builds 3‑D force maps for the chosen magnet geometry,
* integrates the full 6‑DoF equations of motion with magnetic, booster, suspension, drag and brake loads,
* post‑processes results into CSV, 20+ publication‑ready plots and a one‑click HTML → PDF report.

### Why you might care

Colleagues can tweak masses, magnet layouts, suspension stiffness/damping or acceleration profiles and immediately get an updated **“engineering pack”** (figures + KPIs) without touching the solver itself.

---

### Repo structure

```
│ main.py               # Entry point – choose scenario & launch everything
│ datas.py              # Centralised parameters (rail, pod, control flags…)
│ scenarios_masses.py   # Mass breakdowns for each design iteration
│ geometry.py           # Computes instantaneous pod/rail geometry
│ forces.py             # Aggregates all loads except magnets
│ disp_forces_mag.py    # Builds Fx/Fy/Fz surface from magnet data
│ simulation.py         # SciPy solve_ivp wrapper + non‑linear ODE system
│ initialisation.py     # Generates initial state + spring pre‑loads
│ sauvegarde.py         # Creates run folder, handles CSV & figure exports
│ display.py            # 19 default plots for quick visual checks
│ analyse.py            # KPI & FFT helpers
│ script_rapport.py     # Generates HTML then converts to PDF
│ auto_test.py          # Minimal regression tests
└── user_inputs.py      # CLI helpers (optional)
```

### Quick start

```bash
# 0. In cmd.exe go to the repository
cd %folderpath%

# 1. Create/activate virtual environment
python -m venv .venv

# 2. Activate virtual environment
.\.venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt   # numpy, scipy, pandas, matplotlib, pdfkit…

# 4. Run a default scenario
python main.py
```

*Outputs land in* `out/<timestamp>/*` :
`Output.csv`, `*_Compte_rendu_simu.html`, `*.pdf`, and all `.png` figures.

### Customising a run

1. **Select a mass set** in `scenarios_masses.py` (e.g. `masse_version = "2025Q1_150kg"`).
2. **Edit key parameters** in `datas.py` – magnet dimensions, suspension $k/c$, booster force, simulation end‑criteria, etc.
3. Hit **`python main.py`** again; the solver re‑uses your edits and rebuilds the report.

### Tests

`pytest auto_test.py` checks that:

* the solver completes without gap inversion or NaNs,
* KPI regressions stay within tolerance.

### Licence

Distributed under the **GNU General Public License v3.0** (GPL‑3.0‑or‑later).  
See the `LICENSE` file for full terms.

Feel free to fork, extend, or plug in your own force models. Contributions welcome!

---
