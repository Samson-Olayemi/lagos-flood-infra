# Novelty claim (Phase 1 exit criterion)

Drafted 22 Sept 2026, against 4 identified comparators. See `gap_matrix.csv` for full detail.

## The gap

Four recent, directly relevant studies were reviewed:

1. **Gilbert & Shi (2026, J. African Earth Sciences)** map flood susceptibility across the Lagos
   Lagoon corridor using remote-sensing-derived labels (a Sentinel-1 SAR flood mask) at a 30 m
   grid-cell scale. The output is a susceptibility surface, not an infrastructure outcome, and it
   includes no primary field verification of infrastructure condition.
2. **Akindejoye et al. (2025, IJDRR)** profile household-level social vulnerability to coastal
   flooding in Lekki Peninsula. This is a different outcome entirely (social/household, not
   physical infrastructure).
3. **Aniramu et al. (2026, Progress in Disaster Science)** integrate rainfall trends, flood
   frequency, and household perception into a sustainability index across five Lagos LGAs.
   Drainage appears only as a self-reported household perception score, not a measured physical
   condition.
4. **Olotu et al. (2025, Continental J. Applied Sciences)** is the closest existing comparator:
   a genuinely infrastructure-level, field-based study using deflection testing (FWD) and lab CBR
   testing to link flood exposure to pavement condition across Lagos, Oyo, and Ogun States. It is
   a pavement-engineering study, however, without a drainage-specific protocol, without stratified
   citywide sampling across flood-exposure strata, and without any ML-based predictive modelling,
   interpretability (SHAP), or spatial cross-validation.

Across all four, no existing Lagos-focused study combines: (a) primary field-measured road AND
drainage infrastructure condition, (b) a stratified sample spanning multiple flood-exposure zones
citywide rather than a single corridor, LGA cluster, or opportunistic road set, and (c)
interpretable ML prediction validated with spatial cross-validation and independent remote-sensing
evidence.

## This project's claim

This project is the first to combine standardized, field-measured road and drainage
infrastructure vulnerability, collected across a stratified sample spanning six flood-exposure
strata citywide, with an interpretable machine-learning prediction pipeline validated through
spatial cross-validation and independent Sentinel-1-derived flood evidence, rather than relying
on remote-sensing susceptibility, household perception, or single-corridor pavement testing alone.

## Status

Seeded with 4 comparators as of 22 Sept 2026. Phase 1 is not fully closed: continue widening the
search (informal-settlement infrastructure studies, LASEMA/NiHSA technical reports, other West
African infrastructure-vulnerability field studies) before treating the gap matrix as final.
