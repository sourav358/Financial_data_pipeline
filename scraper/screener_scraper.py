import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

URL = "https://www.screener.in/company/RELIANCE/consolidated/"

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"


def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def scrape(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = []

    for i, table in enumerate(soup.find_all("table")):
        rows = []

        for tr in table.find_all("tr"):
            row = [
                cell.get_text(" ", strip=True)
                for cell in tr.find_all(["th", "td"])
            ]
            if row:
                rows.append(row)

        if rows:
            heading = table.find_previous(
                ["h1", "h2", "h3", "h4", "h5", "h6"]
            )

            tables.append({
                "table_index": i,
                "section": heading.get_text(" ", strip=True)
                if heading else None,
                "rows": rows
            })

    return tables


def save(html, tables):
    RAW.mkdir(parents=True, exist_ok=True)
    time = datetime.now().strftime("%Y%m%d_%H%M%S")

    html_file = RAW / f"screener_{time}.html"
    json_file = RAW / f"screener_tables_{time}.json"

    html_file.write_text(html, encoding="utf-8")
    json_file.write_text(
        json.dumps(tables, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return html_file, json_file


def main():
    print("Downloading Screener data...")

    html = fetch_page()
    tables = scrape(html)
    html_file, json_file = save(html, tables)

    print(f"Tables found: {len(tables)}")
    print(f"HTML : {html_file}")
    print(f"JSON : {json_file}")

    for t in tables:
        print(f"- {t['section']}")


if __name__ == "__main__":
    main()