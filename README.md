# DBA-TSP: Discrete Bat Algorithm for TSP

Starter project for implementing and evaluating a Discrete Bat Algorithm (DBA/IBA)
for the Traveling Salesman Problem (TSP).

## Requirements

- Python 3.10 or newer
- Git
- VS Code (recommended, optional)

## Windows PowerShell setup

```powershell
# 1. Create and enter the project folder after extracting the ZIP
cd dba-tsp

# 2. Create a virtual environment
py -m venv .venv

# 3. Activate it
.\.venv\Scripts\Activate.ps1

# If PowerShell blocks activation, use Command Prompt:
# .venv\Scripts\activate.bat

# 4. Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Run the starter program
python main.py
```

## Git setup

```powershell
git init
git add .
git commit -m "Initial DBA-TSP project structure"
```

If Git asks for your identity, configure it once:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Replace the example identity with your own. Do not put passwords or API keys in Git.

## Proposed architecture

- `src/problem.py`: TSP tour cost and validity checks.
- `src/operators.py`: permutation distance and local-search operators.
- `src/bat.py`: bat representation and algorithm parameters.
- `src/dba.py`: DBA/IBA optimization loop.
- `src/experiment.py`: repeated runs and result summaries.
- `src/visualize.py`: plots for tours and convergence.
- `tests/`: correctness tests.

## Research fidelity note

This repository is a starter scaffold, not yet a faithful reproduction of a paper.
Before claiming reproduction of DBA/IBA, compare the full paper's exact equations,
acceptance rules, parameter schedules, initialization, and stopping criteria.
The supplied summary identifies Hamming distance and adaptive 2-opt/3-opt as key
ideas, but does not contain every implementation detail.

## Suggested first milestone

1. Implement `tour_length` and `is_valid_tour`.
2. Add unit tests for symmetric TSP.
3. Implement 2-opt and test that it preserves a valid permutation.
4. Implement Hamming distance.
5. Add 3-opt, then the DBA/IBA loop.
6. Run repeated experiments and report best, mean, standard deviation, and runtime.
