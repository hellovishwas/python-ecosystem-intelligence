import time
from datetime import date, timedelta

import pandas as pd
import requests


# ============================================================
# PATHS
# ============================================================

input_path = "data/raw/pypi_packages_raw.csv"
output_path = "data/raw/pypi_download_history.csv"

history_url = "https://pypistats.org/api/packages/{}/overall"

headers = {"Accept": "application/json"}


# ============================================================
# LOAD PACKAGES
# ============================================================

packages_df = pd.read_csv(input_path)

package_names = packages_df["package_name"].dropna().drop_duplicates().tolist()

print("=" * 60)
print("PyPI Historical Download Collector")
print("=" * 60)

print("Packages found:", len(package_names))


# ============================================================
# DATE RANGE
# ============================================================

end_date = date.today()
start_date = end_date - timedelta(days=179)

print("Start date:", start_date)
print("End date:", end_date)


# ============================================================
# COLLECT HISTORY
# ============================================================

history_rows = []

for index, package in enumerate(package_names, start=1):
    print(f"\n[{index}/{len(package_names)}] Collecting: {package}")

    try:
        response = requests.get(
            history_url.format(package),
            headers=headers,
            params={"mirrors": "false"},
            timeout=60,
        )

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("History failed:", response.status_code)
            continue

        data = response.json()

        # PyPI Stats returns downloads as a LIST
        downloads = data.get("data", [])

        package_rows = 0

        for item in downloads:
            if not isinstance(item, dict):
                continue

            download_date = item.get("date")
            download_count = item.get("downloads")

            if not download_date:
                continue

            if str(start_date) <= download_date <= str(end_date):
                history_rows.append(
                    {
                        "package_name": package,
                        "date": download_date,
                        "downloads": download_count,
                    }
                )

                package_rows += 1

        print("Historical rows:", package_rows)

        time.sleep(0.5)

    except requests.exceptions.RequestException as error:
        print("Request error:", error)


# ============================================================
# CREATE DATAFRAME
# ============================================================

history_df = pd.DataFrame(history_rows)


# ============================================================
# CLEAN DATA
# ============================================================

if not history_df.empty:
    history_df = history_df.drop_duplicates(subset=["package_name", "date"])

    history_df["date"] = pd.to_datetime(history_df["date"])

    history_df["downloads"] = pd.to_numeric(history_df["downloads"], errors="coerce")

    history_df = history_df.sort_values(["package_name", "date"]).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

history_df.to_csv(output_path, index=False)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 60)
print("COLLECTION FINISHED")
print("=" * 60)

print("Packages requested:", len(package_names))

print("Historical rows:", len(history_df))

print("Dataset shape:", history_df.shape)

print(
    "Unique packages:",
    history_df["package_name"].nunique() if not history_df.empty else 0,
)

if not history_df.empty:
    print(
        "Date range:",
        history_df["date"].min().date(),
        "to",
        history_df["date"].max().date(),
    )

print("\nSaved to:", output_path)

print("\nFirst 10 rows:")

print(history_df.head(10).to_string(index=False))


missing_packages = sorted(set(package_names) - set(history_df["package_name"]))

print("\nPackages without historical data:")
print(missing_packages)
print("Missing count:", len(missing_packages))
