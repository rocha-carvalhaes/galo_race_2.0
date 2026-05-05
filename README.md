# Overview: 2024 - A New Race, New Insights

After a year of focused training, I ran my second street race in 2024, and I hit my target: placing within the top 50%! It felt incredible, but as I reviewed my results, new questions arose. I realized that raw placement numbers don't tell the full story—I needed to understand how my performance compared within specific demographic groups, training backgrounds, and competitive tiers.

Now, I want to analyze how my performance compares across specific runner subgroups and explore how advanced statistics might reveal patterns among returning competitors. Could I identify trends or untapped competitive opportunities?

## Objectives

In this next phase, my goals are to:

### - Investigate Placement Across Different Runner Segments
I'll explore how my performance stacks up against specific runner groups, such as age brackets, those running in teams, and perhaps even solo vs. team runners.

### - Analyze Advanced Statistics for Insightful Comparisons
Delve into statistics that go beyond averages and percentiles, using techniques like ANOVA to assess performance variance between groups and clustering to find patterns among runners.

### - Predict Returning Runners and Future Placements
Using historical data, I'll attempt to forecast which runners are likely to participate again and predict their potential placements based on past results.

## Methodology

### Data Collection and Preparation

The project follows a structured data pipeline to gather and process race data:

- **Data Extraction**: Race results are extracted from PDF files (2023 and 2024) using `pdfplumber` and custom PDF parsing with `fitz`
- **Data Consolidation**: Multi-year datasets are combined into a unified structure with consistent formatting
- **Feature Engineering**: Enhanced datasets include temporal breakdowns (hours, minutes, seconds), pace calculations, and distance normalization
- **Data Storage**: Processed datasets are saved as Parquet files for efficient analysis

**Pipeline Components** (`/src`):
- `get_data.py`: Extracts race results from PDF files using OCR-safe regex patterns
- `treat_data.py`: Performs feature engineering, including time conversions and pace calculations
- `main.py`: Orchestrates the end-to-end pipeline for both 2023 and 2024 datasets

### Advanced Analysis

**Current Analysis** (`/notebooks`):
- `exploratory_analysis_2023.ipynb`: Initial exploration of 2023 race demographics and performance patterns
- `performance_eda.ipynb`: Comprehensive exploratory data analysis comparing 2023 and 2024 results, examining distribution of times, performance by gender/age, and segment-level insights

**Planned Techniques**:
- **Descriptive Statistics**: Summaries by group (age groups, solo vs. party runners) to understand performance patterns
- **Comparative Analysis**: Using statistical tests (t-tests, ANOVA) to examine whether performance differs significantly across groups
- **Cluster Analysis**: K-means and other clustering algorithms to identify natural groupings among runners

### Predictive Modeling

- Classification models (Random Forest, Decision Trees) to identify runners likely to return
- Regression models to forecast 2025 placements for returning competitors
- Incorporation of external features (weather conditions, training intensity) to refine predictions

### Visualization and Reporting

Power BI remains the primary visualization tool, with interactive reports enabling:
- Group performance comparisons
- Returning runner tracking
- Predictive insights visualization

## Expected Results

By the end of this project, I will have:

- **Nuanced Performance Understanding**: Clear insights into how my results compare within specific demographic and competitive segments
- **Returning Runner Intelligence**: Patterns and predictors for which runners participate across years
- **Data-Driven Training Plan**: Targeted insights to optimize training strategy against my competitive landscape
- **Actionable Predictions**: Forecast placements for 2025 based on historical trends

## Project Structure

```
galo_race_2.0/
├── src/                          # Data pipeline modules
│   ├── main.py                  # Pipeline orchestration
│   ├── get_data.py              # PDF data extraction
│   ├── treat_data.py            # Feature engineering
│   ├── get_path.py              # Path utilities
│   └── save_parquet.py          # Parquet serialization
│
├── notebooks/                    # Analysis and visualization
│   ├── exploratory_analysis_2023.ipynb
│   └── performance_eda.ipynb
│
└── README.md
```

## Tech Stack

- **Python 3.x**: Core data processing
- **pandas**: Data manipulation and analysis
- **pdfplumber & fitz**: PDF extraction and parsing
- **Jupyter Notebooks**: Interactive analysis and visualization
- **Parquet**: Efficient data storage format
