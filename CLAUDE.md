# CLAUDE.md — Visual Defect Detection (portfolio flagship project)

## Who this is for and why it exists
I'm a recent Cognitive Science graduate (Machine Learning specialization) applying for a role at a
**manufacturing company** (not a tech company). The role is about using AI to automate work, build
workflows, and make existing workflows easier. I was referred directly to a VP, who is business-minded
and probably not an ML specialist.

This project is the featured piece of my portfolio. It must show that I can take a real manufacturing
problem, apply ML to it, and ship something that works end to end. It must be general to manufacturing,
not tailored to any one company or product.

## Hard constraints
- **No LLM APIs.** Do not call Anthropic, OpenAI, or any hosted large-model API anywhere in this project.
  All models are trained or run locally with open-source tools.
- **Speed matters.** Target: working, deployed demo in ~8 working days. Prefer simple, reliable solutions
  over clever ones. Ask before adding big dependencies.
- **I must be able to explain everything.** Keep code readable, commented where non-obvious, and explain
  your choices when you finish a task. No magic.

## What we're building
A system that inspects a photo of a part, decides PASS/FAIL, shows a heatmap of where the defect is,
and logs every inspection with an alert when the defect rate spikes.

- **Approach:** unsupervised anomaly detection — train only on images of good parts.
- **Main model:** PatchCore via **anomalib** (`pip install "anomalib[cpu]"`, or the CUDA extra on Colab).
  Comparison models: PaDiM (`Padim`) and EfficientAD (`EfficientAd`).
- **Current anomalib API (v2.x):** `from anomalib.data import MVTecAD, Folder`,
  `from anomalib.models import Patchcore`, `from anomalib.engine import Engine`;
  `engine.fit(model=..., datamodule=...)`, `engine.test(...)`, `engine.export(...)`.
  The API changes between versions — check the installed version and its docs before writing code,
  and pin the version in requirements.txt.
- **Datasets:**
  1. MVTec AD (public benchmark; non-commercial license, fine for a portfolio). Categories: `screw`,
     `metal_nut`, `bottle`.
  2. My own photos in `data/custom/` (layout below).
- **App:** Gradio, deployed to a Hugging Face Space on the free CPU tier.
- **Heavy training:** I run it on Google Colab (GPU). Scripts must work both locally (CPU) and on Colab.

## Repo layout
```
defect-detection/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .gitignore            # ignore data/, model checkpoints over ~100 MB, .venv, __pycache__
├── notebooks/            # experiments, comparison and charts (also Colab-ready)
├── src/
│   ├── train.py          # train a model on an MVTec category or the custom folder dataset (CLI args)
│   ├── evaluate.py       # metrics, threshold sweep, timing
│   ├── visualize.py      # heatmap overlays, catch-rate vs false-alarm chart
│   ├── inference.py      # load exported model, score one image -> (score, label, heatmap)
│   └── inspection_log.py # SQLite logging + defect-rate + alert logic
├── app/
│   ├── app.py            # Gradio app (3 tabs)
│   └── examples/         # 6–8 example images
├── data/                 # NOT committed
│   └── custom/
│       ├── good/         # training images (good parts only)
│       └── test/
│           ├── good/     # held-out good images
│           └── defect/   # defective images (test only, never training)
└── results/              # metrics JSON/CSV, charts, example heatmaps
```

## Build steps (do one at a time; I'll tell you which)
1. **Setup:** repo structure, requirements.txt (pinned), .gitignore, a minimal README.
2. **Baseline:** `src/train.py` trains PatchCore on a chosen MVTec category; saves metrics to `results/`.
3. **Evaluation:** add Padim and EfficientAd. Produce:
   - comparison table: image AUROC, pixel AUROC, ms/image (CPU and GPU), model size;
   - threshold sweep → catch rate (recall on defects) vs false-alarm rate (good parts flagged), as a chart;
   - a recommended threshold with a one-line business justification
     (e.g., "catches 97% of defects; 3% of good parts re-checked = 30 parts per 1,000").
4. **Error analysis:** save heatmap overlays for correct catches, misses, and false alarms into `results/`.
5. **(Me)** I photograph my own dataset.
6. **Custom data:** train on `data/custom/` using the `Folder` datamodule, repeat the evaluation,
   try one improvement and report before/after, then export the final model.
7. **App (`app/app.py`), three tabs:**
   - *Inspect one part:* upload or webcam → PASS/FAIL, anomaly score, heatmap overlay.
   - *Batch inspection:* upload multiple images or a zip → table (file, score, result) + downloadable CSV.
   - *Inspection log:* every inspection saved to SQLite (timestamp, file, score, result);
     defect-rate-over-time chart; red alert banner when the defect rate over the last N inspections
     exceeds a configurable limit (default: >5% over last 50).
   Include clickable example images.
8. **Deploy:** make it run on a Hugging Face Space (CPU). Keep the model small (lower PatchCore
   coreset sampling ratio if needed) and inference under ~2 s per image.
9. **Docs:** README with demo GIF placeholder, results table, how to run, structure, limitations,
   and a "If I deployed this in a real plant" section (fixed camera + lighting, shadow mode first,
   human review of flagged parts, retraining when product/lighting changes, value estimate).

## Working rules
- One step per session unless I say otherwise. Confirm the plan in 3–5 bullets before writing lots of code.
- After each step: run it, show me the output/metrics, then explain what the code does in plain language.
- Keep functions small; type hints; no unnecessary abstractions.
- Never commit datasets or large checkpoints. Fix random seeds where possible.
- Report numbers honestly, including failures. Don't tune on the test set.
- Write all results to `results/` in a form I can paste into my portfolio page.

## Definition of done
- Public Hugging Face Space where anyone can upload a photo and get PASS/FAIL + heatmap.
- Batch inspection producing a CSV report; inspection log with defect-rate chart and alert.
- Results table for MVTec and my own data; catch-rate vs false-alarm chart; chosen threshold justified.
- README clear enough that a non-technical manager understands what it does in 30 seconds.
