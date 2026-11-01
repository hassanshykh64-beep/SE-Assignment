import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/students"

st.title("Student Management System (Task 1)")

def load_data():
    res = requests.get(API_URL)
    if res.status_code == 200:
        return res.json()
    return []

students = load_data()
st.subheader("All Students Record")
st.table(students)

st.subheader("Add New Student")
with st.form("add_form"):
    name = st.text_input("Name")
    dept = st.text_input("Department")
    email = st.text_input("Email")
    if st.form_submit_button("Add Student"):
        requests.post(API_URL, json={"name": name, "department": dept, "email": email})
        st.success("Added!")
        st.rerun() 

st.subheader("Update Student")
update_id = st.number_input("Enter Student ID to Update", min_value=1, step=1)
u_name = st.text_input("New Name")
u_dept = st.text_input("New Department")
u_email = st.text_input("New Email")
if st.button("Update"):
    requests.put(f"{API_URL}/{update_id}", json={"name": u_name, "department": u_dept, "email": u_email})
    st.success("Updated!")
    st.rerun()

st.subheader("Delete Student")
del_id = st.number_input("Enter Student ID to Delete", min_value=1, step=1)
if st.button("Delete"):
    requests.delete(f"{API_URL}/{del_id}")
    st.warning("Deleted!")
    st.rerun()