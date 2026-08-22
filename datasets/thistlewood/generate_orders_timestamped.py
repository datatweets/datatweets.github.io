"""Generate `thistlewood_orders_timestamped.csv` -- the canonical Thistlewood
Goods order data with a new `order_timestamp_utc` column added, for Module 9
of "Polars for Python Developers"
(content/courses/polars-for-python-developers/time-series-and-date-workflows/).

This script never touches the canonical CSVs. It reads `thistlewood_orders.csv`
read-only (all 6,000 rows, unfiltered) and adds one new column: a full
ISO-8601 UTC datetime combining that row's real `order_date` with a
synthesized time-of-day, weighted by `channel` so the result looks like a
plausible order-history export rather than uniform noise:

- `web` orders draw from the widest hour distribution -- some early-morning
  and late-night browsing, but weighted toward the evening (18:00-23:00),
  when online shoppers are typically active.
- `store` orders draw from a narrower daytime distribution (09:00-20:00),
  peaking around midday/early afternoon, matching normal retail hours.
- `phone` orders draw from the narrowest distribution (09:00-17:00), matching
  a staffed call-center's business hours.

Every hour weight below is a fixed, hand-authored integer array (not itself
random) so the *shape* of each channel's distribution is exactly reproducible
by inspection; the only randomness is which hour/minute/second each of the
6,000 rows lands on, drawn from a single `numpy.random.default_rng(42)`
reused consistently for the whole run (same convention as Module 1's own
`generate_thistlewood_data.py` and Module 4's `generate_orders_raw_variant.py`)
so re-running this script reproduces the exact same file byte-for-byte.

The minute and second within the chosen hour are drawn uniformly (0-59) from
the same RNG, in row order, so nothing about the file's byte content depends
on anything but the fixed seed and the fixed per-channel hour weights below.

Output columns: order_id, order_date, customer_id, channel, status,
order_timestamp_utc -- the same 5 canonical columns plus one new one, an
ISO-8601 UTC datetime string with a "Z" suffix, e.g. "2024-01-01T14:23:07Z".

Run once from the repo root:

    .venv-mlm-tutorials/bin/python static/datasets/thistlewood/generate_orders_timestamped.py

It writes:
    static/datasets/thistlewood/thistlewood_orders_timestamped.csv

After running, copy the result to the repo root as a bare filename for
gate-verified reads (same convention as every other Thistlewood table):

    cp static/datasets/thistlewood/thistlewood_orders_timestamped.csv thistlewood_orders_timestamped.csv
"""
import os

import numpy as np
import polars as pl

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def _find(filename):
    root_copy = os.path.join(REPO_ROOT, filename)
    if os.path.exists(root_copy):
        return root_copy
    return os.path.join(HERE, filename)


# Fixed, hand-authored per-channel hour weights (24 integers each, index 0-23).
# Not randomly generated -- these are the deliberate "shape" of each channel's
# time-of-day distribution. Normalized to probabilities before sampling.
WEB_HOUR_WEIGHTS = [
    1, 1, 1, 1, 1, 2,        # 00-05: quiet overnight, still present
    3, 4, 5, 6, 7, 8,        # 06-11: morning ramp-up
    8, 8, 8, 8, 9, 10,       # 12-17: steady daytime browsing
    12, 14, 15, 14, 10, 6,   # 18-23: evening peak, tapering toward midnight
]
STORE_HOUR_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,   # 00-08: closed
    8, 10, 12,                  # 09-11: opening ramp
    14, 13, 12,                 # 12-14: midday peak
    11, 10, 9,                  # 15-17: afternoon
    7, 5, 3,                    # 18-20: closing hours
    0, 0, 0,                    # 21-23: closed
]
PHONE_HOUR_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,   # 00-08: closed
    10, 14, 16,                 # 09-11: opening ramp
    14, 16, 14,                 # 12-14: midday peak
    12, 8, 6,                   # 15-17: afternoon, winding down
    0, 0, 0, 0, 0, 0,           # 18-23: closed
]

CHANNEL_WEIGHTS = {
    "web": np.array(WEB_HOUR_WEIGHTS, dtype=float),
    "store": np.array(STORE_HOUR_WEIGHTS, dtype=float),
    "phone": np.array(PHONE_HOUR_WEIGHTS, dtype=float),
}
CHANNEL_PROBS = {
    channel: weights / weights.sum() for channel, weights in CHANNEL_WEIGHTS.items()
}


def build_timestamped(orders: pl.DataFrame) -> pl.DataFrame:
    rng = np.random.default_rng(SEED)
    channels = orders["channel"].to_list()
    dates = orders["order_date"].to_list()

    timestamps = []
    for channel, order_date in zip(channels, dates):
        probs = CHANNEL_PROBS[channel]
        hour = int(rng.choice(24, p=probs))
        minute = int(rng.integers(0, 60))
        second = int(rng.integers(0, 60))
        timestamps.append(f"{order_date}T{hour:02d}:{minute:02d}:{second:02d}Z")

    return orders.with_columns(pl.Series("order_timestamp_utc", timestamps))


def main():
    orders = pl.read_csv(_find("thistlewood_orders.csv"))
    result = build_timestamped(orders)

    out_path = os.path.join(HERE, "thistlewood_orders_timestamped.csv")
    result.write_csv(out_path)

    hour_of_day = result.select(
        pl.col("order_timestamp_utc").str.slice(11, 2).cast(pl.Int64).alias("hour")
    )["hour"]
    print(f"wrote thistlewood_orders_timestamped.csv  {result.height} rows  {result.width} cols")
    print(f"channel counts: {dict(zip(*orders['channel'].value_counts().to_dict().values()))}")
    print(f"hour range: {hour_of_day.min()}-{hour_of_day.max()}")
    print(f"mean hour: {round(hour_of_day.mean(), 2)}")


if __name__ == "__main__":
    main()
