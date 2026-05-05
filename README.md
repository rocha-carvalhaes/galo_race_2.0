# Galo Race 2.0 — My second street race: data engineering & performance analysis

## Executive summary — the short story
I raced the 10 km in 2023 and 2024 and turned a “just finished” result into a real competitive leap.

<img width="662" height="530" alt="image" src="https://github.com/user-attachments/assets/6a20bbf6-f7e3-4f6e-b4d5-360ae1b97d26" />

##### This README documents the full analysis of that progression, places it within the race-level context, and summarizes the pipeline and technologies used to get these results.

---

## Full analysis — my performance (2023 → 2024), male 10 km category

### 1) Raw improvement (time & pace)
- 2023 time (10 km): 01:01:59 = 3,719 seconds → pace ≈ 6:11.9 /km  
- 2024 time (10 km): 00:53:13 = 3,193 seconds → pace ≈ 5:19.3 /km  
- Absolute improvement: 526 seconds = 8 minutes 46 seconds  
- Relative improvement: 526 / 3,719 ≈ 14.2% faster overall (same ~14.1% faster per km)

### 2) Placement and percentiles (male category)
- 2023: 948th out of 1,320 male runners → 71.8th percentile (you were in the slower ~72% of male competitors)
- 2024: 390th out of 1,441 male runners → 27.1st percentile (you are faster than ~73% of male competitors)
- Net placement gain: 948 - 390 = 558 positions
- Net percentile gain: 71.8 - 27.1 = 44.7 percentile points

Conclusion: 14% drop in completion time and reaplacement of negative 44.7 percentile points indicates great success in this project.

---

## Market / event highlights (short bullets)
- Combined dataset used for analysis (2023 + 2024): 19,720 participant records (all distances/genders)
- Participants by edition:
  - 2023 total: 8,375 runners
  - 2024 total: 11,347 runners (+35.5% overall)
- Distance split (example): 5 km dominated the event (≈77.7% in 2023 → 81.5% in 2024)
- Gender mix (all distances): 2023 ≈ 50.8% M / 49.2% F → 2024 ≈ 47.9% M / 52.1% F (female participation increased)
- Male 10 km category: 1,320 (2023) → 1,441 (2024) (+9.2%)
- Completion-time summary (combined):
  - Mean completion time ≈ 47.28 minutes
  - Median completion time ≈ 42.03 minutes
  - High variance across the full field (std ≈ 20 min), reflecting mixed levels and both 5 km & 10 km times
- Field got faster overall between editions (median moved toward quicker times).

---

## Methodology, pipeline & technologies used

Project architecture (high level)
- Data source: official race results published as PDF files (one PDF per category/distance)
- Extraction: custom Python pipeline that reads PDFs and converts results into structured tables
- Staging / storage: Parquet files for treated outputs (data/treated/results_2023.parquet, results_2024.parquet)
- Analysis: Jupyter notebooks used for EDA and comparative analysis (notebooks/performance_eda.ipynb, exploratory_analysis_2023.ipynb)
- Reporting / visualization: interactive exploration in notebooks and Power BI for dashboards (Power BI consumes Parquet/SQLite as needed)

Key project files (implementation)
- /src/get_path.py — locate raw PDF files by year
- /src/get_data.py — extract tables from PDFs using:
  - pdfplumber for table extraction when possible
  - PyMuPDF (fitz) as a fallback to parse text and reconstruct rows
  - Custom parsing logic to split rows and fields
- /src/treat_data.py — feature engineering and type conversions:
  - Converts time strings to seconds, minutes, hours
  - Computes pace and numeric fields (pos, num, age, ag, dist_num)
- /src/save_parquet.py — saves cleaned data to Parquet files
- /src/main.py — orchestrates the end-to-end pipeline for each year (2023 and 2024)
- /notebooks — exploratory notebooks that produce the statistics and visualizations used in this README

Technologies
- Python (pandas, pdfplumber, PyMuPDF/fitz, matplotlib, numpy, scipy)
- Jupyter Notebooks for analysis and visualization
- Parquet for intermediate data (efficient columnar storage)
- Power BI for interactive dashboards and reporting (consumes Parquet / SQLite)
- (Optional) SQLite as a lightweight warehouse for downstream consumption

---

## Final note
This project is a blend of data engineering and personal performance analytics: extracting hard-to-read results from PDFs, structuring the data for analysis, and turning those numbers into meaningful training feedback.
