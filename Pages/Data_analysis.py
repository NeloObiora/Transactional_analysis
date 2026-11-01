import streamlit as st
import sqlite3
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
        
 
# functions
def Seperator(inv_no):
    inv_no_str = str(inv_no).upper().strip().replace('/', '').replace('&', '')
    if 'SCH' in inv_no_str:
        return 'SCHOOL'
    elif 'RENT' in inv_no_str or 'RENTAL' in inv_no_str:
        return 'RENTAL'
    elif 'CAFE' in inv_no_str or 'CAFÉ' in inv_no_str:
        return "CYBER_CAFE"
    elif 'JCC' in inv_no_str or 'J C C' in inv_no_str or 'REPAIR' in inv_no_str or 'REPAIRS' in inv_no_str:
        return 'ENGINNERING'
    elif 'ON ACC' in inv_no_str or 'ON ACCOUNT'in inv_no_str or 'ON_ACC' in inv_no_str:
        return 'ON ACCOUNT'
    elif inv_no_str.isdigit():
        return 'SALES'
    elif 'PURCHASE' in inv_no_str or 'DEPOSIT' in inv_no_str or 'PURCHASES' in inv_no_str:
        return 'SALES'
    else:
        return 'OTHERS'

def sales_cleaning(df):
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    sales_df = df[['DATE', 'DESCRIPTION', 'INV NO', 'POS', 'THRU_BANK','CASH']]
    sales_df[['POS','THRU_BANK', 'CASH']] = sales_df[['POS','THRU_BANK', 'CASH']].fillna(value=0)
    sales_df['DATE'] = pd.to_datetime(sales_df['DATE'], dayfirst=True)
    sales_df['DATE'] = sales_df['DATE'].ffill()
    sales_df['DATE'] = sales_df['DATE'].apply(lambda x: x.replace(year=2021))
    sales_df = sales_df.sort_values('DATE')
    sales_df[["POS","THRU_BANK","CASH"]] = sales_df[["POS","THRU_BANK","CASH"]].replace(',', '', regex=True).apply(pd.to_numeric,errors= 'coerce')
    sales_df['AMOUNT'] = sales_df["POS"] + sales_df["THRU_BANK"] + sales_df["CASH"]
    sales_df['DEPARTMENT'] = sales_df['INV NO'].apply(Seperator)
    sales_df.drop(columns=["POS", "THRU_BANK", "CASH", "INV NO"], inplace=True)
    filtered_df = sales_df[sales_df['DEPARTMENT'] != 'OTHERS']
    dept_amount = filtered_df.groupby('DEPARTMENT', as_index=False)['AMOUNT'].sum().sort_values('AMOUNT',ascending=False)
    st.subheader("Sales Data")
    st.dataframe(filtered_df)
    st.subheader("Revenue by Department")
    st.dataframe(dept_amount)
    st.session_state['filtered_data'] = filtered_df
    return filtered_df

def show_basic_info(df):                    
    st.subheader("Basic Info")                                              
    st.write(df)
    st.write("Shape :", df.shape)
    st.write("Data Type :", df.dtypes)

def show_missing_values(df):               
    st.subheader("Missing Values")         
    st.write(df.isna().sum())
    
def Expense_Seperator(desc):
    description = str(desc).upper().strip().replace(',', '').replace("/", '')
    if 'TP' in description:
        return 'LOCAL TRANSPORT'
    elif any(x in description for x in ['PURCHASE', 'PMT']):
        return 'PURCHASE'
    elif 'NEWSPAPER' in description:
        return 'NEWSPAPER'
    elif any(x in description for x in ['MD', 'MDS HOUSE']):
        return 'CEO'
    elif any(x in description for x in ['FUEL', 'DIESEL', 'ELECTRICITY', 'RECONNECTION', 'NEPA BILL']):
        return "UTILITIES/ELECTRICITY"
    elif 'LOAN' in description:
        return 'LOAN'
    elif any(x in description for x in ['BANK', 'LODGEMENT']):
        return 'BANK'
    elif re.search(r'\bPR\b', description) or any(x in description for x in ['PR', 'HAMPER', 'GIFT']):
        return 'SALES PROMOTION'
    elif any(x in description for x in ['FEEDING', 'SALARY', 'OFFICER', 'AIRTIME', 'RECHARGE', 'STOCK TAKING', 'INCENTIVE', 'BONUS']):
        return 'STAFF EXPENSES'
    else:
        return 'OTHERS'
    
def expense_cleaning(df):
    expense_df = df[["DATE", "DESCRIPTION.1", "PV NO", "AMT"]]
    expense_df = expense_df.dropna(subset=['AMT'])
    expense_df= expense_df.rename(columns={"AMT":"AMOUNT", "DESCRIPTION.1": "DESCRIPTION" })
    expense_df['DATE'] = pd.to_datetime(expense_df['DATE'], dayfirst=True)
    expense_df['DATE'] = expense_df['DATE'].ffill()
    expense_df['DATE'] = expense_df['DATE'].apply(lambda x: x.replace(year=2021))
    expense_df = expense_df.sort_values('DATE')
    expense_df["AMOUNT"] = expense_df['AMOUNT'].astype(str).str.replace(',', '', regex=True)
    expense_df['AMOUNT'] = expense_df['AMOUNT'].fillna(value=0)
    expense_df['AMOUNT'] = pd.to_numeric(expense_df['AMOUNT'])
    expense_df['DEPARTMENT'] = expense_df['DESCRIPTION'].apply(Expense_Seperator)
    value = expense_df['AMOUNT'].sum()
    st.subheader("Expense Data")
    st.dataframe(expense_df)
    st.session_state['expense_data'] = expense_df
    return(expense_df)

