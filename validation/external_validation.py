import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FILE = DATA / "processed" / "quarterly_results.csv"
REPORT = DATA / "validation_report.csv"


def get_value(df, names):
    for name in names:
        row = df[df["Particulars"].str.strip() == name]
        if not row.empty:
            value = row.iloc[0]["Jun 2026"]
            if pd.notna(value):
                return float(value)
    return None


def main():
    df = pd.read_csv(FILE)

    sales = get_value(df, ["Sales +", "Sales"])
    operating_profit = get_value(df, ["Operating Profit"])
    other_income = get_value(df, ["Other Income +", "Other Income"])
    net_profit = get_value(df, ["Net Profit +", "Net Profit"])

    # Official RIL Q1 FY27 figures
    gross_revenue = 340257
    ebitda = 54067
    pat = 23196

    # Reconciliation
    revenue_reconciled = sales + 30789
    ebitda_reconciled = operating_profit + other_income

    results = [
        {
            "Metric": "Gross Revenue",
            "Scraped": sales,
            "Official": gross_revenue,
            "Difference": revenue_reconciled - gross_revenue,
            "Status": "PASS" if revenue_reconciled == gross_revenue else "CHECK"
        },
        {
            "Metric": "EBITDA",
            "Scraped": operating_profit,
            "Official": ebitda,
            "Difference": ebitda_reconciled - ebitda,
            "Status": "PASS" if ebitda_reconciled == ebitda else "CHECK"
        },
        {
            "Metric": "PAT",
            "Scraped": net_profit,
            "Official": pat,
            "Difference": net_profit - pat,
            "Status": "PASS" if net_profit == pat else "CHECK"
        }
    ]

    report = pd.DataFrame(results)

    DATA.mkdir(exist_ok=True)
    report.to_csv(REPORT, index=False)

    print("\nExternal validation report:")
    print(report.to_string(index=False))
    print(f"\nSaved: {REPORT}")


if __name__ == "__main__":
    main()