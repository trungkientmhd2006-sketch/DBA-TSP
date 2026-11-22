
import csv
from pathlib import Path

RESULTS = Path("data/results")
REFERENCE_COST = 7542


def read_summary(filename):
    with (RESULTS / filename).open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        return {
            row["Metric"]: float(row["Value"])
            for row in csv.DictReader(file)
        }


dba = read_summary("dba_berlin52_summary.csv")
ga = read_summary("ga_berlin52_summary.csv")

with (RESULTS / "nn_berlin52_summary.csv").open(
    "r", newline="", encoding="utf-8-sig"
) as file:
    nn = {
        row["Metric"]: row["Value"]
        for row in csv.DictReader(file)
    }

rows = [
    ("DBA Best", dba["best"]),
    ("DBA Mean", dba["mean"]),
    ("GA Best", ga["best"]),
    ("GA Mean", ga["mean"]),
    ("Multi-start NN", float(nn["best_cost"])),
    ("Optimal Reference", REFERENCE_COST),
]

output = RESULTS / "gap_berlin52.csv"

with output.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Algorithm", "Cost", "Gap (%)"])

    for name, cost in rows:
        gap = (cost - REFERENCE_COST) / REFERENCE_COST * 100
        writer.writerow([name, cost, round(gap, 2)])

print("Berlin52 gap results saved:", output)
