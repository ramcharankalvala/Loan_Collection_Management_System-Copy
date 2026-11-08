
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# ------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------

st.set_page_config(
    page_title="Loan Collection Management",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Loan Collection Management System")
st.caption("Loan portfolio | Collection performance | Risk monitoring")

# ------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------

st.sidebar.header("Database Connection")

host = st.sidebar.text_input("MySQL Host", "localhost")
port = st.sidebar.number_input("Port", value=3306)
user = st.sidebar.text_input("Username", "root")
password = st.sidebar.text_input(
    "MySQL Password",
    type="password"
)

database = st.sidebar.text_input(
    "Database",
    "loan_collection_db"
)

# ------------------------------------------
# DATABASE QUERY FUNCTION
# ------------------------------------------

def fetch_data(connection, query):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(records)


# ------------------------------------------
# CONNECT AND LOAD DATA
# ------------------------------------------

if not password:
    st.info("Enter your MySQL password in the sidebar to open the dashboard.")
    st.stop()

try:
    connection = mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database
    )

    st.sidebar.success("MySQL connected successfully!")

    cases = fetch_data(
        connection,
        """
        SELECT
            cc.case_id,
            cc.loan_id,
            cc.customer_id,
            c.name AS customer_name,
            c.city,
            l.loan_amount,
            cc.priority_rank,
            cc.priority_score,
            cc.outstanding,
            cc.dpd,
            cc.case_status,
            cc.action_status,
            cc.dispute_status,
            cc.hardship_status,
            cc.contact_status
        FROM collection_cases cc
        LEFT JOIN customers c
            ON cc.customer_id = c.customer_id
        LEFT JOIN loans l
            ON cc.loan_id = l.loan_id
        ORDER BY cc.priority_rank
        """
    )

    priorities = fetch_data(
        connection,
        """
        SELECT
            loan_id,
            priority_rank,
            priority_score,
            risk_score,
            balance_score,
            dpd_score,
            hardship_flag,
            dispute_flag,
            contact_restricted
        FROM collection_priority
        ORDER BY priority_rank
        """
    )

    promises = fetch_data(
        connection,
        """
        SELECT
            promise_id,
            loan_id,
            customer_id,
            promise_amount,
            amount_paid,
            remaining_amount,
            promise_date,
            promise_status
        FROM promises_to_pay
        """
    )

    connection.close()

except Exception as error:
    st.error("Unable to load dashboard data.")
    st.error(str(error))
    st.stop()


# ------------------------------------------
# CHECK DATA
# ------------------------------------------

if cases.empty:
    st.warning("No collection cases found in the database.")
    st.stop()


# ------------------------------------------
# KPI METRICS
# ------------------------------------------

total_loans = cases["loan_id"].nunique()
total_cases = len(cases)

total_outstanding = pd.to_numeric(
    cases["outstanding"], errors="coerce"
).fillna(0).sum()

average_dpd = pd.to_numeric(
    cases["dpd"], errors="coerce"
).fillna(0).mean()

total_promised = pd.to_numeric(
    promises["promise_amount"], errors="coerce"
).fillna(0).sum()

total_paid = pd.to_numeric(
    promises["amount_paid"], errors="coerce"
).fillna(0).sum()

total_remaining = pd.to_numeric(
    promises["remaining_amount"], errors="coerce"
).fillna(0).sum()

st.subheader("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Loans", f"{total_loans:,}")
col2.metric("Collection Cases", f"{total_cases:,}")
col3.metric("Outstanding Loans", f"₹{total_outstanding:,.2f}")
col4.metric("Average DPD", f"{average_dpd:.1f} days")

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Total Promised", f"₹{total_promised:,.2f}")
col2.metric("Total Paid", f"₹{total_paid:,.2f}")
col3.metric("Remaining Promises", f"₹{total_remaining:,.2f}")

st.divider()


# ------------------------------------------
# COLLECTION PRIORITY CHART
# ------------------------------------------

st.subheader("Collection Priority Analysis")

if not priorities.empty:
    priority_chart = px.bar(
        priorities,
        x="loan_id",
        y="priority_score",
        color="priority_score",
        text="priority_score",
        title="Priority Score by Loan",
        labels={
            "loan_id": "Loan ID",
            "priority_score": "Priority Score"
        }
    )

    st.plotly_chart(priority_chart, use_container_width=True)

    risk_chart = px.bar(
        priorities,
        x="loan_id",
        y="risk_score",
        color="risk_score",
        title="Risk Score by Loan"
    )

    st.plotly_chart(risk_chart, use_container_width=True)


# ------------------------------------------
# COLLECTION ACTION DISTRIBUTION
# ------------------------------------------

st.subheader("Collection Action Distribution")

action_counts = (
    cases["action_status"]
    .fillna("UNKNOWN")
    .value_counts()
    .rename_axis("Action")
    .reset_index(name="Cases")
)

action_chart = px.pie(
    action_counts,
    names="Action",
    values="Cases",
    title="Cases by Action Status",
    hole=0.45
)

st.plotly_chart(action_chart, use_container_width=True)


# ------------------------------------------
# PROMISE TO PAY ANALYSIS
# ------------------------------------------

st.subheader("Promise-to-Pay Analysis")

if not promises.empty:
    promise_summary = pd.DataFrame({
        "Category": ["Promised", "Paid", "Remaining"],
        "Amount": [
            total_promised,
            total_paid,
            total_remaining
        ]
    })

    promise_chart = px.bar(
        promise_summary,
        x="Category",
        y="Amount",
        color="Category",
        text_auto=".2f",
        title="Promise Payment Performance"
    )

    st.plotly_chart(
        promise_chart,
        use_container_width=True
    )


# ------------------------------------------
# DELINQUENCY ANALYSIS
# ------------------------------------------

st.subheader("Delinquency Analysis")

dpd_chart = px.bar(
    cases,
    x="loan_id",
    y="dpd",
    color="dpd",
    title="Days Past Due by Loan",
    labels={
        "loan_id": "Loan ID",
        "dpd": "Days Past Due"
    }
)

st.plotly_chart(dpd_chart, use_container_width=True)


# ------------------------------------------
# COLLECTION CASE FILTERS
# ------------------------------------------

st.subheader("Collection Case Explorer")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_action = st.selectbox(
        "Filter by Action Status",
        ["All"] + sorted(
            cases["action_status"].dropna().unique().tolist()
        )
    )

with filter_col2:
    selected_status = st.selectbox(
        "Filter by Case Status",
        ["All"] + sorted(
            cases["case_status"].dropna().unique().tolist()
        )
    )

filtered_cases = cases.copy()

if selected_action != "All":
    filtered_cases = filtered_cases[
        filtered_cases["action_status"] == selected_action
    ]

if selected_status != "All":
    filtered_cases = filtered_cases[
        filtered_cases["case_status"] == selected_status
    ]

search = st.text_input(
    "Search by Customer Name or Loan ID"
)

if search:
    mask = (
        filtered_cases["customer_name"]
        .fillna("")
        .str.contains(search, case=False)
        |
        filtered_cases["loan_id"]
        .fillna("")
        .str.contains(search, case=False)
    )

    filtered_cases = filtered_cases[mask]

st.dataframe(
    filtered_cases,
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------
# CUSTOMER DETAILS
# ------------------------------------------

st.subheader("Customer and Loan Details")

st.dataframe(
    cases[
        [
            "customer_name",
            "customer_id",
            "city",
            "loan_id",
            "loan_amount",
            "outstanding",
            "dpd",
            "action_status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.success("Dashboard data loaded successfully.")
