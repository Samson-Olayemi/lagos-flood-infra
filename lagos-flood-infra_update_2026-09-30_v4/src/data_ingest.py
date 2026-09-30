"""Ingest a KoboToolbox field export: validate it and link photos to sites.

Input
    --export   CSV export of the field form (one row per site).
    --photos   (optional) folder with the ORIGINAL iPhone photos as JPEG
               (iPhone: Settings > Camera > Formats > Most Compatible).

Output (default folder data/interim, all local, none of it is committed to GitHub)
    field_sites_validated.csv    the export with tidy column names and numbers typed.
                                 No value is changed. A blank stays blank, never zero.
    field_sites_validated.gpkg   the same sites as points, CRS EPSG:4326 (WGS84).
    qc_issues.csv                every problem found by src/clean.py.
    photo_link_report.csv        which photos were matched to which site, and flags.
    data/photos/linked/          COPIES named SITEID_00.jpg (marker card), SITEID_01.jpg ...
                                 in the order taken. Originals are never touched.

How photos are matched (a HEURISTIC that must be checked on the pilot)
    1. Read the time each photo was taken from its EXIF data.
    2. Photos taken close together (gap of 15 minutes or less) form one visit.
    3. A visit belongs to the site whose form start/end time (plus 20 minutes either side)
       overlaps it.
    4. The first photo of a visit should be the marker card (paper with the Site ID).
       The script cannot read it. Look at the first photo of every site by eye.
    Anything unclear (no photos, several visits, count differs from the form) is flagged.
    Assumption: the phone clock and time zone were correct and unchanged (Lagos, UTC+1).

Exit code 1 if the validator finds any ERROR (PRD 18), unless --allow-errors is given.

Usage
    python src/data_ingest.py --export path/to/export.csv
    python src/data_ingest.py --export path/to/export.csv --photos path/to/original_photos
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import pandas as pd

try:
    import clean
except ImportError:  # run as a module from the repo root
    from src import clean

LOCAL_TZ = "Africa/Lagos"
PHOTO_SUFFIXES = {".jpg", ".jpeg"}


# ----------------------------------------------------------------------------- typing
def type_columns(df: pd.DataFrame, dictionary: pd.DataFrame) -> pd.DataFrame:
    """Turn numeric columns into numbers. Blank becomes NaN (missing), never 0."""
    out = df.copy()
    numeric_types = {"integer", "decimal", "binary", "ordinal"}
    for _, d in dictionary.iterrows():
        f = d["field_name"]
        if f in out.columns and d["data_type"] in numeric_types:
            out[f] = pd.to_numeric(out[f], errors="coerce")
    return out


# ----------------------------------------------------------------------------- times
def _to_local_naive(value) -> pd.Timestamp:
    """Kobo times may carry an offset (+01:00). Convert to Lagos local time, drop the offset."""
    if value is None or str(value).strip() == "":
        return pd.NaT
    try:
        ts = pd.Timestamp(str(value).strip())
    except (ValueError, TypeError):
        return pd.NaT
    if ts.tzinfo is not None:
        ts = ts.tz_convert(LOCAL_TZ).tz_localize(None)
    return ts


def read_photo_times(folder: Path) -> pd.DataFrame:
    """Read the time each JPEG was taken (EXIF). Photos without a time are listed with NaT."""
    from PIL import Image  # imported here so --help works without Pillow

    rows = []
    for p in sorted(folder.rglob("*")):
        if p.suffix.lower() not in PHOTO_SUFFIXES:
            continue
        taken = pd.NaT
        try:
            with Image.open(p) as img:
                exif = img.getexif()
                raw = exif.get_ifd(0x8769).get(36867) or exif.get(306)  # DateTimeOriginal, else DateTime
            if raw:
                taken = pd.to_datetime(str(raw), format="%Y:%m:%d %H:%M:%S", errors="coerce")
        except Exception as exc:  # unreadable file: report it, do not stop
            print(f"WARNING: cannot read {p.name}: {exc}", file=sys.stderr)
        rows.append({"path": str(p), "taken": taken})
    return pd.DataFrame(rows, columns=["path", "taken"])


# ----------------------------------------------------------------------------- linking
def link_photos(sites: pd.DataFrame, photos: pd.DataFrame, gap_min: int = 15, pad_min: int = 20):
    """Return (report, assignments). assignments maps site_id -> list of photo paths in time order."""
    timed = photos.dropna(subset=["taken"]).sort_values("taken").reset_index(drop=True)
    timed["visit"] = (timed["taken"].diff() > pd.Timedelta(minutes=gap_min)).cumsum()
    visits = timed.groupby("visit").agg(first=("taken", "min"), last=("taken", "max"), n=("path", "count"))

    pad = pd.Timedelta(minutes=pad_min)
    report, chosen = [], {}
    for _, s in sites.iterrows():
        site = str(s.get("site_id", ""))
        start, end = _to_local_naive(s.get("start_time")), _to_local_naive(s.get("end_time"))
        flags, visit_id, n, first, last = [], None, 0, pd.NaT, pd.NaT
        if pd.isna(start) or pd.isna(end):
            flags.append("form_time_missing")
        else:
            hit = visits[(visits["last"] >= start - pad) & (visits["first"] <= end + pad)]
            if len(hit) == 0:
                flags.append("no_photos_found")
            elif len(hit) > 1:
                flags.append("several_photo_visits_match")
            else:
                visit_id = hit.index[0]
                n, first, last = int(hit.iloc[0]["n"]), hit.iloc[0]["first"], hit.iloc[0]["last"]
                claimed = pd.to_numeric(s.get("photo_count"), errors="coerce")
                if pd.notna(claimed) and int(claimed) != n:
                    flags.append(f"count_differs(form={int(claimed)},found={n})")
        chosen[site] = visit_id
        report.append({"site_id": site, "visit": visit_id, "n_photos": n, "first_photo": first,
                       "last_photo": last, "flags": ";".join(flags)})
    report = pd.DataFrame(report)

    # A visit claimed by two sites cannot be trusted for either.
    shared = report["visit"].dropna()[report["visit"].dropna().duplicated(keep=False)].unique()
    for v in shared:
        report.loc[report["visit"] == v, "flags"] += ";visit_shared_between_sites"

    def status_of(r) -> str:
        if pd.isna(r["visit"]) or "visit_shared_between_sites" in r["flags"]:
            return "needs_review"           # nothing safe to copy
        if r["flags"] == "":
            return "linked"
        if all(f.startswith("count_differs") for f in r["flags"].split(";")):
            return "linked_check_count"     # copied, but photo count differs from the form
        return "needs_review"

    report["status"] = report.apply(status_of, axis=1)
    assignments = {
        r["site_id"]: timed.loc[timed["visit"] == r["visit"], "path"].tolist()
        for _, r in report.iterrows() if r["status"] in ("linked", "linked_check_count")
    }
    return report, assignments


def copy_linked(assignments: dict[str, list[str]], out_dir: Path) -> int:
    """Copy (never move) photos to SITEID_00.jpg (marker card), SITEID_01.jpg ... in time order."""
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for site, paths in assignments.items():
        for seq, src in enumerate(paths):
            shutil.copy2(src, out_dir / f"{site}_{seq:02d}.jpg")
            n += 1
    return n


# ----------------------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--export", required=True, type=Path)
    ap.add_argument("--photos", type=Path, default=None)
    ap.add_argument("--dictionary", type=Path, default=clean.DICTIONARY_DEFAULT)
    ap.add_argument("--out-dir", type=Path, default=Path("data/interim"))
    ap.add_argument("--photos-out", type=Path, default=Path("data/photos/linked"))
    ap.add_argument("--gap-min", type=int, default=15, help="minutes of silence that start a new visit")
    ap.add_argument("--pad-min", type=int, default=20, help="minutes added either side of the form window")
    ap.add_argument("--allow-errors", action="store_true", help="write outputs even if the validator found errors")
    ap.add_argument("--dry-run", action="store_true", help="do not copy photos")
    args = ap.parse_args()

    dictionary = clean.load_dictionary(args.dictionary)
    raw = clean.tidy_columns(pd.read_csv(args.export, dtype=str, keep_default_na=False))
    issues = clean.validate_field_table(raw, dictionary)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    issues.to_csv(args.out_dir / "qc_issues.csv", index=False)
    n_err = int((issues["severity"] == "error").sum())
    n_warn = int((issues["severity"] == "warning").sum())
    print(f"{len(raw)} sites read: {n_err} errors, {n_warn} warnings (see qc_issues.csv)")
    if n_err and not args.allow_errors:
        print("Stopped: fix the errors (with the owner's approval, and log every correction) or use --allow-errors.")
        return 1

    typed = type_columns(raw, dictionary)
    typed.to_csv(args.out_dir / "field_sites_validated.csv", index=False)

    ok = typed.dropna(subset=["latitude", "longitude"]) if {"latitude", "longitude"} <= set(typed.columns) else typed.iloc[0:0]
    if len(ok):
        try:
            import geopandas as gpd

            gdf = gpd.GeoDataFrame(ok, geometry=gpd.points_from_xy(ok["longitude"], ok["latitude"]), crs="EPSG:4326")
            gdf.to_file(args.out_dir / "field_sites_validated.gpkg", layer="sites", driver="GPKG")
        except ImportError:
            print("geopandas not installed: GeoPackage skipped.", file=sys.stderr)

    if args.photos:
        photos = read_photo_times(args.photos)
        print(f"{len(photos)} JPEG photos found, {int(photos['taken'].isna().sum())} without a readable time")
        report, assignments = link_photos(raw, photos, args.gap_min, args.pad_min)
        report.to_csv(args.out_dir / "photo_link_report.csv", index=False)
        print(report["status"].value_counts().to_string())
        if not args.dry_run:
            print(f"{copy_linked(assignments, args.photos_out)} photos copied to {args.photos_out}")
        print("Now look at the first photo of every linked site: it must be the marker card.")
    return 1 if (n_err and args.allow_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
