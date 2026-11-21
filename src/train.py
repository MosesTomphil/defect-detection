"""Train an anomaly model on an MVTec category or the custom Folder dataset. (Step 2)"""

from pathlib import Path

# Raw anomalib output (checkpoints, prediction images) goes here and is git-ignored.
# Pass this as Engine(default_root_dir=RUNS_DIR); anomalib's default would be "results/".
RUNS_DIR = Path("runs")

# Curated outputs only: metrics JSON/CSV, charts, selected heatmaps for the portfolio.
RESULTS_DIR = Path("results")
