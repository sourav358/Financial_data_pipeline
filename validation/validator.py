import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed"


def check_file(file):
    df = pd.read_csv(file)

    print(f"\nChecking: {file.name}")
    print("-" * 40)

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    # Basic checks
    if "Particulars" in df.columns:
        print("✓ Particulars column")

    if not df.columns.duplicated().any():
        print("✓ No duplicate columns")

    if not df.duplicated().any():
        print("✓ No duplicate rows")

    periods = [c for c in df.columns if c != "Particulars"]
    print(f"✓ Periods found: {len(periods)}")


def check_profit_loss():
    file = DATA / "profit_loss.csv"

    if not file.exists():
        print("❌ profit_loss.csv not found")
        return

    df = pd.read_csv(file)

    # Convert rows into a dictionary
    data = df.set_index("Particulars")

    print("\nProfit & Loss checks")
    print("-" * 40)

    for period in data.columns:

        try:
            sales = data.loc["Sales +", period]
            expenses = data.loc["Expenses +", period]
            operating_profit = data.loc[
                "Operating Profit", period
            ]

            if pd.notna(sales) and pd.notna(expenses):
                calculated = sales - expenses

                if pd.isna(operating_profit):
                    continue

                if abs(calculated - operating_profit) < 1:
                    print(f"✓ {period}: Sales - Expenses = Operating Profit")
                else:
                    print(
                        f"⚠ {period}: Operating profit mismatch "
                        f"({calculated} vs {operating_profit})"
                    )

        except KeyError:
            print(f"⚠ Missing P&L row for {period}")


def check_opm():
    file = DATA / "profit_loss.csv"
    if not file.exists():
        return

    df = pd.read_csv(file)
    data = df.set_index("Particulars")

    print("\nOPM checks")
    print("-" * 40)

    tolerance = 1.0

    for period in data.columns:
        try:
            sales = pd.to_numeric(data.loc["Sales +", period], errors="coerce")
            profit = pd.to_numeric(
                data.loc["Operating Profit", period],
                errors="coerce"
            )
            reported = pd.to_numeric(
                data.loc["OPM %", period],
                errors="coerce"
            )

            if pd.isna(sales) or pd.isna(profit) or pd.isna(reported):
                continue

            calculated = profit / sales * 100
            difference = calculated - reported

            if abs(difference) < tolerance:
                print(
                    f"✓ {period}: OPM consistent "
                    f"({calculated:.2f}% vs {reported:.2f}%, "
                    f"diff {difference:.2f})"
                )
            else:
                print(
                    f"⚠ {period}: OPM mismatch "
                    f"({calculated:.2f}% vs {reported:.2f}%, "
                    f"diff {difference:.2f})"
                )

        except KeyError:
            print(f"⚠ Missing OPM data for {period}")
    file = DATA / "profit_loss.csv"

    if not file.exists():
        return

    df = pd.read_csv(file)
    data = df.set_index("Particulars")

    print("\nOPM checks")
    print("-" * 40)

    for period in data.columns:

        try:
            sales = data.loc["Sales +", period]
            operating_profit = data.loc[
                "Operating Profit", period
            ]
            opm = data.loc["OPM %", period]

            if pd.isna(sales) or pd.isna(operating_profit):
                continue

            calculated = operating_profit / sales * 100

            if pd.isna(opm):
                continue

            if abs(calculated - opm) < 1:
                print(f"✓ {period}: OPM is consistent")
            else:
                print(
                    f"⚠ {period}: OPM mismatch "
                    f"({calculated:.2f}% vs {opm}%)"
                )

        except KeyError:
            print(f"⚠ Missing OPM data for {period}")


def main():

    print("=" * 50)
    print("FINANCIAL DATA VALIDATION")
    print("=" * 50)

    files = list(DATA.glob("*.csv"))

    if not files:
        print("❌ No processed CSV files found.")
        return

    # Structural validation
    for file in files:
        check_file(file)

    # Financial validation
    check_profit_loss()
    check_opm()

    print("\nValidation completed.")


if __name__ == "__main__":
    main()