"""Generate `thistlewood_orders_timestamps_raw.csv` -- a Q1-2024 subset of
`thistlewood_orders_timestamped.csv` with its `order_timestamp_utc` column
reformatted into several inconsistent raw-export-style string representations,
for Module 9 of "Polars for Python Developers" (Lesson 2's parsing exercise:
content/courses/polars-for-python-developers/time-series-and-date-workflows/).

This script never touches the canonical CSVs, and never re-derives a
timestamp. It reads `thistlewood_orders_timestamped.csv` read-only, takes the
same Q1-2024 (2024-01-01..2024-03-31) subset convention Module 4's
`thistlewood_orders_raw.csv` used (792 real orders), and reformats each row's
already-generated `order_timestamp_utc` value into one of four raw-export
string forms -- the underlying real timestamp (year, month, day, hour,
minute, second) is never changed, only how it's written as a string:

    1. ISO-8601 with a "Z" suffix        "2024-01-15T14:23:07Z"
    2. ISO-8601 with an explicit offset  "2024-01-15T14:23:07+00:00"
    3. MM/DD/YYYY HH:MM AM/PM            "01/15/2024 02:23 PM"  (seconds dropped)
    4. Seconds-omitted ISO               "2024-01-15T14:23"

Which of the four forms each row gets is a deterministic, seeded draw:
`numpy.random.default_rng(42)` (same seed convention as every other
Thistlewood generator), drawing once per row with fixed weights
(0.35 / 0.25 / 0.25 / 0.15) so re-running this script reproduces the exact
same file, and the exact same per-format row count, every time.

Output columns: order_id, order_date, customer_id, channel, status,
order_timestamp_utc -- the same 6 columns as
`thistlewood_orders_timestamped.csv`, restricted to the Q1-2024 subset, with
`order_timestamp_utc` restyled into one of the four formats above.

Run once from the repo root (after `generate_orders_timestamped.py` has
already produced its output):

    .venv-mlm-tutorials/bin/python static/datasets/thistlewood/generate_orders_timestamps_raw.py

It writes:
    static/datasets/thistlewood/thistlewood_orders_timestamps_raw.csv

After running, copy the result to the repo root as a bare filename for
gate-verified reads (same convention as every other Thistlewood table):

    cp static/datasets/thistlewood/thistlewood_orders_timestamps_raw.csv thistlewood_orders_timestamps_raw.csv
"""
import datetime as dt
import os

import numpy as np
import polars as pl

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

FORMAT_NAMES = [
    "iso_z",            # 2024-01-15T14:23:07Z
    "iso_offset",        # 2024-01-15T14:23:07+00:00
    "mm_dd_yyyy_ampm",   # 01/15/2024 02:23 PM
    "iso_no_seconds",    # 2024-01-15T14:23
]
FORMAT_WEIGHTS = [0.35, 0.25, 0.25, 0.15]


def _find(filename):
    root_copy = os.path.join(REPO_ROOT, filename)
    if os.path.exists(root_copy):
        return root_copy
    return os.path.join(HERE, filename)


def restyle(ts_str: str, fmt_name: str) -> str:
    """ts_str is the clean 'YYYY-MM-DDTHH:MM:SSZ' string produced by
    generate_orders_timestamped.py. Parse it and re-render in one of the
    four raw-export string forms -- the underlying moment never changes."""
    parsed = dt.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
    if fmt_name == "iso_z":
        return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")
    if fmt_name == "iso_offset":
        return parsed.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    if fmt_name == "mm_dd_yyyy_ampm":
        return parsed.strftime("%m/%d/%Y %I:%M %p")
    if fmt_name == "iso_no_seconds":
        return parsed.strftime("%Y-%m-%dT%H:%M")
    raise ValueError(fmt_name)


def build_raw(timestamped: pl.DataFrame) -> tuple[pl.DataFrame, dict]:
    q1 = timestamped.filter(
        (pl.col("order_date") >= "2024-01-01") & (pl.col("order_date") <= "2024-03-31")
    ).sort(["order_date", "order_id"])

    rng = np.random.default_rng(SEED)
    fmt_choices = rng.choice(len(FORMAT_NAMES), size=q1.height, p=FORMAT_WEIGHTS)

    ts_values = q1["order_timestamp_utc"].to_list()
    restyled = [
        restyle(ts, FORMAT_NAMES[choice_idx])
        for ts, choice_idx in zip(ts_values, fmt_choices)
    ]

    result = q1.with_columns(pl.Series("order_timestamp_utc", restyled))

    counts = {name: int((fmt_choices == i).sum()) for i, name in enumerate(FORMAT_NAMES)}
    return result, counts


def main():
    timestamped = pl.read_csv(_find("thistlewood_orders_timestamped.csv"))
    result, counts = build_raw(timestamped)

    out_path = os.path.join(HERE, "thistlewood_orders_timestamps_raw.csv")
    result.write_csv(out_path)

    print(f"wrote thistlewood_orders_timestamps_raw.csv  {result.height} rows  {result.width} cols")
    for name, n in counts.items():
        print(f"  {name}: {n}")
    print(f"  total: {sum(counts.values())}")


if __name__ == "__main__":
    main()
