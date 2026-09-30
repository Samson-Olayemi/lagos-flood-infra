"""Schema and QC validation for the field table (PRD sections 18 and 19).

This module CHECKS data. It never edits, fills or "fixes" values. A blank is never
turned into zero (PRD 19). Every problem is reported; the owner decides what to do.

Input : a CSV export of the field form (one row per site) + docs/data_dictionary.csv
Output: a table of issues (printed, and optionally saved as CSV). Exit code 1 if any
        ERROR exists, so the pipeline fails loudly (PRD 18: "pipeline fails on unknown
        categories or malformed units").

Severity
    error   : breaks the schema or a hard rule (unknown category, missing required value,
              value outside hard limits, duplicate site_id, missing value without reason).
    warning : needs a human look (outside soft limits, poor GPS, odd combinations).

Usage:
    python src/clean.py path/to/export.csv
    python src/clean.py path/to/export.csv --issues-out results/qc_issues.csv
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

DICTIONARY_DEFAULT = Path("docs/data_dictionary.csv")
MISSING_CODES = {"inaccessible", "not_applicable", "device_failure", "obscured", "refused_unsafe", "unknown"}
FORM_ONLY_FIELDS = {"site_location"}          # geopoint; split into latitude/longitude/gps_accuracy_m
NO_VALUE_TYPES = {"photo"}                    # photo columns hold a file name; only presence is checked
SYSTEM_COLUMNS = {"instanceID", "uuid", "deprecatedID", "instanceName", "__version__", "_version_"}


def tidy_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Make a Kobo/ODK export match the dictionary.

    Exports may prefix a column with its section name ('sec_1_road/pothole_count').
    Keep only the part after the last '/'. Only renames columns. No values are touched.
    """
    out = df.rename(columns=lambda c: str(c).split("/")[-1])
    if out.columns.duplicated().any():
        dups = sorted(set(out.columns[out.columns.duplicated()]))
        raise ValueError(f"Column names clash after removing section prefixes: {dups}")
    return out


# ----------------------------------------------------------------------------- helpers
def load_dictionary(path: Path = DICTIONARY_DEFAULT) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def allowed_keys(allowed: str) -> set[str]:
    return {p.partition("=")[0].strip() for p in allowed.split("|")} if allowed else set()


def is_blank(v) -> bool:
    return v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() == ""


def norm(v) -> str:
    """'2.0' -> '2' so a spreadsheet round-trip does not create false errors."""
    s = str(v).strip()
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
    except ValueError:
        pass
    return s


def relevant(rule: str, row: pd.Series) -> bool:
    """Evaluate the dictionary's simple 'field==value' / 'field!=value' rule.

    Matches XLSForm behaviour: a blank parent is never equal to a value.
    """
    if not rule:
        return True
    m = re.fullmatch(r"\s*([a-z0-9_]+)\s*(==|!=)\s*([A-Za-z0-9_]+)\s*", rule)
    if not m:
        raise ValueError(f"Unsupported relevant_if rule: {rule!r}")
    field, op, value = m.groups()
    parent = "" if field not in row or is_blank(row[field]) else norm(row[field])
    return (parent == value) if op == "==" else (parent != value)


