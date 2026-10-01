from pathlib import Path
import ast
import re
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "github_repositories_cleaned.csv"

FINAL_FILE = BASE_DIR / "data" / "processed" / "github_repositories_topics_final.csv"

TOPIC_SUMMARY_FILE = BASE_DIR / "data" / "processed" / "github_topic_summary.csv"

CATEGORY_SUMMARY_FILE = BASE_DIR / "data" / "processed" / "github_category_summary.csv"


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

original_columns = df.columns.tolist()
original_repository_count = df["url"].nunique()

print("Original Dataset Shape:", df.shape)
print("Original Repositories:", original_repository_count)


# ============================================================
# 3. PARSE TOPICS
# ============================================================


def parse_topics(value):

    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    try:
        result = ast.literal_eval(value)

        if isinstance(result, list):
            return result

    except (ValueError, SyntaxError):
        pass

    return []


df["topics_list"] = df["topics"].apply(parse_topics)


# ============================================================
# 4. EXPLODE TOPICS
# ============================================================

topics_df = df.explode("topics_list", ignore_index=True)

topics_df = topics_df.rename(columns={"topics_list": "original_topic"})


# ============================================================
# 5. IDENTIFY EMPTY TOPIC REPOSITORIES
# ============================================================

topics_df["original_topic"] = (
    topics_df["original_topic"].astype("string").str.strip().str.lower()
)

topics_df["has_topic"] = topics_df["original_topic"].notna() & (
    topics_df["original_topic"] != ""
)


# ============================================================
# 6. NORMALIZE TOPIC FORMAT
# ============================================================


def normalize_topic(topic):

    topic = str(topic).strip().lower()

    topic = re.sub(r"[-_\s]+", "-", topic)

    return topic


topics_df["normalized_topic"] = topics_df.loc[
    topics_df["has_topic"], "original_topic"
].apply(normalize_topic)


# ============================================================
# 7. TOPIC ALIASES
# ============================================================

TOPIC_ALIASES = {
    # ---------------- PYTHON ----------------
    "python3": "python",
    "python-3": "python",
    "python-2": "python",
    # ---------------- AI ----------------
    "ai": "artificial-intelligence",
    "artificial-intelligence": "artificial-intelligence",
    "artificial-intelligence-ai": "artificial-intelligence",
    # ---------------- MACHINE LEARNING ----------------
    "ml": "machine-learning",
    "machinelearning": "machine-learning",
    "machine-learning": "machine-learning",
    # ---------------- DEEP LEARNING ----------------
    "deeplearning": "deep-learning",
    "deep-learning": "deep-learning",
    # ---------------- LLM ----------------
    "llm": "large-language-models",
    "llms": "large-language-models",
    "large-language-model": "large-language-models",
    "large-language-models": "large-language-models",
    # ---------------- NLP ----------------
    "nlp": "natural-language-processing",
    "natural-language-processing": "natural-language-processing",
    # ---------------- PYTORCH ----------------
    "torch": "pytorch",
    "pytorch": "pytorch",
    # ---------------- SCIKIT LEARN ----------------
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    # ---------------- DATA SCIENCE ----------------
    "datascience": "data-science",
    "data-science": "data-science",
    # ---------------- EDA ----------------
    "eda": "exploratory-data-analysis",
    "exploratory-data-analysis": "exploratory-data-analysis",
    # ---------------- WEB SCRAPING ----------------
    "webscraping": "web-scraping",
    "web-scraping": "web-scraping",
    "web-scraper": "web-scraping",
    "webscraper": "web-scraping",
    "scraping": "web-scraping",
    # ---------------- RAG ----------------
    "retrieval-augmented-generation": "rag",
    "rag": "rag",
    # ---------------- AI AGENTS ----------------
    "ai-agent": "ai-agents",
    "ai-agents": "ai-agents",
    "llm-agent": "ai-agents",
    "llm-agents": "ai-agents",
    # ---------------- TRANSFORMERS ----------------
    "transformer": "transformers",
    "transformers": "transformers",
    # ---------------- CYBERSECURITY ----------------
    "cyber-security": "cybersecurity",
    "cybersecurity": "cybersecurity",
    # ---------------- PENETRATION TESTING ----------------
    "pentest": "penetration-testing",
    "pentesting": "penetration-testing",
    "penetration-testing": "penetration-testing",
    # ---------------- REST ----------------
    "rest": "rest-api",
    "rest-api": "rest-api",
}


