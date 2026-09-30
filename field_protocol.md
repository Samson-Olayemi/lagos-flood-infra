# Field Protocol v0.1 (DRAFT for the 3-4 Oct 2026 pilot)

Built from Master PRD v1.0, sections 6, 7, 8, 18, 19 and 20.
Companion files: `docs/data_dictionary.csv` (every variable) and `configs/field_form_v1_0.xlsx` (the digital form).
**If this protocol and `data_dictionary.csv` ever disagree, the data dictionary wins. Fix this file.**

**Status of the anchors.** The PRD gives ordinal scores as none / minor / moderate / severe and gives no
measurable description. Wherever this protocol adds a description, it is marked **[DRAFT]**. These are project
drafts, not taken from a published standard. They are tested in the pilot. After the pilot they may be revised once,
documented, and then frozen (PRD phase 3). Any change means a new form version (see section 11).

---

## 1. Safety rules (always first)

These come from PRD section 20. No data point is worth breaking them. A skipped field is fine. An injury is not.

1. Daylight only. Leave the site before it gets dark.
2. Never enter a drain, flowing water, floodwater, a traffic lane, an unstable structure, or private property without permission.
3. Measure drains from outside. Use the tape on a rod or the laser meter.
4. Never get into water to take a photo or a measurement.
5. Heavy rain or flooded roads: stop. Reschedule. Do not force sampling (PRD risk register).
6. Do not go alone to a site that feels unsafe. Tell someone your route and expected return time.
7. If a site is unsafe, do not do it. Mark it `refused_unsafe` (see section 6), log it, and move to the next site (or use a reserve, section 10).
8. Wear PPE where conditions need it (gloves near drains, high-visibility vest near traffic, closed shoes).

## 2. What to carry (PRD section 8)

- Smartphone with GPS and camera, charged, form loaded and **tested offline**.
- Power bank (strongly recommended).
- Measuring tape. Laser distance meter if you have one. A rod or stick to hold the tape against a drain wall.
- PPE.
- **Paper backup form** (Appendix A) and a pen.
- **A sheet of paper and a thick marker** for the Site ID marker card (section 8).
- Printed site list for the day (Site IDs, strata, coordinates).

## 3. Before you leave (every field day)

- [ ] Site list for the day printed, route clustered so the day does not cross Lagos twice.
- [ ] Phone charged, power bank charged, mobile data or offline mode checked.
- [ ] Form version on the phone matches the current version (`1.0`). Do not use an older or newer form.
- [ ] Phone GPS set to high accuracy. **Same device and same settings for the whole campaign.**
- [ ] Someone knows where you are going.

## 4. At each site (follow the order)

1. **Approach and check safety.** Look at traffic, water, structures. If unsafe, stop (section 1).
2. **Open a new form.** Type the Site ID exactly. Pick the stratum from your list. Pilot sites use `PILOT`.
3. **Find the segment centre.** Stand at the middle of the road segment (see section 5).
4. **Record GPS.** Wait until the accuracy number is good (aim for 10 m or better, **[DRAFT]**), then save. The form stores latitude, longitude and accuracy. If accuracy stays poor, save anyway. The validator will flag it for review. Do not retry many times to "get a better number".
5. **Fill in place details.** LGA, neighbourhood, road name or a landmark. No house numbers, no names of people.
6. **Road.** Pavement type, width (with method), potholes, cracking, rutting, edge failure.
7. **Choose the drain.** Right-hand drain first (section 5). If there is no drain, choose `none` and all drain questions are skipped.
8. **Drain.** Type, width, depth, obstruction, sediment, vegetation, waste, structure, flow, connectivity.
9. **Flood evidence.** Standing water, water marks, debris line, overtopping evidence, erosion, pavement water damage.
10. **Photos.** Use the iPhone Camera app, not the form (section 8). Then enter the photo count in the form.
11. **Notes.** Context only. No measurements, no names.
12. **Check and save.** Scroll through once. No blank answers without a reason. Save. Then move on.