# ----------------------------------------------------------------------------- core
def validate_field_table(df: pd.DataFrame, dictionary: pd.DataFrame) -> pd.DataFrame:
    issues: list[dict] = []

    def log(site, field, severity, rule, detail):
        issues.append({"site_id": site, "field": field, "severity": severity, "rule": rule, "detail": detail})

    # --- schema level: columns
    expected = set()
    for _, d in dictionary.iterrows():
        if d["field_name"] in FORM_ONLY_FIELDS:
            continue
        expected.add(d["field_name"])
        if d["requirement"] == "value_or_reason":
            expected.add(f"{d['field_name']}_missing")
    missing_cols = sorted(expected - set(df.columns))
    for c in missing_cols:
        log("", c, "error", "missing_column", "Column is in the data dictionary but not in the export.")
    for c in sorted(set(df.columns) - expected):
        if not c.startswith("_") and c not in SYSTEM_COLUMNS:   # Kobo/ODK system columns
            log("", c, "warning", "unknown_column", "Column is not in the data dictionary.")

    # --- site_id uniqueness (never reuse an ID)
    if "site_id" in df.columns:
        dup = df["site_id"][df["site_id"].duplicated(keep=False) & df["site_id"].notna()].unique()
        for s in dup:
            log(s, "site_id", "error", "duplicate_site_id", "Site ID appears more than once. IDs are never reused.")

    # --- row level
    for _, row in df.iterrows():
        site = "" if is_blank(row.get("site_id")) else str(row["site_id"])
        for _, d in dictionary.iterrows():
            f = d["field_name"]
            if f in FORM_ONLY_FIELDS or f not in df.columns:
                continue
            if not relevant(d["relevant_if"], row):
                continue
            req, dtype = d["requirement"], d["data_type"]
            val = row[f]
            reason = row.get(f"{f}_missing") if req == "value_or_reason" else None

            if is_blank(val):
                if req == "always":
                    log(site, f, "error", "missing_required", "Required value is blank.")
                elif req == "value_or_reason":
                    if is_blank(reason):
                        log(site, f, "error", "missing_no_reason", "Blank with no missing-data reason (PRD 19).")
                    elif norm(reason) not in MISSING_CODES:
                        log(site, f, "error", "bad_missing_code", f"Unknown missing-data code {reason!r}.")
                continue

            if req == "value_or_reason" and not is_blank(reason):
                log(site, f, "warning", "value_and_reason", "Has a value AND a missing-data reason. Check which is right.")
            if dtype in NO_VALUE_TYPES:
                continue

            v = norm(val)
            if dtype in ("categorical", "ordinal", "binary"):
                if v not in allowed_keys(d["allowed_values"]):
                    log(site, f, "error", "unknown_category", f"{v!r} is not an allowed value.")
            elif dtype in ("integer", "decimal"):
                try:
                    x = float(v)
                except ValueError:
                    log(site, f, "error", "not_numeric", f"{v!r} is not a number.")
                    continue
                if dtype == "integer" and not x.is_integer():
                    log(site, f, "error", "not_integer", f"{v!r} must be a whole number.")
                if d["hard_min"] and x < float(d["hard_min"]):
                    log(site, f, "error", "below_hard_min", f"{x} < {d['hard_min']} {d['unit']}".strip())
                if d["hard_max"] and x > float(d["hard_max"]):
                    log(site, f, "error", "above_hard_max", f"{x} > {d['hard_max']} {d['unit']}".strip())
                if d["soft_min"] and x < float(d["soft_min"]):
                    log(site, f, "warning", "below_soft_min", f"{x} < {d['soft_min']} {d['unit']}: review".strip())
                if d["soft_max"] and x > float(d["soft_max"]):
                    log(site, f, "warning", "above_soft_max", f"{x} > {d['soft_max']} {d['unit']}: review".strip())
            elif dtype == "date":
                if pd.isna(pd.to_datetime(v, errors="coerce")):
                    log(site, f, "error", "bad_date", f"{v!r} is not a valid date.")
            elif dtype == "string" and d["regex"]:
                if not re.fullmatch(d["regex"], v):
                    log(site, f, "error", "bad_format", f"{v!r} does not match the required format.")

        # ---- cross-field checks
        def num(col):
            v = row.get(col)
            try:
                return None if is_blank(v) else float(norm(v))
            except ValueError:
                return None

        if not is_blank(row.get("site_id")) and str(row["site_id"]).startswith("LAG-FI-R"):
            for col in ("replaces_site_id", "replacement_reason"):
                if col in df.columns and is_blank(row.get(col)):
                    log(site, col, "error", "reserve_needs_replacement_log", "Reserve site must say what it replaces and why (PRD 5).")
        pc = num("photo_count")
        if pc is not None and pc < 8 and "photo_exceptions" in df.columns and is_blank(row.get("photo_exceptions")):
            log(site, "photo_exceptions", "warning", "photo_exception_missing",
                "Fewer than 8 photos and no explanation of which are missing (PRD 26).")
        if not is_blank(row.get("road_width_m")) and "road_width_method" in df.columns and is_blank(row.get("road_width_method")):
            log(site, "road_width_method", "error", "method_missing", "Road width has a value but no measurement method (PRD 6.2).")
        obs = num("obstruction_score")
        comps = [num(c) for c in ("sediment_score", "vegetation_score", "waste_score")]
        if obs == 0 and any(c is not None and c >= 2 for c in comps):
            log(site, "obstruction_score", "warning", "obstruction_inconsistent",
                "Obstruction is 0 but sediment/vegetation/waste is 2 or more. Check.")
        if num("pothole_count") == 0 and any(num(c) is not None for c in
                                              ("pothole_largest_length_m", "pothole_largest_width_m", "pothole_largest_depth_m")):
            log(site, "pothole_count", "warning", "pothole_inconsistent", "Pothole count is 0 but pothole dimensions are filled.")

    return pd.DataFrame(issues, columns=["site_id", "field", "severity", "rule", "detail"])


# ----------------------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export_csv", type=Path)
    ap.add_argument("--dictionary", type=Path, default=DICTIONARY_DEFAULT)
    ap.add_argument("--issues-out", type=Path, default=None)
    args = ap.parse_args()

    df = tidy_columns(pd.read_csv(args.export_csv, dtype=str, keep_default_na=False))
    issues = validate_field_table(df, load_dictionary(args.dictionary))

    n_err = int((issues["severity"] == "error").sum())
    n_warn = int((issues["severity"] == "warning").sum())
    print(f"{len(df)} site rows checked: {n_err} errors, {n_warn} warnings")
    if len(issues):
        print(issues.to_string(index=False))
    if args.issues_out:
        args.issues_out.parent.mkdir(parents=True, exist_ok=True)
        issues.to_csv(args.issues_out, index=False)
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