def show_public_view():
    try:
        conn = sqlite3.connect("finance_data.db")
        sale_data = pd.read_sql("SELECT * FROM cleaned_SalesDF", conn)
        expenses_data = pd.read_sql("SELECT * FROM cleaned_ExpenseDF", conn)
        conn.close()
        st.subheader("Sales Data")
        st.dataframe(sale_data)
        st.subheader("Expenses Data")
        st.dataframe(expenses_data)
        
        if sale_data.empty or expenses_data.empty:
            st.warning("⚠️ No records found. Please contact Accounting.")

        # ✔ Convert DATE after SQL read (CORRECTION)
        sale_data['DATE'] = pd.to_datetime(sale_data['DATE'])
        expenses_data['DATE'] = pd.to_datetime(expenses_data['DATE'])

        dashboard_creation(sale_data, expenses_data)
       
    except sqlite3.OperationalError:
        st.error("⚠️ Database not found. Ask Accounting to upload records.")    
        st.info("The system needs at least one successful upload to create the database files.")

def dashboard_creation(sales_df, expense_df):
    st.title("📊 Dashboard")
    if sales_df is None or expense_df is None:
        st.error("Dashboard data missing")
    total_sales = sales_df['AMOUNT'].sum()
    total_expenses = expense_df['AMOUNT'].sum()
    profit = total_sales - total_expenses
    
# Create the KPI layout
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Sales", value=f"N{total_sales:,}")
    col2.metric(label="Total Expenses", value=f"N{total_expenses:,}")
    col3.metric(label="Net Profit", value=f"N{profit:,.1f}", 
            delta=f"{((profit/total_sales)*100):.1f}% Margin" if total_sales != 0 else None
        )

    st.subheader("Revenue by Department")
    dept_totals = sales_df.groupby('DEPARTMENT')['AMOUNT'].sum().sort_values(ascending=False)
    st.bar_chart(dept_totals, x_label= "Department", y_label= "Revenue", use_container_width=True)#, color="#ff8800")

    
    st.subheader("Revenue Trend Over Time")
    # Plot using the string column instead of the date column
    daily_sales = sales_df.groupby('DATE')['AMOUNT'].sum().reset_index()
    daily_sales['DATE'] = daily_sales['DATE'].dt.strftime('%Y-%m-%d')
    daily_sales = daily_sales.sort_values('DATE')
    st.line_chart(daily_sales, x='DATE', y='AMOUNT')
    
    st.subheader("Expense Breakdown")
    fig, ax = plt.subplots()
    top_5_expenses = expense_df.groupby("DEPARTMENT")["AMOUNT"].sum().reset_index()
    top_5_expenses = top_5_expenses.sort_values(by="AMOUNT", ascending=False).head(5)
    ax.pie(top_5_expenses["AMOUNT"], labels=top_5_expenses["DEPARTMENT"], colors=sns.color_palette("pastel"), 
    autopct='%1.1f%%',
    startangle=110)
    st.pyplot(fig)
    
    st.subheader("Top Customers")
    top_customers = sales_df.groupby('DESCRIPTION')['AMOUNT'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_customers)
    
    st.subheader("Growth: Sales vs Expenses")
    # Prepare cumulative data
    sales_trend = sales_df.groupby('DATE')['AMOUNT'].sum().cumsum().reset_index()
    expense_trend = expense_df.groupby('DATE')['AMOUNT'].sum().cumsum().reset_index()
    comparison_df = pd.merge(sales_trend, expense_trend, on='DATE', how='outer', suffixes=('_Sales', '_Exp')).fillna(method='ffill')
    st.area_chart(comparison_df.set_index('DATE'))

st.title("📈 Analysis")

def get_upload_password():
    try:
        return st.secrets["upload_password"]
    except Exception:
        return None

APP_PASSWORD = get_upload_password()

user_dept = st.session_state.get('user_dept')
if user_dept == "Accounting":
    password = st.text_input("Enter Password", type="password")
    if APP_PASSWORD is None:
        st.error("Upload password is not configured.")
    elif password == APP_PASSWORD:
        st.success("Access Granted")

        uploaded_file = st.file_uploader(
            "Upload your Excel or CSV file",
            type=['csv', 'xlsx']
        )
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)

            elif uploaded_file.name.endswith('.xlsx'):
                st.write("Excel file uploaded")
                df = pd.read_excel(uploaded_file)
            st.session_state["df"] = df
    
# Data cleaning
            show_basic_info(df)
            show_missing_values(df)
            cleaned_SalesDF= sales_cleaning(df)
            cleaned_ExpenseDF= expense_cleaning(df)
                
# Create/Open a connection to the database file
            conn = sqlite3.connect('finance_data.db')
            cleaned_SalesDF.to_sql("cleaned_SalesDF", conn, if_exists="replace", index=False)
            cleaned_ExpenseDF.to_sql("cleaned_ExpenseDF", conn, if_exists="replace", index=False)
            conn.close()
            dashboard_creation(cleaned_SalesDF, cleaned_ExpenseDF)
    else:
        if password != '':
            st.warning("Wrong password. Showing the public view.")
            show_public_view()
        
else:
    show_public_view()
        
  
  
 

