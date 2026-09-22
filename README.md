# Lagos Flood & Infrastructure Vulnerability Research

Data-driven assessment and prediction of urban flood vulnerability of road and drainage
infrastructure in Lagos, Nigeria. Built against Master PRD v1.0 (execution baseline: 21 Sept 2026).

## Research problem

Lagos has substantial flood exposure, but a generic flood-susceptibility map does not by
itself explain how road and drainage infrastructure at specific locations responds to that
exposure. This project distinguishes itself through infrastructure-level primary field
observations, standardized road/drainage measurements, and independent field validation,
rather than reproducing a generic susceptibility map (see `docs/gap_matrix.csv` for how this
differs from existing Lagos-focused work).

## Status

Phase 0 (project setup) in progress. See `docs/phase_timeline.md` for the full 12-phase plan.

## Repository structure

```
data/
  raw/        untouched source data as acquired (never edited in place)
  interim/    cleaned but not yet feature-engineered
  processed/  the frozen master analytical dataset
docs/         protocols, gap matrix, target definition, limitations, PRD
notebooks/    exploratory analysis (exploratory only, not the pipeline of record)
src/          scripted, reproducible pipeline code
configs/      parameters for data acquisition, sampling, modelling
figures/      generated figures
maps/         generated maps
results/      model outputs, metrics, reports
paper/        manuscript source
```

## Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproducibility

No transformation should exist only as a manual GIS or spreadsheet step. If it affects the
analytical dataset, it belongs in `src/` as a scripted, version-controlled step.

## Non-negotiables (from the PRD)

- No fabricated data or results, ever.
- The vulnerability target is frozen (`docs/target_definition_v1.md`) before predictive
  modelling begins, with an explicit rule keeping target construction and predictors separate.
- Spatial cross-validation is the primary generalization metric, not random splits.
- A clean-environment reproduction test must pass before anything is called complete.
