# 📊 Finance Data Pipeline & Dashboard
## Project Description
This Financial Data Automation Dashboard is a full-stack data solution built with Streamlit to streamline the end-to-end process of financial reporting. The application serves as an automated ETL (Extract, Transform, Load) pipeline that ingests raw, unstructured Excel and CSV files and converts them into a queryable SQLite database.

The project solves real-world primary sourced data. It integrit issues by implementing a cleaning engine using Pandas to analysis sales and expense. 
Key features include automated whitespace stripping, currency-to-numeric casting, and a custom temporal correction logic that identifies and standardizes inconsistent date entries (e.g., synchronizing legacy 2020 timestamps to a 2021 fiscal year). By utilizing SQLite for persistent storage, the dashboard decouples data processing from visualization, allowing non-accounting departments to access up-to-date KPIs, revenue trends, and expense breakdowns instantly without needing to re-upload source files. This project demonstrates proficiency in data engineering and analysis, relational database management, and interactive dashboard design.

## Why I built this
Every month, I had to rebuild the sales and expense report by hand from daily transaction records kept in Excel. The work was repetitive, easy to get wrong, and
left little time for the part that actually matters: explaining what the numbers mean.

I built this tool to automate the repeated work, reduce error.

## What it does
1. **Upload** the monthly Excel or CSV file (balance-sheet format).
2. **Clean** it automatically with Pandas:
   - strips stray whitespace
   - converts currency text into numbers
   - fixes inconsistent dates (e.g. legacy 2020 entries aligned to the 2021 fiscal year)
   - sorts every sale and expense into a category (e.g. rentals, school, cyber café, engineering; staff costs, utilities, transport)
3. **Store** the clean data in a SQLite database, so reports no longer depend on re-uploading source files.
4. **Show** a dashboard: total sales, total expenses, margin, revenue by category, revenue trend, expense breakdown, top customers, and sales vs expenses over time.

## Who uses what
| Role | Access |
|---|---|
| Accounting (password) | Upload data, run the cleaning pipeline, update the database |
| Everyone else (Sales, Engineering, Institute, Management) | Read-only dashboard from the stored data |

## Results
A clearer dashboard for managers and the CEO to make better, informed decisions, and recommendations to go with the numbers.

## Tech stack
Python · Pandas · SQLite · Streamlit · Plotly · Matplotlib · Seaborn · openpyxl

## Run it yourself
```bash