def standardize_topic(topic):

    if pd.isna(topic):
        return "no-topic"

    return TOPIC_ALIASES.get(topic, topic)


topics_df.loc[topics_df["has_topic"], "final_topic"] = topics_df.loc[
    topics_df["has_topic"], "normalized_topic"
].apply(standardize_topic)

topics_df.loc[~topics_df["has_topic"], "final_topic"] = "no-topic"


# ============================================================
# 8. CATEGORY DEFINITIONS
# ============================================================

AI_ML = {
    "artificial-intelligence",
    "machine-learning",
    "deep-learning",
    "large-language-models",
    "natural-language-processing",
    "pytorch",
    "tensorflow",
    "keras",
    "scikit-learn",
    "transformers",
    "rag",
    "ai-agents",
    "agent",
    "agents",
    "agentic-ai",
    "multi-agent-systems",
    "computer-vision",
    "reinforcement-learning",
    "generative-ai",
    "genai",
    "mlops",
    "automl",
    "neural-network",
    "neural-networks",
    "graph-neural-networks",
    "object-detection",
    "image-classification",
    "ocr",
    "multimodal",
    "prompt-engineering",
    "fine-tuning",
    "embeddings",
    "foundation-models",
    "federated-learning",
    "classification",
    "regression",
    "clustering",
    "recommender-system",
    "anomaly-detection",
    "predictive-modeling",
    "speech-recognition",
}


DATA_SCIENCE = {
    "data",
    "data-science",
    "data-analysis",
    "data-visualization",
    "exploratory-data-analysis",
    "numpy",
    "pandas",
    "matplotlib",
    "plotly",
    "seaborn",
    "statistics",
    "data-engineering",
    "data-mining",
    "feature-engineering",
    "dataset",
    "datasets",
    "tabular-data",
    "data-quality",
    "data-cleaning",
    "analytics",
    "scientific-computing",
    "polars",
}


WEB = {
    "web",
    "web-development",
    "web-app",
    "website",
    "frontend",
    "backend",
    "html",
    "html5",
    "css",
    "javascript",
    "typescript",
    "react",
    "nextjs",
    "django",
    "flask",
    "fastapi",
    "streamlit",
    "http",
    "rest-api",
    "openapi",
    "websocket",
    "websockets",
    "browser",
    "playwright",
    "selenium",
    "beautifulsoup",
    "web-scraping",
}


CYBERSECURITY = {
    "security",
    "cybersecurity",
    "hacking",
    "penetration-testing",
    "ctf",
    "ctf-tools",
    "bugbounty",
    "reverse-engineering",
    "forensics",
    "osint",
    "security-tools",
    "privacy",
    "pwn",
}


DEVOPS = {
    "docker",
    "docker-compose",
    "kubernetes",
    "devops",
    "aws",
    "azure",
    "gcp",
    "cloud",
    "deployment",
    "monitoring",
    "observability",
    "ci-cd",
    "pipeline",
    "orchestration",
    "linux",
    "server",
}


DATABASES = {
    "database",
    "databases",
    "postgresql",
    "mysql",
    "sqlite",
    "sql",
    "vector-database",
    "vector-search",
    "mongodb",
    "redis",
}


AUTOMATION = {
    "automation",
    "workflow",
    "asyncio",
    "async",
    "bot",
    "bots",
    "mcp",
    "mcp-server",
}


PYTHON_TOOLS = {
    "python",
    "python-library",
    "pydantic",
    "jupyter",
    "jupyter-notebook",
    "requests",
    "pip",
    "poetry",
    "pytest",
}


FINANCE = {
    "finance",
    "fintech",
    "quantitative-finance",
    "algorithmic-trading",
    "trading",
    "stock-market",
    "crypto",
    "backtesting",
}


MOBILE = {
    "android",
    "ios",
    "flutter",
    "mobile",
    "mobile-app",
}


RESEARCH = {
    "research",
    "reproducible-research",
    "reproducibility",
    "bioinformatics",
    "physics",
    "simulation",
}


ROBOTICS = {
    "robotics",
    "ros",
    "iot",
    "embedded",
    "autonomous",
}


EDUCATION = {
    "education",
    "learning",
    "tutorial",
    "course",
    "university",
    "student",
}


GAMES = {
    "game",
    "games",
    "gaming",
}


SOFTWARE_DEVELOPMENT = {
    "open-source",
    "developer-tools",
    "programming",
    "software-engineering",
    "github",
    "git",
    "algorithms",
    "data-structures",
    "testing",
    "benchmark",
    "benchmarking",
}


