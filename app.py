# RQS/POGG1 Progress Tracking Dashboard - Based on Salesforce Export
import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# Page configuration
st.set_page_config(
    page_title="RQS/POGG1 Tracking Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data storage
if 'rqs_data' not in st.session_state:
    # Load initial data from CSV if it exists, otherwise use sample data
    try:
        st.session_state.rqs_data = pd.read_csv('rqs_cleaned_data.csv').to_dict('records')
    except FileNotFoundError:
        # Sample data based on actual Salesforce export structure
        st.session_state.rqs_data = [
            {
                'RQS': 12769,
                'Date_RQS_Received': '2025-04-30',
                'Document_Start_Date': '2025-05-19',
                'Vendor': 'El Grupo Vida Inc',
                'Description': 'Grant award for DAA in order to assist individuals and families complete complicated public benefits applications for access to services.',
                'Original_Amount': 125000,
                'PCS_Assigned_Staff': 'Donald Southworth',
                'Status': 'In Draft',
                'SOS_GS': True,
                'SAM_Record': False,
                'CORE_Number': '',
                'Contract_Record_Number': 10078,
                'Record_Type': 'Purchase Order',
                'Contract_Type': 'Purchase Order Grant',
                'Contract_Name': 'El Grupo_DAA_10078_POGG1 KAAA 2026-XXXX_BY26',
                'Active_Stage': 'Drafting',
                'Last_Modified_By': 'Don Southworth',
                'Status_Category': 'In Process',
                'Timeline_Events': [
                    '05/19/2025: RQS in-review. DS',
                    '06/02/2025: Entered in CORE Budget & SOW in progress'
                ]
            },
            {
                'RQS': 12849,
                'Date_RQS_Received': '2025-05-09',
                'Document_Start_Date': '2025-05-19',
                'Vendor': 'County of Archuleta',
                'Description': 'Grant award for DAA in order to assist individuals and families complete complicated public benefits applications for access to services.',
                'Original_Amount': 25000,
                'PCS_Assigned_Staff': 'Donald Southworth',
                'Status': 'In Draft',
                'SOS_GS': True,
                'SAM_Record': False,
                'CORE_Number': '',
                'Contract_Record_Number': 10077,
                'Record_Type': 'Purchase Order',
                'Contract_Type': 'Purchase Order Grant',
                'Contract_Name': 'County of Archuleta_DAA_10077_POGG1 KAAA 2026-XXXX_BY26',
                'Active_Stage': 'Drafting',
                'Last_Modified_By': 'Don Southworth',
                'Status_Category': 'In Process',
                'Timeline_Events': [
                    '05/19/2025: RQS in-review. DS',
                    '06/03/25: Entered in CORE Budget & SOW in progress'
                ]
            }
        ]

# Helper functions
def format_currency(amount):
    return f"${amount:,.2f}"

def calculate_progress_percentage(status, active_stage):
    """Calculate progress percentage based on status and active stage"""
    stage_progress = {
        'Draft': 10,
        'In Draft': 20,
        'RQS Review': 35,
        'CORE Entry': 50,
        'Budget & SOW': 65,
        'Drafting': 25,
        'Review': 40,
        'Approval': 75,
        'Executed': 100
    }
    return stage_progress.get(active_stage, stage_progress.get(status, 0))

# Main Title and Header
st.title("🏛️ RQS/POGG1 Progress Tracking Dashboard")
st.markdown("*Colorado State Government - Purchase Order Grants Given (POGG1) Tracking System*")
st.markdown("---")

# Sidebar - Summary Statistics
st.sidebar.header("📊 Dashboard Summary")
if st.session_state.rqs_data:
    df = pd.DataFrame(st.session_state.rqs_data)
    total_amount = df['Original_Amount'].sum()
    avg_amount = df['Original_Amount'].mean()
    total_grants = len(df)
    
    st.sidebar.metric("Total Grants", total_grants)
    st.sidebar.metric("Total Amount", format_currency(total_amount))
    st.sidebar.metric("Average Grant", format_currency(avg_amount))
    
    # Status distribution
    st.sidebar.subheader("Status Distribution")
    status_counts = df['Status'].value_counts()
    for status, count in status_counts.items():
        st.sidebar.write(f"• {status}: {count}")

# Main Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "➕ Add New RQS", "📈 Analytics", "⚙️ Manage"])

# Tab 1: Overview
with tab1:
    if st.session_state.rqs_data:
        df = pd.DataFrame(st.session_state.rqs_data)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            vendor_filter = st.multiselect(
                "Filter by Vendor", 
                options=df['Vendor'].unique(),
                default=df['Vendor'].unique()
            )
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['Status'].unique(),
                default=df['Status'].unique()
            )
        with col3:
            staff_filter = st.multiselect(
                "Filter by Assigned Staff",
                options=df['PCS_Assigned_Staff'].unique(),
                default=df['PCS_Assigned_Staff'].unique()
            )
        
        # Apply filters
        filtered_df = df[
            (df['Vendor'].isin(vendor_filter)) &
            (df['Status'].isin(status_filter)) &
            (df['PCS_Assigned_Staff'].isin(staff_filter))
        ]
        
        # Display data table
        st.subheader("Current RQS/POGG1 Entries")
        
        # Format display data
        display_df = filtered_df.copy()
        display_df['Original_Amount'] = display_df['Original_Amount'].apply(format_currency)
        display_df['Progress_%'] = display_df.apply(
            lambda row: f"{calculate_progress_percentage(row['Status'], row['Active_Stage'])}%", 
            axis=1
        )
        
        # Select columns for display
        display_columns = ['RQS', 'Vendor', 'Original_Amount', 'Status', 'Active_Stage', 
                         'PCS_Assigned_Staff', 'Date_RQS_Received', 'Progress_%']
        
        st.dataframe(
            display_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
        # Timeline view for selected RQS
        st.subheader("Timeline Details")
        selected_rqs = st.selectbox(
            "Select RQS for detailed timeline:",
            options=filtered_df['RQS'].tolist(),
            format_func=lambda x: f"RQS {x} - {filtered_df[filtered_df['RQS']==x]['Vendor'].iloc[0]}"
        )
        
        if selected_rqs:
            selected_record = filtered_df[filtered_df['RQS'] == selected_rqs].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Grant Details:**")
                st.write(f"• **Vendor:** {selected_record['Vendor']}")
                st.write(f"• **Amount:** {format_currency(selected_record['Original_Amount'])}")
                st.write(f"• **Contract #:** {selected_record['Contract_Record_Number']}")
                st.write(f"• **Status:** {selected_record['Status']}")
                st.write(f"• **Active Stage:** {selected_record['Active_Stage']}")
            
            with col2:
                st.write("**Timeline Events:**")
                if 'Timeline_Events' in selected_record and selected_record['Timeline_Events']:
                    try:
                        # Handle both string and list formats
                        events = selected_record['Timeline_Events']
                        if isinstance(events, str):
                            events = json.loads(events.replace("'", '"'))
                        
                        for event in events:
                            st.write(f"• {event}")
                    except:
                        st.write("• Timeline data needs formatting")
                else:
                    st.write("• No timeline events recorded")

# Tab 2: Add New RQS
with tab2:
    st.subheader("Add New RQS Entry")
    
    with st.form("new_rqs_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            new_rqs = st.number_input("RQS Number*", min_value=1, step=1)
            new_vendor = st.text_input("Vendor*")
            new_amount = st.number_input("Original Amount ($)*", min_value=0, step=1000)
            new_staff = st.selectbox("Assigned Staff*", 
                                   options=["Donald Southworth", "Other"], 
                                   index=0)
            if new_staff == "Other":
                new_staff = st.text_input("Enter staff name:")
        
        with col2:
            new_date_received = st.date_input("Date RQS Received*", value=date.today())
            new_doc_start = st.date_input("Document Start Date*", value=date.today())
            new_status = st.selectbox("Status*", 
                                    options=["Draft", "In Draft", "RQS Review", "CORE Entry", 
                                           "Budget & SOW", "Approval", "Executed"])
            new_active_stage = st.selectbox("Active Stage*",
                                          options=["Drafting", "Review", "CORE Entry", 
                                                 "Budget & SOW", "Approval", "Executed"])
        
        new_description = st.text_area("Description*", 
                                     value="Grant award for DAA in order to assist individuals and families complete complicated public benefits applications for access to services.")
        
        new_contract_num = st.number_input("Contract Record Number", min_value=0, step=1)
        new_core_num = st.text_input("CORE Number (if applicable)")
        
        # Checkboxes
        col3, col4 = st.columns(2)
        with col3:
            new_sos_gs = st.checkbox("SOS GS", value=True)
        with col4:
            new_sam_record = st.checkbox("SAM Record", value=False)
        
        new_notes = st.text_area("Initial Timeline Entry")
        
        if st.form_submit_button("Add RQS Entry", type="primary"):
            if new_rqs and new_vendor and new_amount > 0:
                new_entry = {
                    'RQS': new_rqs,
                    'Date_RQS_Received': new_date_received.strftime('%Y-%m-%d'),
                    'Document_Start_Date': new_doc_start.strftime('%Y-%m-%d'),
                    'Vendor': new_vendor,
                    'Description': new_description,
                    'Original_Amount': new_amount,
                    'PCS_Assigned_Staff': new_staff,
                    'Status': new_status,
                    'SOS_GS': new_sos_gs,
                    'SAM_Record': new_sam_record,
                    'CORE_Number': new_core_num,
                    'Contract_Record_Number': new_contract_num,
                    'Record_Type': 'Purchase Order',
                    'Contract_Type': 'Purchase Order Grant',
                    'Contract_Name': f"{new_vendor}_DAA_{new_contract_num}_POGG1",
                    'Active_Stage': new_active_stage,
                    'Last_Modified_By': new_staff,
                    'Status_Category': 'In Process',
                    'Timeline_Events': [f"{date.today().strftime('%m/%d/%Y')}: {new_notes}"] if new_notes else []
                }
                
                st.session_state.rqs_data.append(new_entry)
                st.success(f"✅ RQS {new_rqs} added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

# Tab 3: Analytics
with tab3:
    if st.session_state.rqs_data:
        df = pd.DataFrame(st.session_state.rqs_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Grant Distribution by Vendor")
            vendor_amounts = df.groupby('Vendor')['Original_Amount'].sum().sort_values(ascending=False)
            st.bar_chart(vendor_amounts)
            
            st.subheader("Status Distribution")
            status_counts = df['Status'].value_counts()
            st.bar_chart(status_counts)
        
        with col2:
            st.subheader("Progress Overview")
            df['Progress_%'] = df.apply(
                lambda row: calculate_progress_percentage(row['Status'], row['Active_Stage']),
                axis=1
            )
            progress_df = df[['RQS', 'Vendor', 'Progress_%']].set_index('RQS')
            st.bar_chart(progress_df['Progress_%'])
            
            st.subheader("Monthly RQS Volume")
            df['Date_RQS_Received'] = pd.to_datetime(df['Date_RQS_Received'])
            monthly_counts = df.groupby(df['Date_RQS_Received'].dt.to_period('M')).size()
            if len(monthly_counts) > 0:
                st.line_chart(monthly_counts)

# Tab 4: Manage
with tab4:
    if st.session_state.rqs_data:
        st.subheader("Update Existing RQS Entries")
        
        df = pd.DataFrame(st.session_state.rqs_data)
        
        # Select RQS to update
        rqs_to_update = st.selectbox(
            "Select RQS to update:",
            options=df['RQS'].tolist(),
            format_func=lambda x: f"RQS {x} - {df[df['RQS']==x]['Vendor'].iloc[0]}"
        )
        
        if rqs_to_update:
            current_record = df[df['RQS'] == rqs_to_update].iloc[0]
            
            with st.form("update_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    updated_status = st.selectbox(
                        "Status", 
                        options=["Draft", "In Draft", "RQS Review", "CORE Entry", "Budget & SOW", "Approval", "Executed"],
                        index=["Draft", "In Draft", "RQS Review", "CORE Entry", "Budget & SOW", "Approval", "Executed"].index(current_record['Status'])
                    )
                    updated_stage = st.selectbox(
                        "Active Stage",
                        options=["Drafting", "Review", "CORE Entry", "Budget & SOW", "Approval", "Executed"],
                        index=["Drafting", "Review", "CORE Entry", "Budget & SOW", "Approval", "Executed"].index(current_record['Active_Stage'])
                    )
                
                with col2:
                    updated_core = st.text_input("CORE Number", value=str(current_record.get('CORE_Number', '')))
                    updated_staff = st.text_input("Last Modified By", value=current_record['Last_Modified_By'])
                
                new_timeline_entry = st.text_area("Add Timeline Entry")
                
                if st.form_submit_button("Update RQS", type="primary"):
                    # Update the record
                    for i, record in enumerate(st.session_state.rqs_data):
                        if record['RQS'] == rqs_to_update:
                            st.session_state.rqs_data[i]['Status'] = updated_status
                            st.session_state.rqs_data[i]['Active_Stage'] = updated_stage
                            st.session_state.rqs_data[i]['CORE_Number'] = updated_core
                            st.session_state.rqs_data[i]['Last_Modified_By'] = updated_staff
                            
                            if new_timeline_entry:
                                timeline_entry = f"{date.today().strftime('%m/%d/%Y')}: {new_timeline_entry}"
                                if 'Timeline_Events' not in st.session_state.rqs_data[i]:
                                    st.session_state.rqs_data[i]['Timeline_Events'] = []
                                st.session_state.rqs_data[i]['Timeline_Events'].append(timeline_entry)
                            
                            break
                    
                    st.success(f"✅ RQS {rqs_to_update} updated successfully!")
                    st.rerun()
        
        # Export functionality
        st.subheader("Export Data")
        if st.button("📥 Export to CSV"):
            df = pd.DataFrame(st.session_state.rqs_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"rqs_pogg1_export_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("*RQS/POGG1 Tracking Dashboard | Colorado State Government | Based on Salesforce Export*")