Use the form's missing-data reason any time a value is blank (section 6). Never leave a gap.

## 5. Definitions you need on site

**Site.** One road segment and its drainage environment, one unique Site ID (PRD 4).

**Observation segment.** A stretch of road centred on the GPS point. Default length **50 m [DRAFT]**
(form field `obs_segment_length_m`). Everything you count or rate refers to this stretch. If the site physically
cannot give 50 m, use the real length and say why in notes.

**Which drain.** Stand at the segment centre, facing the direction of travel. Assess the right-hand drain.
Use the left-hand drain only if there is none on the right. **[DRAFT]** This fixed rule means the choice never
depends on which drain looks worse. If there is no drain at all, choose `none`.

**Worst accessible point.** Where you can safely see the drain at its most blocked inside the segment. Measure width
and depth at a representative accessible point.

## 6. Missing data (PRD section 19)

**A blank is never the same as zero.** If you cannot record a value, pick one reason code:

| Code | Use when |
|---|---|
| `inaccessible` | You cannot reach or see the thing |
| `not_applicable` | The thing does not exist here (for example, no flood evidence for photo 7) |
| `device_failure` | Phone, laser or GPS failed |
| `obscured` | Covered by water, debris, parked vehicles or vegetation |
| `refused_unsafe` | It would be unsafe to measure (traffic, flowing water, unstable structure) |
| `unknown` | None of the above fits. Explain in notes |

Outliers are never deleted in the field. Record what you measure. If a value looks odd, re-measure once, record the
measurement you trust, and say so in notes.

## 7. Variable guide

Full detail is in `docs/data_dictionary.csv`. Ordinal scores below are **[DRAFT]** anchors.

### 7.1 Road

| Variable | How to record |
|---|---|
| Pavement type | asphalt, concrete, interlock, unpaved, other. The surface under most of the carriageway in the segment |
| Road width (m) | Edge to edge of the driven surface at a representative point. Record the method (tape, laser, pacing, visual estimate). Never stand in the traffic lane |
| Pothole count | Every visible pothole on the carriageway in the segment |
| Largest pothole L / W / D (m) | Only the largest one you can measure safely. Depth is the deepest point below the surrounding surface. Not safe: `refused_unsafe` |
| Cracking 0-3 | 0 none. 1 isolated or hairline cracks, not linked. 2 several cracks, some linked, no loose pieces. 3 widespread linked cracking, or loose or missing pieces |
| Rutting 0-3 | 0 none. 1 slight wheel-path dip, visible by eye only. 2 clear dip where water would pond. 3 deep ruts, shoving or heave |
| Edge failure 0-3 | 0 none. 1 slight edge breaking. 2 broken or eroded edge along part of the segment. 3 edge collapsed or undercut, base exposed |

### 7.2 Drainage

| Variable | How to record |
|---|---|
| Drain type | open earth, masonry/concrete, covered, pipe/culvert, other |
| Width (m) | Clear internal width, from outside |
| Depth (m) | Invert (bottom) to top edge, from outside. If debris or water hides the bottom, measure to the visible surface and say so in notes |
| Obstruction 0-5 | Share of the cross-section blocked by **all materials together** at the worst accessible point. 0 none. 1 under 25%. 2 25-50%. 3 50-75%. 4 over 75%. 5 completely blocked. On an exact boundary choose the higher class **[DRAFT]** |
| Sediment 0-3 | Share of the cross-section filled by silt or soil. 0 none. 1 up to 25%. 2 over 25% to 50%. 3 over 50% |
| Vegetation 0-3 | Same scale, for plants in the drain |
| Solid waste 0-3 | Same scale, for waste in the drain |
| Structural condition 0-3 | 0 sound. 1 minor damage (hairline cracks, chips). 2 moderate (spalling, broken or missing slabs or lining, leaning), still works. 3 severe or failed (collapsed, long missing sections, not working) |
| Visible flow | none, slow, moderate, fast. Look from outside. **Never enter flowing water** |
| Connectivity | `connected_outlet` (you see it continue to an outlet, channel, culvert or another drain), `disconnected` (visibly ends, blocked or buried), `uncertain` |

