Python Ecosystem Intelligence

An exploratory data analysis project focused on understanding the Python ecosystem through data collected from GitHub and PyPI.

The project looks at the ecosystem from two sides:

GitHub — Python repositories, repository activity, topics, categories, stars, forks, issues and licenses.
PyPI — Python packages, download activity and Python version requirements.

Instead of starting with a ready-made dataset, I collected the data, cleaned and validated it, processed GitHub topics, created summary datasets, and then used EDA and visualization to explore the patterns in the data.

What I wanted to understand

The project was built around questions such as:

How has Python repository activity changed from 2020 to 2026?
Which Python repositories receive the most stars and forks?
What does repository activity look like across different years?
Which licenses are most commonly used?
Which Python-related topics appear most frequently?
Which topics and categories attract the most community attention?
Which Python packages have the highest download activity?
How does package download activity change over time?
Which Python versions are commonly required by packages?
What patterns can be observed across GitHub and PyPI data?
Project Workflow

The project follows a complete data-analysis workflow:

Research & Data Collection
↓
Raw Data
↓
Data Cleaning
↓
Data Validation
↓
Data Transformation
↓
Topic Processing & Aggregation
↓
Exploratory Data Analysis
↓
Visualization & Findings

1. GitHub Repository Analysis

GitHub is the larger part of the project and focuses on Python repositories created between 2020 and 2026.

Data Collection

Repository data was collected using the GitHub REST API.

The collection process used multiple time windows and categories to build a broader dataset of Python repositories.

The main search logic was based on:

Python repositories
Repository creation date
fork:false
Multiple topic/category searches
Sorting by stars

The collected repository information includes fields such as:

Repository name and owner
Description
Stars
Forks
Watchers
Repository size
Language
Creation and update dates
Open issues
License
Topics
Repository URL
Repository features and metadata

The final cleaned repository dataset contains 5,359 Python repositories.

Data Cleaning

The raw GitHub data was cleaned before starting the analysis.

The process included:

Inspecting dataset structure and data types
Checking missing values
Handling missing descriptions and licenses
Checking duplicate repositories
Converting date columns to datetime
Creating the repository creation year
Validating creation years
Checking numeric values for invalid negatives
Checking whether created_at occurs after updated_at
Preserving important repository-level information

The cleaned dataset is stored separately from the raw API output.

2. GitHub Topic Processing

GitHub topics require additional processing because a repository can have multiple topics.

For example, one repository may contain topics such as:

python, machine-learning, pytorch, deep-learning

These topics cannot be treated as a single value when performing topic-level analysis.

The topic-processing workflow therefore:

Parses the original topic lists
Explodes topics into individual records
Cleans topic formatting
Normalizes spaces, hyphens and underscores
Standardizes common aliases
Handles repositories without topics
Removes duplicate repository-topic combinations
Assigns broader categories to topics

Common variations such as ai, ml, llm, nlp, sklearn, torch and similar topic names are mapped to consistent names.

The processed topic data also keeps the original repository-level information so that repository-level questions can still be answered.

Topic Categories

Topics are grouped into broader areas including:

AI & Machine Learning
Data Science & Analytics
Web Development
Cybersecurity
DevOps & Cloud
Databases
Automation
Python & Developer Tools
Finance & Trading
Mobile & App Development
Research & Science
Robotics & IoT
Education
Games
Software Development
General Python & Open Source
3. Topic and Category Summaries

After processing the topics, separate summary datasets were created for analysis.

These include:

github_topic_summary.csv
github_category_summary.csv

The summaries make it easier to perform topic-level and category-level analysis without repeatedly aggregating the exploded repository data.

Metrics include repository counts and repository-level measures such as stars, forks, open issues and repository size.

Avoiding Double Counting

One important part of this project was handling the effect of exploding topics.

If a repository has five topics, that repository appears five times in the exploded dataset.

Therefore, directly summing repository-level metrics from the exploded topic data can produce incorrect totals.

For example:

If one repository has 10,000 stars and belongs to three topics, the exploded dataset contains 10,000 stars in each of those topic rows.

Summing those rows would incorrectly count the same 10,000 stars three times.

Because of this, the project keeps a distinction between:

Repository-level analysis
Topic-level analysis
Category-level analysis

and uses separate summary datasets where required.

This was an important validation point in the topic-processing stage.

4. GitHub Exploratory Data Analysis

The GitHub EDA is divided into focused notebooks rather than putting the complete analysis into one large notebook.

Repository-level analysis

The repository analysis covers areas such as:

Dataset overview
Descriptive statistics
Repository counts by year
Repository creation trends
Stars
Forks
Watchers
Open issues
Repository size
License distribution
Repository activity and update patterns
Topic and category analysis

The topic/category analysis explores:

Most common topics
Topic distribution
Topics with high repository counts
Topics with high star activity
Category distribution
Category-level repository activity
Relationships between repository count and popularity

Different visualization types are used depending on the question, including:

Bar charts
Scatter plots
Treemaps
Heatmaps
Other comparison-focused visualizations

The goal is not to create as many charts as possible, but to choose a chart that makes the particular comparison easier to understand.