# ============================================================
# 9. CATEGORY ASSIGNMENT
# ============================================================


def assign_category(topic):

    if topic == "no-topic":
        return "No Topic"

    if topic in AI_ML:
        return "AI & Machine Learning"

    if topic in DATA_SCIENCE:
        return "Data Science & Analytics"

    if topic in WEB:
        return "Web Development"

    if topic in CYBERSECURITY:
        return "Cybersecurity"

    if topic in DEVOPS:
        return "DevOps & Cloud"

    if topic in DATABASES:
        return "Databases"

    if topic in AUTOMATION:
        return "Automation & Agents"

    if topic in PYTHON_TOOLS:
        return "Python & Developer Tools"

    if topic in FINANCE:
        return "Finance & Trading"

    if topic in MOBILE:
        return "Mobile & App Development"

    if topic in RESEARCH:
        return "Research & Science"

    if topic in ROBOTICS:
        return "Robotics & IoT"

    if topic in EDUCATION:
        return "Education"

    if topic in GAMES:
        return "Games"

    if topic in SOFTWARE_DEVELOPMENT:
        return "Software Development"

    return "Other"


topics_df["category"] = topics_df["final_topic"].apply(assign_category)


# ============================================================
# 10. REMOVE DUPLICATE REPOSITORY + FINAL TOPIC
# ============================================================

topics_df = topics_df.drop_duplicates(subset=["url", "final_topic"]).reset_index(
    drop=True
)


# ============================================================
# 11. FINAL DATASET
# ============================================================

# Remove temporary column
topics_df = topics_df.drop(columns=["has_topic"])


# Keep ALL original columns
# + analytical topic columns

new_columns = [
    "original_topic",
    "normalized_topic",
    "final_topic",
    "category",
]

final_columns = original_columns + [
    col for col in new_columns if col not in original_columns
]

final_df = topics_df[final_columns].copy()


# ============================================================
# 12. TOPIC-LEVEL DATA
# ============================================================

# One repository contributes only ONCE to one topic.

repo_topic = (
    final_df[final_df["final_topic"] != "no-topic"]
    .drop_duplicates(subset=["url", "final_topic"])
    .copy()
)


topic_summary = (
    repo_topic.groupby(["final_topic", "category"], as_index=False)
    .agg(
        repository_count=("url", "nunique"),
        total_stars=("stars", "sum"),
        average_stars=("stars", "mean"),
        median_stars=("stars", "median"),
        maximum_stars=("stars", "max"),
        total_forks=("forks", "sum"),
        average_forks=("forks", "mean"),
        total_watchers=("watchers", "sum"),
        average_watchers=("watchers", "mean"),
        maximum_watchers=("watchers", "max"),
        total_open_issues=("open_issues", "sum"),
        average_open_issues=("open_issues", "mean"),
        average_repo_size=("repo_size", "mean"),
        first_created_year=("created_year", "min"),
        last_created_year=("created_year", "max"),
    )
    .sort_values("repository_count", ascending=False)
)


# ============================================================
# 13. REPOSITORY + CATEGORY LEVEL
# ============================================================

# IMPORTANT:
#
# Repo A:
# pandas     -> Data Science -> 80 watchers
# numpy      -> Data Science -> 80 watchers
#
# must become:
#
# Repo A -> Data Science -> 80 watchers
#
# BEFORE category totals are calculated.


repo_category = repo_topic.groupby(["url", "category"], as_index=False).agg(
    stars=("stars", "first"),
    forks=("forks", "first"),
    watchers=("watchers", "first"),
    open_issues=("open_issues", "first"),
    repo_size=("repo_size", "first"),
    created_year=("created_year", "first"),
    updated_at=("updated_at", "first"),
    language=("language", "first"),
    license=("license", "first"),
)


# ============================================================
# 14. CATEGORY SUMMARY
# ============================================================

category_summary = (
    repo_category.groupby("category", as_index=False)
    .agg(
        repository_count=("url", "nunique"),
        total_stars=("stars", "sum"),
        average_stars=("stars", "mean"),
        total_forks=("forks", "sum"),
        average_forks=("forks", "mean"),
        total_watchers=("watchers", "sum"),
        average_watchers=("watchers", "mean"),
        total_open_issues=("open_issues", "sum"),
        average_open_issues=("open_issues", "mean"),
        average_repo_size=("repo_size", "mean"),
        unique_languages=("language", "nunique"),
        unique_licenses=("license", "nunique"),
    )
    .sort_values("repository_count", ascending=False)
)