Obstruction covers everything together, so it should not be lower than sediment, vegetation or waste on their own.
The validator warns if it is.

### 7.3 Flood evidence (physical evidence only)

| Variable | How to record |
|---|---|
| Standing water (0/1) | Water lying on the road, shoulder or in the drain at the time of your visit. Do not enter water to check |
| Standing water depth (m) | Only if safe. Measure from the edge with a rod. Otherwise `refused_unsafe` |
| Water mark (0/1) | A stain or line on walls, poles, kerbs, fences or ground that looks like an old water level. Photograph it |
| Sediment / debris line (0/1) | A line of silt, debris or waste left on the road, walls or plants |
| Drain overtopping evidence (0/1) | Only with physical signs: silt or debris outside the drain edge, flattened plants, scour channels leading away. **Never from reputation** |
| Erosion 0-3 | Flood-related scour of the shoulder, bank or ground beside the road or drain. 0 none. 1 surface scour. 2 gullies or cut channels. 3 deep gullies, undermined edges, large washout |
| Pavement water damage 0-3 | Damage that looks water-related. 0 none. 1 staining or light surface scouring. 2 loose aggregate or washed-out patches. 3 washed-out sections, exposed base, undermined slabs. If unsure of the cause, record the damage and say so in notes |

Edge failure (road) is damage to the pavement edge itself. Erosion (flood evidence) is scour of the ground beside it.

### 7.4 Local flood history (optional, see section 9)

## 8. Photographs (PRD section 7)

Photos are taken with the normal **iPhone Camera app**, not inside the form. This keeps the original files untouched
(PRD 7) and avoids unreliable photo upload from the iPhone browser. Photos are matched to sites later by script.

**One-time phone setting:** Settings, Camera, Formats, choose **Most Compatible** (saves JPEG, not HEIC). Keep Location Services
on for the Camera so each photo also carries its own GPS position.

**At each site, take the photos in this order (8 photos):**

| Order | Photo |
|---|---|
| 0 | **Marker card:** a sheet of paper with the Site ID written large (example `LAG-FI-P01`). Take it first, every time |
| 1 | Road approach |
| 2 | Pavement surface (worst cracking if any) |
| 3 | Drainage entrance |
| 4 | Drainage interior |
| 5 | Drainage outlet or connection |
| 6 | Surrounding terrain and land cover |
| 7 | Any visible flood-related damage or evidence |

- The marker card is what tells the script which photos belong to which site. Without it the photos cannot be linked. Never skip it.
- Take photos from a safe position. **No faces, no number plates, no private property details.**
- If a photo cannot be taken (drain covered, unsafe), skip it and write which one and why in `photo_exceptions`. If there is no flood evidence, skip photo 7 and say so.
- Enter `photo_count` (all photos you took at the site, marker card included). A full set is 8.
- Never delete or edit photos on the phone. The script copies photos to new names (`SITEID_00.jpg` for the marker card, then `SITEID_01.jpg` ... in the order taken) and never touches the originals.
- The script matches photos to sites by **time**. So: take all photos of a site in one go (a pause of more than 15 minutes starts a new site), fill the form during the same visit, and never change the phone's clock or time zone.
- **Photos and raw field data are never committed to GitHub before a privacy review** (the repo is public).

## 9. Local flood history (optional, off by default)

PRD 6.4 allows a reported flood history as context, kept separate from direct observation. PRD 20 says a consent
process is needed for interviews and local reports. **Until that consent wording is agreed, leave
`local_flood_history` and its source blank.** Never record names. Never mix it with what you observed yourself.

## 10. Replacing a site (PRD section 5)

A site may only be replaced if it is inaccessible, unsafe, not a valid road and drain site, or access is denied.

