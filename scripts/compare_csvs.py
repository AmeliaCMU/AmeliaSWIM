#!/usr/bin/env python3
"""
compare_csv_dirs.py

Iterate over two directory trees, load every matching CSV into Pandas
DataFrames, and report whether they are identical.

Usage:
    python compare_csv_dirs.py /path/to/dirA /path/to/dirB [-i] [-v]

Arguments
---------
dirA, dirB : str
    Root directories containing the CSV files to compare.  The script walks
    each tree; any file with the same **relative** path and “.csv” suffix is
    compared.

Options
-------
-i, --ignore-order
        Ignore row order and index order when comparing (sorts both frames).
-v, --verbose
        Print *all* identical files; otherwise only differences / missing files
        are shown.

Exit status
-----------
0 if every matched CSV is identical (per the chosen options), else 1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import pandas.testing as pdt


def csv_files(root: Path) -> dict[str, Path]:
    """Map relative CSV path → absolute Path under *root*."""
    return {
        p.relative_to(root).as_posix(): p
        for p in root.rglob("*.csv")
        if p.is_file()
    }


def load_csv(path: Path) -> pd.DataFrame:
    """Read a CSV with default options; tweak here if needed."""
    return pd.read_csv(path)


def frames_equal(
    a: pd.DataFrame, b: pd.DataFrame, ignore_order: bool = False
) -> bool:
    """True if DataFrames are equal (optionally ignoring row/index order)."""
    if ignore_order:
        a = a.sort_index(axis=1).sort_values(list(a.columns)).reset_index(drop=True)
        b = b.sort_index(axis=1).sort_values(list(b.columns)).reset_index(drop=True)

    try:
        # `check_like=True` ignores column order but *not* row order
        pdt.assert_frame_equal(a, b, check_like=True, check_dtype=False)
        return True
    except AssertionError:
        return False


def compare_dirs(dir_a: Path, dir_b: Path, ignore_order: bool, verbose: bool) -> bool:
    files_a = csv_files(dir_a)
    files_b = csv_files(dir_b)

    all_ok = True

    # Check for files present in only one directory
    only_a = sorted(set(files_a) - set(files_b))
    only_b = sorted(set(files_b) - set(files_a))

    for rel in only_a:
        all_ok = False
        print(f"[MISSING] {rel} — present only in {dir_a}")

    for rel in only_b:
        all_ok = False
        print(f"[MISSING] {rel} — present only in {dir_b}")

    # Compare common files
    for rel in sorted(set(files_a) & set(files_b)):
        df_a = load_csv(files_a[rel])
        df_b = load_csv(files_b[rel])

        if frames_equal(df_a, df_b, ignore_order):
            if verbose:
                print(f"[OK] {rel}")
        else:
            all_ok = False
            print(f"[DIFF] {rel}")

    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare CSV contents across two directory trees."
    )
    parser.add_argument("--dirA", type=Path, help="First directory")
    parser.add_argument("--dirB", type=Path, help="Second directory")
    parser.add_argument(
        "-i",
        "--ignore-order",
        action="store_true",
        help="Ignore row/index order when comparing",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Also list identical files",
    )

    args = parser.parse_args()

    ok = compare_dirs(args.dirA, args.dirB, args.ignore_order, args.verbose)
    print(
        f"\n{'All files are identical' if ok else 'Some files differ'}"
    )
    print(f"Compared {args.dirA} and {args.dirB}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