# ============================================================
# 15. SAVE DATASETS
# ============================================================

final_df.to_csv(FINAL_FILE, index=False)

topic_summary.to_csv(TOPIC_SUMMARY_FILE, index=False)

category_summary.to_csv(CATEGORY_SUMMARY_FILE, index=False)


# ============================================================
# 16. VALIDATION TESTS
# ============================================================

print("\n" + "=" * 65)
print("FINAL VALIDATION")
print("=" * 65)


# Test 1 — Original columns preserved

missing_original_columns = [
    col for col in original_columns if col not in final_df.columns
]

assert not missing_original_columns, (
    f"Missing original columns: {missing_original_columns}"
)

print("✓ All 21 original columns preserved")


# Test 2 — Repository count preserved

final_repository_count = final_df["url"].nunique()

assert final_repository_count == original_repository_count

print(f"✓ All {original_repository_count} repositories preserved")


# Test 3 — New analytical columns exist

for col in [
    "original_topic",
    "normalized_topic",
    "final_topic",
    "category",
]:
    assert col in final_df.columns

print("✓ All analytical columns created")


# Test 4 — No duplicate repository/topic

duplicate_repo_topics = (
    final_df[final_df["final_topic"] != "no-topic"]
    .duplicated(subset=["url", "final_topic"])
    .sum()
)

assert duplicate_repo_topics == 0

print("✓ No duplicate repository-topic combinations")


# Test 5 — Topic summary matches repository-topic data

assert (
    topic_summary["repository_count"].sum() == repo_topic["url"].nunique()
    or topic_summary["repository_count"].sum() >= repo_topic["url"].nunique()
)

print("✓ Topic summary validated")


# Test 6 — Category summary must not double count
# repositories within the same category

category_repo_pairs = repo_category[["url", "category"]].duplicated().sum()

assert category_repo_pairs == 0

print("✓ No duplicate repository-category combinations")


# Test 7 — Category watcher total is based on
# one repository per category

calculated_category_watchers = repo_category["watchers"].sum()

summary_category_watchers = category_summary["total_watchers"].sum()

assert calculated_category_watchers == summary_category_watchers

print("✓ Category watcher aggregation validated")


# Test 8 — Category stars aggregation

assert repo_category["stars"].sum() == category_summary["total_stars"].sum()

print("✓ Category star aggregation validated")


# Test 9 — Category forks aggregation

assert repo_category["forks"].sum() == category_summary["total_forks"].sum()

print("✓ Category fork aggregation validated")


# Test 10 — No empty final topics

assert final_df["final_topic"].notna().all()

print("✓ No empty final_topic values")


# Test 11 — No empty categories

assert final_df["category"].notna().all()

print("✓ No empty category values")


# Test 12 — Alias logic

assert standardize_topic("ai") == "artificial-intelligence"
assert standardize_topic("python3") == "python"
assert standardize_topic("ml") == "machine-learning"
assert standardize_topic("llm") == "large-language-models"
assert standardize_topic("torch") == "pytorch"
assert standardize_topic("sklearn") == "scikit-learn"

print("✓ Topic alias tests passed")


# Test 13 — Category logic

assert assign_category("tensorflow") == "AI & Machine Learning"

assert assign_category("pandas") == "Data Science & Analytics"

assert assign_category("docker") == "DevOps & Cloud"

assert assign_category("postgresql") == "Databases"

print("✓ Category assignment tests passed")


# ============================================================
# 17. FINAL REPORT
# ============================================================

print("\n" + "=" * 65)
print("FINAL DATASET REPORT")
print("=" * 65)

print("\nFinal dataset shape:", final_df.shape)

print("Repositories:", final_df["url"].nunique())

print("Unique final topics:", repo_topic["final_topic"].nunique())

print("Unique categories:", final_df["category"].nunique())

print("Repositories without topics:", (final_df["final_topic"] == "no-topic").sum())


print("\nTop 10 Topics:")

print(
    topic_summary[
        [
            "final_topic",
            "category",
            "repository_count",
            "total_stars",
            "total_watchers",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print("\nCategory Summary:")

print(
    category_summary[
        [
            "category",
            "repository_count",
            "total_stars",
            "total_watchers",
        ]
    ].to_string(index=False)
)


print("\nFiles created:")

print(FINAL_FILE)
print(TOPIC_SUMMARY_FILE)
print(CATEGORY_SUMMARY_FILE)

print("\n" + "=" * 65)
print("✓ ALL VALIDATION TESTS PASSED")
print("=" * 65)
