import streamlit as st
import pandas as pd

# Sample data for POGG1 transactions
sample_data = {
    'Transaction ID': ['POGG1-001', 'POGG1-002', 'POGG1-003', 'POGG1-004'],
    'Department': ['Health', 'Education', 'Transportation', 'Health'],
    'Event Type': ['PR05', 'PR06', 'CG07', 'CG08'],
    'Status': ['Pre-encumbrance', 'Encumbrance', 'Expenditure', 'Pre-encumbrance'],
    'Budget Utilization (%)': [45, 70, 90, 30],
    'Phase': ['Pre-encumbrance', 'Encumbrance', 'Expenditure', 'Pre-encumbrance'],
    'Amount Encumbered': [10000, 20000, 15000, 5000],
    'Amount Spent': [4500, 14000, 13500, 1500],
    'Remaining Balance': [5500, 6000, 1500, 3500]
}

df = pd.DataFrame(sample_data)

st.title('POGG1 Progress Tracking Dashboard')

# Sidebar filters
department_filter = st.sidebar.multiselect('Select Department', options=df['Department'].unique(), default=df['Department'].unique())
event_type_filter = st.sidebar.multiselect('Select Event Type', options=df['Event Type'].unique(), default=df['Event Type'].unique())
status_filter = st.sidebar.multiselect('Select Status', options=df['Status'].unique(), default=df['Status'].unique())

# Data filtering
filtered_df = df[
    (df['Department'].isin(department_filter)) &
    (df['Event Type'].isin(event_type_filter)) &
    (df['Status'].isin(status_filter))
]

# Overview
st.header('Overview')
st.dataframe(filtered_df)

# Budget Utilization
st.header('Budget Utilization')
st.bar_chart(filtered_df.set_index('Transaction ID')['Budget Utilization (%)'])

# Phase Tracking
st.header('Phase Tracking')
phase_counts = filtered_df['Phase'].value_counts()
st.bar_chart(phase_counts)

# Financial Summary
st.header('Financial Summary')
st.write('Total Amount Encumbered:', filtered_df['Amount Encumbered'].sum())
st.write('Total Amount Spent:', filtered_df['Amount Spent'].sum())
st.write('Total Remaining Balance:', filtered_df['Remaining Balance'].sum())

st.markdown('---')
st.markdown('Dashboard created for tracking POGG1 transactions in Colorado state government.')
