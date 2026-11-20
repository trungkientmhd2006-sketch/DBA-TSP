# DBA-TSP: Discrete Bat Algorithm for the Traveling Salesman Problem

## 1. Project Overview

This project implements and evaluates a Discrete Bat Algorithm (DBA) for solving the Traveling Salesman Problem (TSP).

The project focuses on permutation-based search operators, 2-opt local search, repeated experiments, and statistical evaluation.

The implementation uses the Basic Discrete Bat Algorithm (BA1) with 2-opt neighborhood search.

## 2. Main Features

- TSPLIB instance reading (EUC_2D).
- Distance matrix calculation using TSPLIB rounding.
- TSP tour cost evaluation and solution validation.
- Discrete permutation operators:
  - Swap
  - Insertion
  - 2-opt
- Hamming distance calculation.
- Bat population initialization.
- Discrete Bat Algorithm optimization.
- 2-opt local search.
- Nearest Neighbor heuristic.
- Multi-start Nearest Neighbor.
- Repeated experiments with multiple random seeds.
- Statistical analysis:
  - Best cost
  - Worst cost
  - Mean cost
  - Standard deviation
  - Runtime
- Convergence and comparison plots.
- Optimality gap calculation.
- CSV result export.

## 3. Project Structure

```text
DBA-TSP/
│
├── data/
│   ├── instances/
│   │   └── eil51.tsp
│   │
│   └── results/
│       ├── dba_eil51_runs.csv
│       ├── dba_eil51_summary.csv
│       ├── gap_eil51.csv
│       ├── convergence_eil51.png
│       └── comparison_eil51.png
│
├── src/
│   ├── __init__.py
│   ├── bat.py
│   ├── dba.py
│   ├── experiment.py
│   ├── nearest_neighbor.py
│   ├── operators.py
│   ├── problem.py
│   └── visualize.py
│
├── tests/
│   ├── test_dba.py
│   ├── test_nearest_neighbor.py
│   ├── test_operators.py
│   └── test_problem.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 4. Requirements

- Python 3.10 or newer
- Git
- VS Code (recommended)
- Matplotlib
- Pytest

## 5. Installation

### Windows PowerShell

Clone the repository:

```powershell
git clone https://github.com/trungkientmhd2006-sketch/DBA-TSP.git
cd DBA-TSP
```

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
# If PowerShell blocks script execution, use:
.\.venv\Scripts\activate.bat
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Running Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The current project test suite contains 50 tests.

## 7. Running Experiments

The experiments use the `eil51.tsp` TSPLIB instance.

Run DBA with 10 different random seeds:

```powershell
python -c "from src.problem import read_tsplib,calculate_distance_matrix; from src.experiment import run_experiments,save_experiment_results; cities=read_tsplib('data/instances/eil51.tsp'); D=calculate_distance_matrix(cities); experiment=run_experiments(D,seeds=range(10),population_size=50,iterations=50); save_experiment_results(experiment,instance_name='eil51')"
```

This experiment uses:

- Population size: 50
- Iterations: 50
- Random seeds: 0–9

The results are saved in `data/results/`.

## 8. Nearest Neighbor

The project implements:

- Single-start Nearest Neighbor.
- Multi-start Nearest Neighbor.

Multi-start Nearest Neighbor runs the heuristic from every possible starting city and selects the best resulting tour.

## 9. Visualization

### Convergence Plot

Generate the DBA convergence plot:

```powershell
python -c "from src.problem import read_tsplib,calculate_distance_matrix; from src.dba import solve_tsp; from src.visualize import plot_convergence; cities=read_tsplib('data/instances/eil51.tsp'); D=calculate_distance_matrix(cities); result=solve_tsp(D,population_size=50,iterations=50,seed=42); plot_convergence(result['history'])"
```

Output:

`data/results/convergence_eil51.png`

### Algorithm Comparison

Generate the comparison plot:

```powershell
python -c "from src.visualize import plot_comparison; plot_comparison()"
```

Output:

`data/results/comparison_eil51.png`

## 10. Experimental Results

### Dataset

| Property | Value |
|---|---:|
| Instance | eil51 |
| Number of cities | 51 |
| Edge weight type | EUC_2D |
| Population size | 50 |
| Iterations | 50 |
| Number of DBA runs | 10 |

### DBA Results

| Metric | Result |
|---|---:|
| Best | 443 |
| Worst | 469 |
| Mean | 453.8 |
| Standard deviation | 8.3373 |
| Mean runtime | Approximately 0.97 seconds |

### Comparison with Multi-start Nearest Neighbor

| Algorithm | Tour Cost |
|---|---:|
| Multi-start NN | 482 |
| DBA Mean | 453.8 |
| DBA Best | 443 |
| Optimal reference | 426 |

### Optimality Gap

The percentage gap is calculated as:

\[
Gap(\%) =
\frac{C_{\text{algorithm}}-C_{\text{reference}}}
{C_{\text{reference}}}\times100
\]

| Algorithm | Gap |
|---|---:|
| Multi-start NN | 13.15% |
| DBA Mean | 6.53% |
| DBA Best | 3.99% |
| Optimal reference | 0% |

The optimal reference cost for eil51 is 426.

In this experiment, DBA achieved a lower average tour cost than Multi-start Nearest Neighbor. However, further experiments are needed to establish a more general performance comparison.

## 11. Research Methodology

The implementation follows the Basic Discrete Bat Algorithm (BA1) approach using:

- Hamming distance for discrete solution comparison.
- 2-opt neighborhood operations for solution movement.
- Local search around selected high-quality bats.
- Loudness-based solution acceptance.
- Adaptive loudness and pulse rate parameters.

The implementation focuses on symmetric TSP instances.

It should not be interpreted as a complete reproduction of every DBA/IBA variant described in the literature.

## 12. References

Osaba, E., Yang, X. S., Diaz, F., Lopez-Garcia, P., & Carballedo, R. (2016).

An Improved Discrete Bat Algorithm for Symmetric and Asymmetric Traveling Salesman Problems.

Engineering Applications of Artificial Intelligence, 48, 59–71.

TSPLIB: Traveling Salesman Problem Library.

http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

## 13. Future Improvements

- Evaluate additional TSPLIB instances.
- Increase the number of independent experimental runs.
- Compare with additional TSP heuristics.
- Improve parameter tuning.
- Evaluate solution quality and computational efficiency across different instances.
- Investigate additional discrete neighborhood operators.
