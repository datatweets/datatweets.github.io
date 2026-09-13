"""Generate `thistlewood_orders_nested.json` -- the same real Thistlewood
order data, but with each order's line items embedded as a nested list of
structs instead of a separate `order_items` table, for Module 6 of "Polars
for Python Developers" (content/courses/polars-for-python-developers/
nested-data/).

This script never invents new data. It reads the real canonical
`thistlewood_orders.csv` and `thistlewood_order_items.csv` read-only and
re-shapes them -- one JSON record per order, with `line_items` as a real
list of structs built exactly from that order's real order_items rows. No
random draw, no injected messiness, no seed needed: this is a pure,
deterministic re-shaping of already-canonical data, the same "derive a new
variant FROM the base tables, never a fresh random draw" rule every later
Thistlewood dataset in this course follows.

**Subset: real Q1 2024 orders (2024-01-01 through 2024-03-31)**, the same
quarter -- and the same real order count, 792 -- Module 4's
`generate_orders_raw_variant.py` already used for its own "raw quarterly
export." Reusing the identical real subset keeps this course's derived
datasets consistent with each other and keeps the nested file a manageable
size for a lesson to load, print, and inspect directly.

Each output record has these real fields, matching the canonical source
tables exactly:
    order_id, order_date, customer_id, channel, status,
    line_items: [ { product_id, quantity, unit_price_at_sale }, ... ]

Real counts for this exact subset (verified by this script's own printed
output, and the numbers cited in Module 6's lessons):
    - 792 real Q1 2024 orders (order records)
    - 1,892 real total nested line items across those 792 orders
    - min 1, max 4, average 2.3889 real line items per order

Run once from the repo root:

    .venv-mlm-tutorials/bin/python static/datasets/thistlewood/generate_orders_nested.py

It writes:
    static/datasets/thistlewood/thistlewood_orders_nested.json

After running, copy the result to the repo root as a bare filename for
gate-verified reads (same convention as every other Thistlewood table):

    cp static/datasets/thistlewood/thistlewood_orders_nested.json thistlewood_orders_nested.json
"""
import json
import os

import polars as pl

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def _find(filename):
    """Prefer the repo-root bare-filename copy (used for gate-verified lesson
    reads); fall back to the hosted copy under this same directory."""
    root_copy = os.path.join(REPO_ROOT, filename)
    if os.path.exists(root_copy):
        return root_copy
    return os.path.join(HERE, filename)


def build_nested_records():
    orders = pl.read_csv(_find("thistlewood_orders.csv"))
    order_items = pl.read_csv(_find("thistlewood_order_items.csv"))

    q1_orders = orders.filter(
        (pl.col("order_date") >= "2024-01-01") & (pl.col("order_date") <= "2024-03-31")
    ).sort("order_id")

    q1_items = order_items.join(q1_orders.select("order_id"), on="order_id", how="inner")

    # One row per Q1 2024 order, with a real Python list of real line-item
    # dicts built directly from that order's own order_items rows -- no
    # aggregation, no derived values, every field copied byte-for-byte from
    # the canonical source tables.
    items_by_order = {}
    for row in q1_items.sort(["order_id", "order_item_id"]).iter_rows(named=True):
        items_by_order.setdefault(row["order_id"], []).append(
            {
                "product_id": row["product_id"],
                "quantity": row["quantity"],
                "unit_price_at_sale": row["unit_price_at_sale"],
            }
        )

    records = []
    line_item_counts = []
    for row in q1_orders.iter_rows(named=True):
        line_items = items_by_order.get(row["order_id"], [])
        line_item_counts.append(len(line_items))
        records.append(
            {
                "order_id": row["order_id"],
                "order_date": row["order_date"],
                "customer_id": row["customer_id"],
                "channel": row["channel"],
                "status": row["status"],
                "line_items": line_items,
            }
        )

    stats = {
        "n_orders": len(records),
        "n_line_items": sum(line_item_counts),
        "min_line_items": min(line_item_counts),
        "max_line_items": max(line_item_counts),
        "avg_line_items": round(sum(line_item_counts) / len(line_item_counts), 4),
    }
    return records, stats


def main():
    records, stats = build_nested_records()

    out_path = os.path.join(HERE, "thistlewood_orders_nested.json")
    with open(out_path, "w") as f:
        json.dump(records, f, indent=None)

    print(f"orders (records):        {stats['n_orders']}")
    print(f"total nested line items:  {stats['n_line_items']}")
    print(f"min line items per order: {stats['min_line_items']}")
    print(f"max line items per order: {stats['max_line_items']}")
    print(f"avg line items per order: {stats['avg_line_items']}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
