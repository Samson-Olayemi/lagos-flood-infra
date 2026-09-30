# PROJECT STATE

Last updated: 30 Sep 2026 (end of session 5).
Source of truth order: Master PRD v1.0, then this file, then `lagos_flood_tracker.xlsx`.
Update this file at the end of every working session. Chats do not share memory.

## 1. Where the project stands

- Today is 30 Sep 2026. Pilot field study is planned for **3-4 Oct 2026**.
- Phase 0 (setup): repo skeleton exists on GitHub (1 commit). Clean-environment hello-world not confirmed.
- Phase 1 (literature): in progress, **not closed**. Gap matrix rebuilt (4 comparators verified at abstract level, 3 candidates not yet assessed). Novelty claim is a draft.
- Phase 2 (dataset audit): **not started. Was due 2 Oct, so behind.**
- Phase 3 (pilot): form and protocol drafted. **Form not yet tested on the iPhone.** No pilot sites chosen yet.
- Phases 4-12: not started.

## 2. Files and their status

| File | Status |
|---|---|
| `docs/data_dictionary.csv` | Draft v1.0, 56 fields. Single source for the form and the validator |
| `configs/field_form_v1_0.xlsx` | XLSForm, generated from the dictionary. Converts cleanly with pyxform. **Never run on a phone** |
| `src/build_xlsform.py` | Builds the form from the dictionary |
| `src/clean.py` | Validator for the field export (PRD 18, 19). Has had only a small smoke check. First real test = pilot data |
| `docs/field_protocol.md` | v0.2 DRAFT. Anchors marked [DRAFT] are project drafts, not from a published standard |
| `docs/phone_quickstart.md` | Short field guide for the iPhone |
| `docs/gap_matrix.csv` | Rebuilt. 7 rows, 14 columns |
| `docs/novelty_claim.md` | Draft, softened. Not final |
| `.gitignore`, `requirements.txt` | Updated (blocks photos and processed data; adds openpyxl, pyxform) |

## 3. Decisions

**Made by the owner**
- Python 3.12 is the language. QGIS is only for viewing maps.
- Field device: iPhone. A laptop is also available.
- No test runs on fake data. The code's first real run is on real pilot data.
- The owner pushes to GitHub. Claude cannot push and will not ask for a token.

**Drafted by Claude, waiting for owner approval** (see `docs/field_protocol.md` section 13)
1. Observation segment length 50 m.
2. Pilot site IDs `LAG-FI-Pnn` and stratum value `PILOT`.
3. Fixed right-hand-drain rule and a `none` option when there is no drain.
4. Edge failure and erosion are two separate variables.
5. Draft ordinal score anchors and the higher-class rule on boundaries.
6. Skip local flood history in the pilot (needs a consent step).
7. Photos are taken with the iPhone Camera app (marker card first) and matched by script. They are not uploaded through the form.
8. Extra context fields such as weather at visit are **not** added. They would change core variables and need a PRD version bump.

## 4. Open questions

1. Does the Kobo web form work offline on the iPhone? Test in airplane mode before 3 Oct.
2. Is the owner eligible for the free KoboToolbox plan?
3. Pilot sites: are they pilot-only? They are hand-picked, which conflicts with "no convenience sampling" if used in the final data. Recommendation: pilot-only.
4. H2 versus target dimension B: obstruction cannot be both a predictor and a target component. Must be settled in `target_definition_v1.md` by 6 Oct.
5. Full text of the four comparator papers has not been read. DOIs still missing for Gilbert & Shi (2026) and Aniramu et al. (2026).
6. Minor PRD inconsistencies to settle later: pilot size (15-20 in section 23, 10-15 in section 24, 18 in the tracker); source registry path (`data/` in section 10, `docs/` in section 21); `target_definition.md` versus `target_definition_v1.md`.

## 5. Risks

- Rain on 3-4 Oct would move the pilot and push back the 10 Oct campaign start.
- Phase 2 is already behind schedule.
- The repo is public. Photos and raw field data must not be committed before a privacy review.

## 6. Next 3 actions

1. Push the latest update zip to GitHub. Set up KoboToolbox. Add the form to the iPhone Home Screen and run the airplane-mode test.
2. Choose pilot areas, route, transport and PPE for 3-4 Oct. Approve or change the draft decisions in section 3.
3. Start the dataset audit and `source_registry.csv` (Phase 2).

## 7. Session log

| Session | What was done |
|---|---|
| 1 | Read all project files. Built data dictionary, form generator, validator and protocol v0.1 |
| 2 | Verified the four comparator papers. Rebuilt the gap matrix. Softened the novelty claim. Updated `.gitignore` and requirements |
| 3 | Fixed validator for Kobo-style column names. Added the phone guide. Packed an update zip |
| 4 | Confirmed Claude cannot push to GitHub or create the Kobo account |
| 5 | iPhone confirmed. Photo workflow changed to Camera app plus marker card. Protocol v0.2. Added this file and an improved README |
