"""Generate `thistlewood_products_raw.csv` -- a deliberately messy variant of
the canonical Thistlewood Goods product catalog, for Module 5 of "Polars for
Python Developers" (content/courses/polars-for-python-developers/
text-and-categories/).

This script never touches the canonical CSV. It reads
`thistlewood_products.csv` read-only, copies it, and reintroduces realistic
text messiness on top of that copy, using a fixed seed (42, same convention
as Module 1's `generate_thistlewood_data.py` and Module 4's
`generate_orders_raw_variant.py`) so the exact injected-error counts are
reproducible.

Perturbations applied to a copy of the 60-row canonical table (exact counts,
seed 42):
    - 14 rows: `category` rewritten with a case/whitespace inconsistency --
      chosen with a seeded random draw, then cycled through three real
      variant shapes in seed-order:
          lowercase          e.g. "Kitchen"  -> "kitchen"
          uppercase          e.g. "Bath"     -> "BATH"
          trailing whitespace e.g. "Bedding" -> "Bedding "
      (the other 46 rows keep the canonical category string exactly)
    -  6 rows: `product_name` rewritten with a real whitespace/casing
       inconsistency, drawn independently of the 14 category rows --
          3 rows -> a doubled internal space plus leading/trailing whitespace
                    (e.g. "Modern Saucepan"  -> "  Modern  Saucepan  ")
          3 rows -> a casing inconsistency (all-lowercase or all-uppercase
                    instead of the canonical Title Case)
    -  1 row: one canonical product appended a second time, as a near-
       duplicate catalog entry with a real respelled `product_name` (an
       extra hyphen/space variant of the same product) -- a realistic
       "product re-entered under a slightly different name" bug, and a real
       normalization target for Lesson 2's regex work. This is what pushes
       the file from 60 to 61 total rows.

`category` values in the untouched 46 rows, and `product_name` values in the
untouched 53 non-appended rows, are byte-identical to the canonical file --
this dataset's messiness is deliberately limited to these three problems.

The module's job (Lessons 1-5) is normalizing this file back into a table
whose category set and per-category aggregates match the real canonical
`thistlewood_products.csv`.

Run once from the repo root:

    .venv-mlm-tutorials/bin/python static/datasets/thistlewood/generate_products_raw_variant.py

It writes:
    static/datasets/thistlewood/thistlewood_products_raw.csv

After running, copy the result to the repo root as a bare filename for
gate-verified reads (same convention as every other Thistlewood table):

    cp static/datasets/thistlewood/thistlewood_products_raw.csv thistlewood_products_raw.csv
"""
import os

import numpy as np
import polars as pl

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

CATEGORY_MESS_COUNT = 14
NAME_MESS_COUNT = 6


def _find(filename):
    """Prefer the repo-root bare-filename copy (used for gate-verified lesson
    reads); fall back to the hosted copy under this same directory."""
    root_copy = os.path.join(REPO_ROOT, filename)
    if os.path.exists(root_copy):
        return root_copy
    return os.path.join(HERE, filename)


def apply_category_messiness(rows, idx):
    """Cycle through three real variant shapes, in the order the seeded draw
    produced the indices -- lowercase, uppercase, trailing whitespace."""
    variant_cycle = ["lower", "upper", "trailing_space"]
    counts = {"lower": 0, "upper": 0, "trailing_space": 0}
    for j, i in enumerate(idx):
        variant = variant_cycle[j % 3]
        cat = rows[i]["category"]
        if variant == "lower":
            rows[i]["category"] = cat.lower()
        elif variant == "upper":
            rows[i]["category"] = cat.upper()
        else:
            rows[i]["category"] = cat + " "
        counts[variant] += 1
    return counts


def apply_name_messiness(rows, idx):
    """First half of the drawn indices get a whitespace inconsistency,
    second half get a casing inconsistency."""
    half = len(idx) // 2
    whitespace_idx, casing_idx = idx[:half], idx[half:]
    for i in whitespace_idx:
        name = rows[i]["product_name"]
        doubled = name.replace(" ", "  ")
        rows[i]["product_name"] = f"  {doubled}  "
    for j, i in enumerate(casing_idx):
        name = rows[i]["product_name"]
        rows[i]["product_name"] = name.lower() if j % 2 == 0 else name.upper()
    return len(whitespace_idx), len(casing_idx)


def build_dupe_row(rows, used_idx, rng):
    """Append one canonical row again, respelled with a real hyphen/space
    variant of its product_name -- a near-duplicate catalog entry."""
    remaining = [i for i in range(len(rows)) if i not in used_idx]
    dupe_source = int(rng.choice(remaining))
    dupe = dict(rows[dupe_source])
    name = dupe["product_name"]
    if "-" in name:
        respelled = name.replace("-", " ")
    else:
        words = name.split(" ")
        mid = len(words) // 2
        respelled = " ".join(words[:mid]) + "-" + " ".join(words[mid:])
    dupe["product_name"] = respelled
    return dupe_source, dupe


def main():
    canonical = pl.read_csv(_find("thistlewood_products.csv"))
    rows = canonical.to_dicts()
    n = len(rows)
    rng = np.random.default_rng(SEED)

    cat_idx = sorted(int(i) for i in rng.choice(n, size=CATEGORY_MESS_COUNT, replace=False))

    remaining_for_names = [i for i in range(n) if i not in cat_idx]
    name_idx = sorted(int(i) for i in rng.choice(remaining_for_names, size=NAME_MESS_COUNT, replace=False))

    used_idx = set(cat_idx) | set(name_idx)
    dupe_source_idx, dupe_row = build_dupe_row(rows, used_idx, rng)

    cat_counts = apply_category_messiness(rows, cat_idx)
    ws_count, case_count = apply_name_messiness(rows, name_idx)

    all_rows = rows + [dupe_row]
    result = pl.DataFrame(
        all_rows,
        schema={
            "product_id": pl.Utf8,
            "product_name": pl.Utf8,
            "category": pl.Utf8,
            "subcategory": pl.Utf8,
            "unit_price": pl.Float64,
            "cost": pl.Float64,
            "supplier": pl.Utf8,
        },
    )

    out_path = os.path.join(HERE, "thistlewood_products_raw.csv")
    result.write_csv(out_path)

    print(f"canonical (clean) table: {n} rows, {canonical.width} cols")
    print(f"  category-messy rows:          {len(cat_idx)}  (lower={cat_counts['lower']}, "
          f"upper={cat_counts['upper']}, trailing_space={cat_counts['trailing_space']})")
    print(f"  product_name-messy rows:      {len(name_idx)}  (whitespace={ws_count}, casing={case_count})")
    print(f"  appended near-duplicate row:  1  (respelled from {rows[dupe_source_idx]['product_id']}"
          f" \"{rows[dupe_source_idx]['product_name']}\")")
    print(f"    -> respelled as: \"{dupe_row['product_name']}\"")
    print(f"wrote thistlewood_products_raw.csv  {result.height} rows  {result.width} cols")
    print()
    print("category-messy row detail:")
    for i in cat_idx:
        print(f"  {rows[i]['product_id']:6s} {canonical['category'][i]!r:>12s} -> {rows[i]['category']!r}")
    print()
    print("product_name-messy row detail:")
    for i in name_idx:
        print(f"  {rows[i]['product_id']:6s} {canonical['product_name'][i]!r} -> {rows[i]['product_name']!r}")


if __name__ == "__main__":
    main()
