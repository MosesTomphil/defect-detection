# Visual Defect Detection

Upload a photo of a manufactured part and get **PASS / FAIL**, an anomaly score, and a heatmap
showing *where* the defect is. Every inspection is logged, and an alert fires when the defect
rate spikes.

The model learns only from photos of **good** parts (unsupervised anomaly detection with
PatchCore), so it doesn't need a library of every possible defect: anything that looks unlike
a good part gets flagged.

> Work in progress. Demo, results and full write-up coming soon.

## Setup

Python 3.11–3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Project structure

```
src/        training, evaluation, inference, inspection log
app/        Gradio web app + example images
notebooks/  experiments and charts (Colab-ready)
results/    curated metrics, charts and example heatmaps
data/       datasets (not committed)
runs/       raw training output and checkpoints (not committed)
```

## Results

_Coming soon._
