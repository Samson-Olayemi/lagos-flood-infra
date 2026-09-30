# Novelty claim (Phase 1 exit criterion) - DRAFT, NOT FINAL

Revised 30 Sep 2026. Replaces the 22 Sep draft. See `gap_matrix.csv` for detail and for what was and was not verified.

## What changed from the 22 Sep draft

- The four comparators were checked on the web. Their titles, authors, journals and (where found) DOIs are confirmed.
- The matrix was rebuilt. The old file had shifted columns and a wrong link for Gilbert & Shi.
- "Olotu et al." is two authors: Olotu and Oyewo.
- Only abstracts were read. Statements about what a paper does NOT include are not yet proven. They must be checked against the full text before this claim is frozen.
- The claim no longer says "first to". That cannot be proven from a limited search.

## The gap (abstract-level)

1. **Gilbert & Shi (2026, J. African Earth Sciences)** map flood susceptibility for the Lagos Lagoon corridor using a Sentinel-1 SAR flood mask (2024) and an interpretable ensemble. The output is a susceptibility surface. The abstract shows no primary field check of road or drainage condition.
2. **Akindejoye et al. (2025, IJDRR)** profile social vulnerability of 1,334 flood-affected households in Lekki Peninsula. The outcome is social, not physical infrastructure.
3. **Aniramu et al. (2026, Progress in Disaster Science)** combine rainfall and streamflow analysis with household perception surveys in Lagos. The abstract does not mention measured road or drainage condition.
4. **Olotu & Oyewo (2025, Continental J. Applied Sciences)** are the closest comparator: field surveys, deflection and CBR testing of pavements in Lagos, Oyo and Ogun States, with a regression model for Pavement Condition Index. It is pavement-focused. Whether it lacks a drainage protocol, stratified sampling, SHAP and spatial cross-validation is **to be confirmed from the full text**. It does fit a predictive regression, so it must not be described as having no predictive modelling.

Three more Lagos papers from the Aniramu/Orimoogunje group are listed as candidates in the matrix and are not yet assessed.

## This project's claim (draft wording)

To our knowledge, and based on a search up to 30 Sep 2026, no Lagos-focused study found so far combines
(a) primary field-measured road and drainage condition,
(b) a sample stratified across several flood-exposure zones citywide, and
(c) interpretable ML prediction checked with spatial cross-validation and independent satellite flood evidence.

This project aims to do that, using a standardized field protocol and a reproducible pipeline.

## Before this claim is frozen

- [ ] Read the full text of comparators 1-4 and confirm each "does not include" statement.
- [ ] Assess the three candidate papers.
- [ ] Widen the search: informal-settlement infrastructure studies, LASEMA / NiHSA technical reports, other West African road-drainage field studies.
- [ ] Find the DOI and correct URL for Gilbert & Shi, and the DOI for Aniramu et al. (2026).
- [ ] Confirm the peer-review status of the venue for Olotu & Oyewo (it is deposited on Zenodo).