1. Replace it only from the **same stratum's** reserve list (`LAG-FI-Rnnn`).
2. Fill `replaces_site_id` and `replacement_reason` on the reserve site's form.
3. Note it in the site tracker. Never reuse the original ID.

## 11. End of day and form versioning

**End of day (same day):**
- [ ] Sync or export all forms. Copy to a second place (laptop plus cloud or a drive). Daily backup is in the PRD risk register.
- [ ] Copy all photos off the phone to the laptop (originals, unedited). Do not delete them from the phone until the backup is checked.
- [ ] Update the site tracker (status and date).

**Within 48 hours:**
- [ ] Run `python src/clean.py <export.csv>`. Fix typing mistakes with the owner's approval, and log every correction. Never "fix" a value silently.
- [ ] Check every valid site has a marker photo and a photo count, or a documented reason.

**Versioning.** The form must not change mid-campaign without a new version (PRD 6). Any change to the form or this
protocol after the pilot: new form version, new protocol version, reason written in the change log below.

## 12. Pilot review: what to check after the pilot

1. Time per site. Does 8-12 sites a day (PRD) hold?
2. Did two different people (or the same person twice) give the same score for the same site? If not, which anchor is unclear?
3. Which questions were skipped or always needed a missing code?
4. Is 50 m the right segment length? Is the right-hand-drain rule workable?
5. Was GPS accuracy good enough? Was 15 m too strict or too loose for the soft flag?
6. Did the photo set take too long?

One controlled revision is allowed after the pilot. Then freeze.

## 13. Open decisions (need the owner)

| # | Decision | Why it matters |
|---|---|---|
| 1 | Observation segment length (50 m proposed) | PRD says "defined segment" without a number |
| 2 | Pilot site IDs (`LAG-FI-Pnn`) and stratum value `PILOT` | Sampling frame comes after the pilot, tracker has no pilot rows |
| 3 | Fixed right-hand-drain rule and the `none` gate | Keeps drain choice objective |
| 4 | Edge failure vs erosion are two variables | PRD lists both names but only `erosion_score` in section 11 |
| 5 | Draft ordinal anchors and the boundary rule | Repeatability between observers |
| 6 | Local flood history: skip in the pilot? | Needs a consent process |
| 7 | Photo workflow change (Camera app + marker card instead of in-form photos) | Needed for iPhone; changes how PRD 7 photo linking is done |
| 8 | Extra context fields (weather at visit, rain in last 24 h) | Not in the PRD. Would change core variables, so needs a PRD version bump if approved |

## Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-30 | First draft from PRD v1.0 for the pilot |
| 0.2 | 2026-09-30 | Photos moved out of the form (iPhone): Camera app plus marker card, matched by script. Form fields photo_marker_taken, photo_count, photo_exceptions replace 7 photo fields. Before any field use |

---

## Appendix A. Paper backup form (write these down if the phone fails)

Copy each line onto paper in this order. The field names match `data_dictionary.csv`.

```
SITE: site_id ____  stratum ____  date ____  observer ____  GPS lat ____ lon ____ accuracy ____
PLACE: lga ____  neighbourhood ____  road/landmark ____  segment length (m) ____
ROAD: pavement_type ____  width_m ____ (method ____)  pothole_count ____
      largest pothole L ____ W ____ D ____   cracking 0-3 ____  rutting 0-3 ____  edge failure 0-3 ____
DRAIN: side (right/left/none) ____  type ____  width_m ____  depth_m ____
      obstruction 0-5 ____  sediment 0-3 ____  vegetation 0-3 ____  waste 0-3 ____
      structure 0-3 ____  flow (none/slow/moderate/fast) ____  connectivity ____
FLOOD EVIDENCE: standing water 0/1 ____ (depth ____)  water mark 0/1 ____  debris line 0/1 ____
      overtopping 0/1 ____  erosion 0-3 ____  pavement water damage 0-3 ____
PHOTOS (Camera app): marker card first ____  photo count ____  missing photos + why ____________
Missing values + reason code: ______________________
NOTES (context only): ______________________________________________
```
