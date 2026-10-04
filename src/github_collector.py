import os
import json
import time

import requests
import pandas as pd
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout


load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

url = "https://api.github.com/search/repositories"

date_windows = [
    ("2020-01-01", "2020-06-30"),
    ("2020-07-01", "2020-12-31"),
    ("2021-01-01", "2021-06-30"),
    ("2021-07-01", "2021-12-31"),
    ("2022-01-01", "2022-06-30"),
    ("2022-07-01", "2022-12-31"),
    ("2023-01-01", "2023-06-30"),
    ("2023-07-01", "2023-12-31"),
    ("2024-01-01", "2024-06-30"),
    ("2024-07-01", "2024-12-31"),
    ("2025-01-01", "2025-06-30"),
    ("2025-07-01", "2025-12-31"),
    ("2026-01-01", "2026-06-30"),
    ("2026-07-01", "2026-12-31"),
]

categories = [
    "",
    "topic:machine-learning",
    "topic:data-science",
    "topic:web",
    "topic:artificial-intelligence",
    "topic:deep-learning",
    "topic:natural-language-processing",
    "topic:computer-vision",
    "topic:data-engineering",
    "topic:cybersecurity",
    "topic:devops",
    "topic:cloud",
    "topic:automation",
    "topic:database",
    "topic:django",
    "topic:flask",
    "topic:fastapi",
    "topic:scientific-computing",
    "topic:robotics",
    "topic:finance",
]

checkpoint_file = "data/raw/github_checkpoint.csv"
completed_file = "data/raw/github_completed_queries.json"
output_path = "data/raw/github_repositories_raw.csv"


if os.path.exists(checkpoint_file):
    checkpoint_df = pd.read_csv(checkpoint_file)
    all_repositories = checkpoint_df.to_dict("records")
    print("Loaded checkpoint:", len(all_repositories))
else:
    all_repositories = []


if os.path.exists(completed_file):
    with open(completed_file, "r") as f:
        completed_queries = set(json.load(f))
    print("Completed queries loaded:", len(completed_queries))
else:
    completed_queries = set()


for start_date, end_date in date_windows:
    for category in categories:
        print("\n" + "=" * 60)
        print(f"Window: {start_date} to {end_date}")
        print("Category:", category if category else "general")

        params = {
            "q": f"language:python created:{start_date}..{end_date} {category} fork:false",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
        }

        query = params["q"]

        print("QUERY:", query)

        if query in completed_queries:
            print("Already completed. Skipping...")
            continue

        request_success = False

        while True:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)

                print("Status:", response.status_code)

                if response.status_code == 200:
                    request_success = True
                    break

                if response.status_code == 403:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

                    wait_time = max(reset_time - int(time.time()) + 5, 5)

                    print(f"Rate limit reached. Waiting {wait_time} seconds...")

                    time.sleep(wait_time)
                    continue

                print("Error:", response.status_code)
                print(response.text[:500])
                break

            except ConnectionError:
                print("Connection error. Retrying in 5 seconds...")
                time.sleep(5)

            except Timeout:
                print("Request timed out. Retrying in 5 seconds...")
                time.sleep(5)

        if not request_success:
            print("Query failed. Moving to next query.")
            continue

        data = response.json()

        repositories = data.get("items", [])

        print("Repositories:", len(repositories))

        all_repositories.extend(repositories)

        checkpoint_df = pd.DataFrame(all_repositories)

        checkpoint_df.to_csv(checkpoint_file, index=False)

        print("Checkpoint saved.")

        completed_queries.add(query)

        with open(completed_file, "w") as f:
            json.dump(list(completed_queries), f, indent=2)

        print("Query marked as completed.")

        time.sleep(2)


print("\n" + "=" * 60)
print("Collection finished.")
print("Raw repositories collected:", len(all_repositories))


rows = []

for repo in all_repositories:
    rows.append(
        {
            "owner": repo["owner"]["login"],
            "name": repo["full_name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "watchers": repo["watchers_count"],
            "repo_size": repo["size"],
            "language": repo["language"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "created_year": repo["created_at"][:4],
            "open_issues": repo["open_issues_count"],
            "license": (repo["license"]["spdx_id"] if repo["license"] else None),
            "topics": repo["topics"],
            "has_issues": repo["has_issues"],
            "has_wiki": repo["has_wiki"],
            "has_discussions": repo.get("has_discussions"),
            "archived": repo["archived"],
            "default_branch": repo["default_branch"],
            "visibility": repo["visibility"],
            "url": repo["html_url"],
        }
    )


df = pd.DataFrame(rows)

print("\nBefore deduplication:", len(df))

df = df.drop_duplicates(subset="name")

print("After deduplication:", len(df))
print("Dataset shape:", df.shape)

df.to_csv(output_path, index=False)

print("\nFinal dataset saved to:", output_path)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
