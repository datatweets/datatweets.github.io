"""Generate `thistlewood_orders_raw.csv` -- a deliberately messy variant of the
canonical Thistlewood Goods order data, for Module 4 of "Polars for Python
Developers" (content/courses/polars-for-python-developers/cleaning-and-validation/).

This script never touches the canonical CSVs. It reads them read-only, builds
a derived, order-level "raw quarterly export" table (Q1 2024 orders joined to
customer contact info and to an order-level quantity/price rollup from the
real order-line data), and then reintroduces realistic messiness on top of
that COPY, using a fixed seed (42, same convention as Module 1's own
`generate_thistlewood_data.py`) so the exact injected-error counts are
reproducible.

The base (pre-perturbation) table:
    order_id, order_date, customer_id, email, city, channel, status,
    quantity, unit_price
- One row per real Q1 2024 order (2024-01-01..2024-03-31) from the canonical
  `thistlewood_orders.csv` (792 orders, every status/channel included, since
  this is meant to look like an unfiltered raw export).
- `email` / `city` joined in from the canonical `thistlewood_customers.csv`.
- `quantity` = the real total units across that order's line items;
  `unit_price` = real total revenue / real total quantity for that order,
  both rolled up from the canonical `thistlewood_order_items.csv`.

Perturbations applied to a copy of that base table (exact counts, seed 42):
    -  9 rows: city set to null
    -  6 rows: email set to null (independent draw from the city rows --
       may occasionally land on the same row as a null city, which is a
       realistic "we lost this customer's contact info entirely" case)
    - 12 rows: order_date rewritten to a non-ISO string format --
        8 rows -> "MM/DD/YYYY" (e.g. "03/15/2024")
        4 rows -> "DD-Mon-YYYY" (e.g. "15-Mar-2024")
      (the other 780 rows keep the canonical "YYYY-MM-DD" string)
    -  5 rows: a negative numeric value, a real data-entry-error pattern --
        3 rows -> quantity negated
        2 rows -> unit_price negated
    -  3 order_ids: duplicated as an exact extra row appended to the file
       (a realistic double-submitted-order bug), so the raw file has 792 + 3
       = 795 rows total even though only 792 distinct orders exist.

The module's job (Lessons 1-6) is cleaning this file back into a table that
matches the real canonical data on every one of these checks.

Run once from the repo root:

    .venv-mlm-tutorials/bin/python static/datasets/thistlewood/generate_orders_raw_variant.py

It writes:
    static/datasets/thistlewood/thistlewood_orders_raw.csv

After running, copy the result to the repo root as a bare filename for
gate-verified reads (same convention as every other Thistlewood table):

    cp static/datasets/thistlewood/thistlewood_orders_raw.csv thistlewood_orders_raw.csv
"""
import datetime as dt
import os

import numpy as np
import polars as pl

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# Canonical source files. Prefer the repo-root bare-filename copies (used for
# gate-verified lesson reads); fall back to the hosted copies under this same
# directory for order_items, which doesn't have a repo-root copy.
def _find(filename):
    root_copy = os.path.join(REPO_ROOT, filename)
    if os.path.exists(root_copy):
        return root_copy
    return os.path.join(HERE, filename)


MONTH_ABBR = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def to_mmddyyyy(iso_date: str) -> str:
    d = dt.date.fromisoformat(iso_date)
    return f"{d.month:02d}/{d.day:02d}/{d.year:04d}"


def to_dd_mon_yyyy(iso_date: str) -> str:
    d = dt.date.fromisoformat(iso_date)
    return f"{d.day:02d}-{MONTH_ABBR[d.month - 1]}-{d.year:04d}"


def build_base_table() -> pl.DataFrame:
    """Real Q1 2024 orders, joined to customer contact info and an
    order-level quantity/price rollup from the real order-line data. This is
    the clean starting point every perturbation below is applied on top of."""
    customers = pl.read_csv(_find("thistlewood_customers.csv"))
    orders = pl.read_csv(_find("thistlewood_orders.csv"))
    order_items = pl.read_csv(_find("thistlewood_order_items.csv"))

    q1_orders = orders.filter(
        (pl.col("order_date") >= "2024-01-01") & (pl.col("order_date") <= "2024-03-31")
    )

    rollup = (
        q1_orders.join(order_items, on="order_id", how="inner")
        .group_by("order_id")
        .agg(
            pl.col("quantity").sum().alias("quantity"),
            (pl.col("quantity") * pl.col("unit_price_at_sale")).sum().alias("_revenue"),
        )
        .with_columns((pl.col("_revenue") / pl.col("quantity")).round(2).alias("unit_price"))
        .select("order_id", "quantity", "unit_price")
    )

    base = (
        q1_orders.join(rollup, on="order_id", how="inner")
        .join(customers.select("customer_id", "email", "city"), on="customer_id", how="inner")
        .select(
            "order_id", "order_date", "customer_id", "email", "city",
            "channel", "status", "quantity", "unit_price",
        )
        .sort(["order_date", "order_id"])
    )
    return base


