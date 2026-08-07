## Project Description
This Financial Data Automation Dashboard is a full-stack data solution built with Streamlit to streamline the end-to-end process of financial reporting. The application serves as an automated ETL (Extract, Transform, Load) pipeline that ingests raw, unstructured Excel and CSV files and converts them into a queryable SQLite database.

The project solves real-world primary sourced data. It integrit issues by implementing a cleaning engine using Pandas to analysis sales and expense. 
Key features include automated whitespace stripping, currency-to-numeric casting, and a custom temporal correction logic that identifies and standardizes inconsistent date entries (e.g., synchronizing legacy 2020 timestamps to a 2021 fiscal year). By utilizing SQLite for persistent storage, the dashboard decouples data processing from visualization, allowing non-accounting departments to access up-to-date KPIs, revenue trends, and expense breakdowns instantly without needing to re-upload source files. This project demonstrates proficiency in data engineering and analysis, relational database management, and interactive dashboard design.

## Tools used
Language: Python
Storage: Sqlite3
Frontend: Streamlit
Data Handling: Pandas
Visualization: Matplotlib, Seaborn and Plotly 
