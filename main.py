import subprocess
import sys


def run_step(name, command):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable] + command
    )

    if result.returncode != 0:
        print(f"\n❌ {name} failed.")
        sys.exit(result.returncode)

    print(f"✓ {name} completed.")


def main():

    print("=" * 60)
    print("FINANCIAL DATA PIPELINE")
    print("=" * 60)

    # 1. Scraping
    run_step(
        "STEP 1: SCRAPING",
        ["scraper/screener_scraper.py"]
    )

    # 2. Cleaning
    run_step(
        "STEP 2: DATA CLEANING",
        ["cleaning/cleaner.py"]
    )

    # 3. Internal validation
    run_step(
        "STEP 3: INTERNAL VALIDATION",
        ["validation/validator.py"]
    )

    # 4. External validation
    run_step(
        "STEP 4: EXTERNAL VALIDATION",
        ["validation/external_validation.py"]
    )

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nGenerated data:")
    print("  data/raw/")
    print("  data/processed/")
    print("  data/validation_report.csv")

    print("\nTo start dashboard:")
    print("  python -m http.server 8000")

    print("\nThen open:")
    print("  http://localhost:8000/dashboard/")


if __name__ == "__main__":
    main()