import streamlit as st

## Page setting

Register = st.Page(
   page= "Pages/Register.py",
   title ="Registration",
   icon = ":material/account_circle:",
   default= True, 
)
Project_1 = st.Page(
    page= "Pages/Data_analysis.py",
    title="Analysis",
    icon= ":material/analytics:",
)

        
st.logo("images/company_logo.png", size="large")        
## Navigation
pg = st.navigation(pages= [Register, Project_1] )
pg.run()