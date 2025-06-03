import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for data storage
if 'pogg1_data' not in st.session_state:
    st.session_state.pogg1_data = []

st.title("POGG1 Progress Tracker")
st.markdown("Manually track Purchase Order Grants Given (POGG1) progress")

# Manual Data Entry Form
with st.expander("Add New POGG1 Entry", expanded=True):
    with st.form("pogg1_form"):
        col1, col2 = st.columns(2)
        with col1:
            pogg_id = st.text_input("POGG1 ID*")
            department = st.selectbox("Department*", ["Health", "Education", "Transportation", "Other"])
            amount = st.number_input("Total Amount ($)*", min_value=0)
            
        with col2:
            status = st.selectbox("Status*", ["Draft", "Pre-Encumbrance", "Encumbrance", "Expenditure", "Completed"])
            progress = st.slider("Progress (%)", 0, 100, 50)
            last_updated = st.date_input("Last Updated", datetime.today())
        
        notes = st.text_area("Additional Notes")
        
        if st.form_submit_button("Add Entry"):
            if not pogg_id:
                st.error("POGG1 ID is required")
            else:
                new_entry = {
                    "POGG1 ID": pogg_id,
                    "Department": department,
                    "Amount": amount,
                    "Status": status,
                    "Progress": progress,
                    "Last Updated": last_updated.strftime("%Y-%m-%d"),
                    "Notes": notes
                }
                st.session_state.pogg1_data.append(new_entry)
                st.success("Entry added successfully!")

# Data Display and Management
if st.session_state.pogg1_data:
    df = pd.DataFrame(st.session_state.pogg1_data)
    
    # Filters
    st.sidebar.header("Filters")
    selected_dept = st.sidebar.multiselect("Filter by Department", df['Department'].unique())
    selected_status = st.sidebar.multiselect("Filter by Status", df['Status'].unique())
    
    if selected_dept:
        df = df[df['Department'].isin(selected_dept)]
    if selected_status:
        df = df[df['Status'].isin(selected_status)]
    
    # Main Display
    st.subheader("Current POGG1 Entries")
    st.dataframe(df.style.format({'Amount': '${:,.2f}'}), use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Progress Distribution")
        st.bar_chart(df.set_index('POGG1 ID')['Progress'])
    
    with col2:
        st.subheader("Budget Utilization")
        st.metric("Total Amount", f"${df['Amount'].sum():,.2f}")
        st.metric("Average Progress", f"{df['Progress'].mean():.1f}%")
    
    # Edit/Delete Functionality
    st.subheader("Manage Entries")
    edit_id = st.selectbox("Select Entry to Edit", df['POGG1 ID'])
    edit_entry = df[df['POGG1 ID'] == edit_id].iloc[0].to_dict()
    
    with st.form("edit_form"):
        new_progress = st.slider("Update Progress", 0, 100, int(edit_entry['Progress']))
        new_status = st.selectbox("Update Status", ["Draft", "Pre-Encumbrance", "Encumbrance", "Expenditure", "Completed"], 
                                index=["Draft", "Pre-Encumbrance", "Encumbrance", "Expenditure", "Completed"].index(edit_entry['Status']))
        new_notes = st.text_area("Update Notes", edit_entry['Notes'])
        
        if st.form_submit_button("Update Entry"):
            for entry in st.session_state.pogg1_data:
                if entry['POGG1 ID'] == edit_id:
                    entry['Progress'] = new_progress
                    entry['Status'] = new_status
                    entry['Notes'] = new_notes
                    entry['Last Updated'] = datetime.today().strftime("%Y-%m-%d")
            st.experimental_rerun()
else:
    st.info("No entries yet. Use the form above to add new POGG1 entries.")