def apply_messiness(base: pl.DataFrame) -> pl.DataFrame:
    rng = np.random.default_rng(SEED)
    n = base.height
    rows = base.to_dicts()

    # --- 1. Null cities (9 rows) and null emails (6 rows), independent draws ---
    null_city_idx = set(int(i) for i in rng.choice(n, size=9, replace=False))
    null_email_idx = set(int(i) for i in rng.choice(n, size=6, replace=False))
    for i in null_city_idx:
        rows[i]["city"] = None
    for i in null_email_idx:
        rows[i]["email"] = None

    # --- 2. Inconsistent date-string formats (12 rows: 8 MM/DD/YYYY, 4 DD-Mon-YYYY) ---
    remaining_for_dates = [i for i in range(n) if i not in null_city_idx and i not in null_email_idx]
    date_pool = rng.choice(remaining_for_dates, size=12, replace=False)
    mmddyyyy_idx = set(int(i) for i in date_pool[:8])
    ddmonyyyy_idx = set(int(i) for i in date_pool[8:])
    for i in mmddyyyy_idx:
        rows[i]["order_date"] = to_mmddyyyy(rows[i]["order_date"])
    for i in ddmonyyyy_idx:
        rows[i]["order_date"] = to_dd_mon_yyyy(rows[i]["order_date"])

    # --- 3. Negative quantities/prices (5 rows: 3 negative quantity, 2 negative unit_price) ---
    used_so_far = null_city_idx | null_email_idx | mmddyyyy_idx | ddmonyyyy_idx
    remaining_for_negatives = [i for i in range(n) if i not in used_so_far]
    negative_pool = rng.choice(remaining_for_negatives, size=5, replace=False)
    neg_qty_idx = set(int(i) for i in negative_pool[:3])
    neg_price_idx = set(int(i) for i in negative_pool[3:])
    for i in neg_qty_idx:
        rows[i]["quantity"] = -abs(rows[i]["quantity"])
    for i in neg_price_idx:
        rows[i]["unit_price"] = -abs(rows[i]["unit_price"])

    # --- 4. Duplicate order_ids (3 order_ids, each appended once more, exact copy) ---
    used_so_far |= neg_qty_idx | neg_price_idx
    remaining_for_dupes = [i for i in range(n) if i not in used_so_far]
    dupe_source_idx = rng.choice(remaining_for_dupes, size=3, replace=False)
    dupe_rows = [dict(rows[int(i)]) for i in dupe_source_idx]

    all_rows = rows + dupe_rows
    result = pl.DataFrame(
        all_rows,
        schema={
            "order_id": pl.Utf8,
            "order_date": pl.Utf8,
            "customer_id": pl.Utf8,
            "email": pl.Utf8,
            "city": pl.Utf8,
            "channel": pl.Utf8,
            "status": pl.Utf8,
            "quantity": pl.Int64,
            "unit_price": pl.Float64,
        },
    )

    stats = {
        "base_rows": n,
        "null_city_rows": len(null_city_idx),
        "null_email_rows": len(null_email_idx),
        "bad_date_rows_mmddyyyy": len(mmddyyyy_idx),
        "bad_date_rows_ddmonyyyy": len(ddmonyyyy_idx),
        "negative_quantity_rows": len(neg_qty_idx),
        "negative_price_rows": len(neg_price_idx),
        "duplicate_order_ids": len(dupe_rows),
        "total_rows": result.height,
    }
    return result, stats


def main():
    base = build_base_table()
    messy, stats = apply_messiness(base)

    out_path = os.path.join(HERE, "thistlewood_orders_raw.csv")
    messy.write_csv(out_path)

    print(f"base (clean) table: {stats['base_rows']} rows, {base.width} cols")
    print(f"  null city rows:              {stats['null_city_rows']}")
    print(f"  null email rows:             {stats['null_email_rows']}")
    print(f"  bad-date rows (MM/DD/YYYY):  {stats['bad_date_rows_mmddyyyy']}")
    print(f"  bad-date rows (DD-Mon-YYYY): {stats['bad_date_rows_ddmonyyyy']}")
    print(f"  negative-quantity rows:      {stats['negative_quantity_rows']}")
    print(f"  negative-price rows:         {stats['negative_price_rows']}")
    print(f"  duplicated order_ids:        {stats['duplicate_order_ids']}")
    print(f"wrote thistlewood_orders_raw.csv  {stats['total_rows']} rows  {messy.width} cols")


if __name__ == "__main__":
    main()
