import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"


def latest_json():
    files = list(RAW.glob("screener_tables_*.json"))
    if not files:
        raise FileNotFoundError("No raw JSON found.")
    return max(files, key=lambda x: x.stat().st_mtime)


def clean_value(x):
    if not isinstance(x, str):
        return x

    x = x.replace(",", "").strip()

    if x in ("", "-", "--", "NA", "N/A"):
        return None

    if x.endswith("%"):
        try:
            return float(x[:-1])
        except ValueError:
            return x

    try:
        return float(x)
    except ValueError:
        return x


def make_dataframe(table):
    rows = table["rows"]

    # Find the row containing financial periods
    header_index = next(
        (
            i for i, row in enumerate(rows)
            if any(
                "Mar " in str(x) or
                "Jun " in str(x) or
                "Sep " in str(x) or
                "Dec " in str(x)
                for x in row
            )
        ),
        None
    )

    if header_index is None:
        return None

    header = rows[header_index]

    # Remove empty first header
    if not header[0]:
        header[0] = "Particulars"

    data = rows[header_index + 1:]

    width = len(header)

    data = [
        row[:width] + [None] * max(0, width - len(row))
        for row in data
    ]

    df = pd.DataFrame(data, columns=header)

    df = df.map(clean_value)

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    return df


def main():

    OUT.mkdir(parents=True, exist_ok=True)

    with open(latest_json(), "r", encoding="utf-8") as f:
        tables = json.load(f)

    # Only these financial datasets are required
    targets = {
        "Quarterly Results": "quarterly_results.csv",
        "Profit & Loss": "profit_loss.csv",
        "Balance Sheet": "balance_sheet.csv",
        "Cash Flows": "cash_flow.csv",
        "Ratios": "ratios.csv"
    }

    for section, filename in targets.items():

        # Find the first useful table for this section
        table = next(
            (
                t for t in tables
                if t["section"] == section
                and make_dataframe(t) is not None
            ),
            None
        )

        if table is None:
            print(f"WARNING: {section} not found")
            continue

        df = make_dataframe(table)

        output = OUT / filename
        df.to_csv(output, index=False)

        print(f"✓ {section} -> {filename}")


if __name__ == "__main__":
    main()