5. PyPI Package Analysis

The second major part of the project focuses on Python packages available through PyPI.

The PyPI work contains both package metadata and download-history analysis.

Package Data Cleaning

The package dataset was inspected and cleaned before analysis.

The process included:

Inspecting columns and data types
Checking missing values
Checking duplicate records
Standardizing column names
Retaining license information
Filling missing license values with Unknown
Checking Python version requirements
Examining download distributions

Some columns were renamed to make their purpose clearer, for example:

requires_python → required_python_version
downloads_last_day → downloads_daily
downloads_last_week → downloads_weekly
downloads_last_month → downloads_monthly

The cleaned package data is stored separately in the processed data directory.

6. PyPI Download History EDA

A separate historical download dataset is used to study package download activity over time.

The analysis focuses on:

Most downloaded packages
Total download activity
Download share of popular packages
Monthly download trends
Comparing popular packages over time
Overall download patterns

For some visualizations, less significant packages are grouped into an Other category so that the main trends remain readable.

The historical data is cleaned separately and then used for time-based analysis.

7. PyPI Python Version Analysis

Package metadata also contains information about required Python versions.

The project examines the different Python version requirements specified by packages.

Examples found in the dataset include:

>=3.12
>=3.11
>=3.10
>=3.9
>=3.8
>=3.7.0
>=3.6

This provides another way of looking at compatibility and the Python versions supported by packages in the analyzed dataset.

8. Data Validation

Validation was performed throughout the project instead of relying only on visual inspection.

GitHub validation included
Repository count checks
Duplicate repository checks
Creation-year validation
Negative numeric-value checks
Date consistency checks
Repository-topic duplicate checks
Repository-category duplicate checks
Preservation of original repository columns
Validation of topic and category summaries
Validation of aggregated repository metrics
PyPI validation included
Duplicate checks
Python version requirement inspection
Download metric consistency checks
Outlier identification
Review of unusually high download values

The download metrics were checked for logical consistency:

Daily downloads ≤ Weekly downloads ≤ Monthly downloads

No invalid cases were found in these checks.

Outliers were identified in the download metrics, but they were not automatically removed because very popular Python packages can legitimately have unusually high download numbers.

9. Data Visualization

The project uses Python's data-analysis and visualization libraries:

Pandas — data loading, cleaning and transformation
NumPy — numerical operations
Matplotlib — visualization
Seaborn — statistical and categorical visualization
Plotly — interactive visualization
Requests — API requests
python-dotenv — environment variable management
Jupyter Notebook — analysis and experimentation

Different visualization styles are used where they make the data easier to understand.

The focus is on readability and analytical purpose, rather than creating decorative charts.

Project Structure
python-ecosystem-intelligence/
│
├── data/
│   ├── raw/
│   │   ├── github_repositories_raw.csv
│   │   ├── pypi_packages_raw.csv
│   │   └── pypi_download_history.csv
│   │
│   └── processed/
│       ├── github_repositories_cleaned.csv
│       ├── github_topic_summary.csv
│       ├── github_category_summary.csv
│       ├── pypi_packages_cleaned.csv
│       └── pypi_download_history_cleaned.csv
│
├── notebooks/
│   ├── 01_pypi_data_cleaning.ipynb
│   ├── 02_github_data_cleaning.ipynb
│   ├── 03_github_topics_cleaning.py
│   ├── 04_pypi_download_history_cleaning.ipynb
│   ├── 05_github_eda.ipynb
│   ├── 06_github_topic_category_eda.ipynb
│   └── 07_pypi_download_history_eda.ipynb
│
├── src/
│   ├── github_collector.py
│   ├── pypi_collector.py
│   └── pypi_history_collector.py
│
├── requirements.txt
└── README.md
What This Project Demonstrates

This project gave me practical experience with a complete data-analysis workflow:

Research → API Data Collection → Raw Data → Cleaning → Validation → Transformation → Aggregation → EDA → Visualization

More importantly, it involved working with real API data rather than only analyzing a small, ready-made CSV.

The project required decisions around:

What data to collect
How to structure the collection process
How to handle missing and inconsistent data
How to normalize GitHub topics
How to categorize topics
How to avoid double-counting after exploding data
Which metrics should be aggregated
Which outliers should be investigated rather than blindly removed
Which visualizations best represent each analysis

The current focus is on completing the EDA and extracting meaningful findings from the collected data before moving toward any further presentation or dashboard work.

Data Note

GitHub repository information, PyPI package metadata and download statistics change over time.

Therefore, the results in this project represent the datasets collected during the project's collection period and should be treated as a snapshot of the Python ecosystem rather than a permanent measurement.

API Credentials

GitHub API authentication is handled through an environment variable stored in a local .env file.

The .env file is excluded from version control and no API token is stored in the repository.

AI-Assisted Development

AI tools were used during development as a supporting tool for tasks such as troubleshooting, understanding API behaviour, checking implementation logic and exploring visualization approaches.

The data collection, cleaning decisions, validation, topic processing, analysis and interpretation were carried out as part of the project workflow.
