import streamlit as st

col1,col2,col3,col4,col5 = st.columns( 5 ,gap="small", vertical_alignment="center")


with col1:
    st.header("Column 1")
    st.write("Content for column 1")
    

with col2:
    st.header("Column 2")
    st.write("Content for column 2")
    

with col3:
    st.header("Column 3")
    st.write("Content for column 3")
    

with col4:
    st.header("Column 4")
    st.write("Content for column 4")

    
with col5:
    st.header("Column 5")
    st.write("Content for column 5")



   
    
