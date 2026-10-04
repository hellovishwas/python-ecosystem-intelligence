import time
import requests
import pandas as pd

packages = [
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "seaborn",
    "plotly",
    "scikit-learn",
    "tensorflow",
    "torch",
    "transformers",
    "xgboost",
    "lightgbm",
    "statsmodels",
    "keras",
    "opencv-python",
    "nltk",
    "spacy",
    "django",
    "flask",
    "fastapi",
    "requests",
    "beautifulsoup4",
    "selenium",
    "scrapy",
    "streamlit",
    "jupyter",
    "jupyterlab",
    "pydantic",
    "sqlalchemy",
    "pytest",
    "rich",
    "click",
    "typer",
    "pillow",
    "sympy",
    "networkx",
    "gradio",
    "langchain",
    "openai",
    "polars",
    "pyarrow",
    "dask",
    "pyspark",
    "catboost",
    "sentence-transformers",
    "huggingface-hub",
    "datasets",
    "ollama",
    "litellm",
    "celery",
    "redis",
    "boto3",
    "docker",
    "uvicorn",
    "httpx",
    "pydantic-settings",
    "pytest-asyncio",
    "black",
]

stats_url = "https://pypistats.org/api/packages/{}/recent"

metadata_url = "https://pypi.org/pypi/{}/json"

headers = {"Accept": "application/json"}

rows = []

for package in packages:
    print(f"Collecting: {package}")

    try:
        stats_response = requests.get(
            stats_url.format(package), headers=headers, timeout=30
        )

        metadata_response = requests.get(metadata_url.format(package), timeout=30)

        if stats_response.status_code != 200:
            print("Stats failed:", stats_response.status_code)
            continue

        if metadata_response.status_code != 200:
            print("Metadata failed:", metadata_response.status_code)
            continue

        stats = stats_response.json()
        metadata = metadata_response.json()

        info = metadata["info"]

        rows.append(
            {
                "package_name": info.get("name"),
                "version": info.get("version"),
                "summary": info.get("summary"),
                "license": info.get("license"),
                "requires_python": info.get("requires_python"),
                "downloads_last_day": stats["data"]["last_day"],
                "downloads_last_week": stats["data"]["last_week"],
                "downloads_last_month": stats["data"]["last_month"],
            }
        )

        print(
            "Day:",
            stats["data"]["last_day"],
            "| Week:",
            stats["data"]["last_week"],
            "| Month:",
            stats["data"]["last_month"],
        )

        time.sleep(0.5)

    except requests.exceptions.RequestException as error:
        print("Request error:", error)

df = pd.DataFrame(rows)

print("\n" + "=" * 60)
print("Packages collected:", len(df))
print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nTop packages by monthly downloads:")
print(
    df[["package_name", "downloads_last_month"]]
    .sort_values("downloads_last_month", ascending=False)
    .head(10)
    .to_string(index=False)
)

output_path = "data/raw/pypi_packages_raw.csv"

df.to_csv(output_path, index=False)

print("\nSaved to:", output_path)
