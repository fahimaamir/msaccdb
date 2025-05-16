import pandas as pd
import streamlit as st
import urllib
from sqlalchemy import create_engine, text

def access_engine(access_db):
    cnnstr = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=" + access_db
    )
    cnnurl = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(cnnstr)}"
    acc_engine = create_engine(cnnurl)
    return acc_engine

db_path = (r"C:\mfa\st_data_entry.accdb")
engine = access_engine(db_path)
#streamlit controls
st.title("Add me!")
fn = st.text_input("First Name", "Enter", 255)
ln = st.text_input("Last Name", "Enter", 255)
ad = st.text_input("Address", "Enter", 255)
ci = st.text_input("City", "Enter", 150)
re = st.selectbox("Choose your region", ("BC", "WA", "OR", "CA"))
po = st.text_input("Postal/Zip", "Enter", 16)
co = st.selectbox("Country", ("Canada", "United States"))
em = st.text_input("Email", "Enter", 255)
if st.button("Save!"):
    params = {
        "fn": fn,
        "ln": ln,
        "ad": ad,
        "ci": ci,
        "re": re,
        "po": po,
        "co": co,
        "em": em
    }
    sql = text("""Insert Into tblContact (FirstName, LastName, Address, City,
                Region, PostalZip, Country, Email) 
                Values (:fn, :ln, :ad, :ci, :re, :po, :co, :em);""")
    with engine.connect() as cnn:
        result = cnn.execute(sql, params)
        cnn.commit()
        st.write("You have been added!")
        
        sql = "Select *  From tblContact;"
        df_country = pd.read_sql(sql, engine)
        st.write(df_country)

else:
    st.write("Click save to be added.")