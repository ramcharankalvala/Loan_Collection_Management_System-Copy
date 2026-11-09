
import re

import mysql.connector
import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Loan Collection Management",
    page_icon="💰",
    layout="wide",
)

st.title("Loan Collection Management System")
st.caption("Loan portfolio | Collection performance | Risk monitoring")


# ==========================================
# DATABASE CONNECTION SETTINGS
# ==========================================

st.sidebar.header("Database Connection")

host = st.sidebar.text_input("Host", value="localhost")
port = st.sidebar.number_input("Port", value=3306, step=1)
user = st.sidebar.text_input("Username", value="root")
password = st.sidebar.text_input(
    "MySQL Password",
    type="password",
)
database = st.sidebar.text_input(
    "Database",
    value="loan_collection_synthetic",
)

connect_button = st.sidebar.button(
    "Connect to Database",
    type="primary",
)


def get_crud_connection():
    """Create a connection to the configured MySQL database."""
    return mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
    )


def fetch_data(query, params=None):
    """Run a SELECT query and return rows as dictionaries."""
    connection = None
    cursor = None

    try:
        connection = get_crud_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def valid_email(email):
    if not email:
        return True

    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email,
        )
    )


def valid_phone(phone):
    if not phone:
        return True

    return phone.isdigit() and 7 <= len(phone) <= 15


# ==========================================
# CONNECT BUTTON
# ==========================================

if connect_button:
    if not password:
        st.sidebar.error("Please enter your MySQL password.")
        st.session_state["db_connected"] = False

    else:
        test_connection = None

        try:
            test_connection = get_crud_connection()
            test_connection.close()
            test_connection = None

            st.session_state["db_connected"] = True
            st.sidebar.success("Database connected successfully!")

        except Exception as error:
            st.session_state["db_connected"] = False
            st.sidebar.error("Connection failed: " + str(error))

        finally:
            if (
                test_connection
                and test_connection.is_connected()
            ):
                test_connection.close()


if not st.session_state.get("db_connected", False):
    st.info(
        "Enter your MySQL password in the sidebar and click "
        "'Connect to Database'."
    )
    st.stop()


# ==========================================
# CREATE CUSTOMER MANAGEMENT TABLE
# ==========================================

if not st.session_state.get("managed_table_ready", False):

    connection = None
    cursor = None

    try:
        connection = get_crud_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dashboard_managed_customers (
                customer_id VARCHAR(40) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT fk_dashboard_customer
                    FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()
        st.session_state["managed_table_ready"] = True

    except Exception as error:
        st.error(
            "Customer management setup failed: " + str(error)
        )
        st.stop()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ==========================================
# LOAD DASHBOARD DATA
# ==========================================

try:
    total_loans_data = fetch_data(
        "SELECT COUNT(*) AS total_loans FROM loans"
    )

    total_customers_data = fetch_data(
        "SELECT COUNT(*) AS total_customers FROM customers"
    )

    cases = pd.DataFrame(
        fetch_data(
            """
            SELECT
                cc.case_id,
                cc.loan_id,
                cc.account_id,
                cc.customer_id,
                c.name AS customer_name,
                c.city,
                l.loan_amount,
                cc.outstanding,
                cc.days_past_due AS dpd,
                cc.risk_score,
                cc.priority_score,
                cc.priority_rank,
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
            """
        )
    )

    promises = pd.DataFrame(
        fetch_data(
            """
            SELECT
                promise_id,
                case_id,
                promise_amount,
                amount_paid,
                remaining_amount,
                promise_status,
                promise_date
            FROM promises_to_pay
            """
        )
    )

    total_loans = int(total_loans_data[0]["total_loans"])
    total_customers = int(
        total_customers_data[0]["total_customers"]
    )

except Exception as error:
    st.error("Unable to load dashboard data: " + str(error))
    st.stop()


# ==========================================
# KPI METRICS
# ==========================================

st.header("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

total_cases = len(cases)

if not cases.empty:
    cases["outstanding"] = pd.to_numeric(
        cases["outstanding"],
        errors="coerce",
    ).fillna(0)

    cases["risk_score"] = pd.to_numeric(
        cases["risk_score"],
        errors="coerce",
    ).fillna(0)

    cases["priority_score"] = pd.to_numeric(
        cases["priority_score"],
        errors="coerce",
    ).fillna(0)

    cases["dpd"] = pd.to_numeric(
        cases["dpd"],
        errors="coerce",
    ).fillna(0)

    total_outstanding = cases["outstanding"].sum()

    high_risk_cases = len(
        cases[cases["risk_score"] >= 70]
    )

else:
    total_outstanding = 0
    high_risk_cases = 0


col1.metric("Total Customers", format(total_customers, ","))
col2.metric("Total Loans", format(total_loans, ","))
col3.metric("Collection Cases", format(total_cases, ","))
col4.metric(
    "Outstanding Amount",
    "₹" + format(total_outstanding, ",.2f"),
)

col5, col6 = st.columns(2)

col5.metric(
    "High Risk Cases",
    format(high_risk_cases, ","),
)

col6.metric(
    "Promises to Pay",
    format(len(promises), ","),
)


# ==========================================
# COLLECTION ANALYTICS
# ==========================================

st.divider()
st.header("Collection Analytics")

if not cases.empty:

    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("Collection Cases by Status")

        status_counts = (
            cases["case_status"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        status_counts.columns = ["Status", "Count"]

        fig = px.bar(
            status_counts,
            x="Status",
            y="Count",
            title="Cases by Status",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with chart2:
        st.subheader("Risk Distribution")

        risk_groups = pd.cut(
            cases["risk_score"],
            bins=[-1, 39, 69, float("inf")],
            labels=[
                "Low Risk",
                "Medium Risk",
                "High Risk",
            ],
        )

        risk_counts = (
            risk_groups.value_counts()
            .reindex(
                [
                    "Low Risk",
                    "Medium Risk",
                    "High Risk",
                ],
                fill_value=0,
            )
            .reset_index()
        )

        risk_counts.columns = ["Risk Level", "Count"]

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            title="Risk Level Distribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    chart3, chart4 = st.columns(2)

    with chart3:
        st.subheader("Top 15 Collection Priorities")

        top_cases = cases.nlargest(
            15,
            "priority_score",
        )

        fig = px.bar(
            top_cases,
            x="case_id",
            y="priority_score",
            title="Priority Scores",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with chart4:
        st.subheader("Delinquency Distribution")

        fig = px.histogram(
            cases,
            x="dpd",
            nbins=20,
            title="Days Past Due",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

else:
    st.info("No collection cases available.")


# ==========================================
# COLLECTION CASE EXPLORER
# ==========================================

st.divider()
st.header("Collection Case Explorer")

if not cases.empty:

    search_case = st.text_input(
        "Search by Case ID, Loan ID or Customer ID"
    )

    filtered_cases = cases.copy()

    if search_case:
        mask = (
            filtered_cases["case_id"]
            .astype(str)
            .str.contains(
                search_case,
                case=False,
                na=False,
            )
            |
            filtered_cases["loan_id"]
            .astype(str)
            .str.contains(
                search_case,
                case=False,
                na=False,
            )
            |
            filtered_cases["customer_id"]
            .astype(str)
            .str.contains(
                search_case,
                case=False,
                na=False,
            )
        )

        filtered_cases = filtered_cases[mask]

    st.dataframe(
        filtered_cases,
        use_container_width=True,
        hide_index=True,
    )

    if not filtered_cases.empty:

        selected_case = st.selectbox(
            "Select a case to view details",
            filtered_cases["case_id"].tolist(),
        )

        st.subheader("Selected Case Details")

        st.dataframe(
            filtered_cases[
                filtered_cases["case_id"] == selected_case
            ],
            use_container_width=True,
            hide_index=True,
        )

else:
    st.info("No collection cases available.")


# ==========================================
# CUSTOMER MANAGEMENT TABS
# ==========================================

st.divider()
st.header("Customer Management")

view_tab, add_tab, edit_tab = st.tabs(
    [
        "View & Search",
        "Add Customer",
        "Edit Customer",
    ]
)


# ==========================================
# VIEW AND SEARCH CUSTOMERS
# ==========================================

with view_tab:

    st.subheader("View and Search Customers")

    customer_search = st.text_input(
        "Search by Customer ID, Name, Email or Phone",
        key="customer_search",
    )

    if customer_search:

        pattern = "%" + customer_search + "%"

        customer_rows = fetch_data(
            """
            SELECT
                customer_id,
                name,
                email,
                city,
                phone
            FROM customers
            WHERE customer_id LIKE %s
               OR name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
            ORDER BY customer_id
            LIMIT 100
            """,
            (
                pattern,
                pattern,
                pattern,
                pattern,
            ),
        )

    else:

        customer_rows = fetch_data(
            """
            SELECT
                customer_id,
                name,
                email,
                city,
                phone
            FROM customers
            ORDER BY customer_id
            LIMIT 100
            """
        )

    st.caption("Showing up to 100 matching customers.")

    st.dataframe(
        pd.DataFrame(customer_rows),
        use_container_width=True,
        hide_index=True,
    )


# ==========================================
# ADD CUSTOMER
# ==========================================

with add_tab:

    st.subheader("Add New Customer")

    st.caption(
        "A new customer ID is generated automatically."
    )

    with st.form("add_customer_form"):

        new_name = st.text_input("Customer Name")
        new_email = st.text_input("Email Address")
        new_city = st.text_input("City")
        new_phone = st.text_input("Phone Number")

        add_submitted = st.form_submit_button(
            "Add Customer"
        )

    if add_submitted:

        if not new_name.strip():
            st.error("Customer name is required.")

        elif not valid_email(new_email.strip()):
            st.error("Please enter a valid email address.")

        elif not valid_phone(new_phone.strip()):
            st.error(
                "Phone must contain 7 to 15 digits."
            )

        else:

            add_connection = None
            add_cursor = None

            try:

                add_connection = get_crud_connection()
                add_cursor = add_connection.cursor()

                # Generate the next customer ID.
                add_cursor.execute(
                    """
                    SELECT COALESCE(
                        MAX(
                            CAST(
                                SUBSTRING(customer_id, 6)
                                AS UNSIGNED
                            )
                        ),
                        0
                    ) + 1
                    FROM customers
                    WHERE customer_id REGEXP '^CUST-[0-9]+$'
                    """
                )

                result = add_cursor.fetchone()

                next_number = int(result[0] or 1)

                new_customer_id = (
                    "CUST-" + str(next_number).zfill(6)
                )

                # Insert the new customer.
                add_cursor.execute(
                    """
                    INSERT INTO customers
                        (
                            customer_id,
                            name,
                            email,
                            city,
                            phone
                        )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        new_customer_id,
                        new_name.strip(),
                        new_email.strip() or None,
                        new_city.strip() or None,
                        new_phone.strip() or None,
                    ),
                )

                # Record that this customer was created
                # through the dashboard.
                add_cursor.execute(
                    """
                    INSERT INTO dashboard_managed_customers
                        (customer_id)
                    VALUES (%s)
                    """,
                    (new_customer_id,),
                )

                add_connection.commit()

                st.success(
                    "Customer added successfully! ID: "
                    + new_customer_id
                )

                st.rerun()

            except Exception as error:

                if add_connection:
                    add_connection.rollback()

                st.error(
                    "Unable to add customer: " + str(error)
                )

            finally:

                if add_cursor:
                    add_cursor.close()

                if (
                    add_connection
                    and add_connection.is_connected()
                ):
                    add_connection.close()


# ==========================================
# EDIT DASHBOARD-CREATED CUSTOMERS
# ==========================================

with edit_tab:

    st.subheader("Edit Dashboard-Created Customer")

    st.caption(
        "Original generated challenge customers are read-only. "
        "Only customers added through this dashboard can be edited."
    )

    try:

        managed_customers = fetch_data(
            """
            SELECT
                c.customer_id,
                c.name,
                c.email,
                c.city,
                c.phone
            FROM customers c
            INNER JOIN dashboard_managed_customers d
                ON c.customer_id = d.customer_id
            ORDER BY c.customer_id
            """
        )

        if not managed_customers:

            st.info(
                "No dashboard-created customers yet. Add one first."
            )

        else:

            customer_options = {
                row["customer_id"]: row
                for row in managed_customers
            }

            selected_customer_id = st.selectbox(
                "Select customer to edit",
                options=list(customer_options.keys()),
            )

            selected_customer = customer_options[
                selected_customer_id
            ]

            with st.form("edit_customer_form"):

                edit_name = st.text_input(
                    "Customer Name",
                    value=selected_customer["name"] or "",
                )

                edit_email = st.text_input(
                    "Email Address",
                    value=selected_customer["email"] or "",
                )

                edit_city = st.text_input(
                    "City",
                    value=selected_customer["city"] or "",
                )

                edit_phone = st.text_input(
                    "Phone Number",
                    value=selected_customer["phone"] or "",
                )

                edit_submitted = st.form_submit_button(
                    "Save Customer Changes"
                )

            if edit_submitted:

                if not edit_name.strip():

                    st.error("Customer name is required.")

                elif not valid_email(edit_email.strip()):

                    st.error("Please enter a valid email address.")

                elif not valid_phone(edit_phone.strip()):

                    st.error(
                        "Phone must contain 7 to 15 digits."
                    )

                else:

                    update_connection = None
                    update_cursor = None

                    try:

                        update_connection = get_crud_connection()
                        update_cursor = update_connection.cursor()

                        update_cursor.execute(
                            """
                            UPDATE customers
                            SET
                                name = %s,
                                email = %s,
                                city = %s,
                                phone = %s
                            WHERE customer_id = %s
                            """,
                            (
                                edit_name.strip(),
                                edit_email.strip() or None,
                                edit_city.strip() or None,
                                edit_phone.strip() or None,
                                selected_customer_id,
                            ),
                        )

                        update_cursor.execute(
                            """
                            UPDATE dashboard_managed_customers
                            SET updated_at = CURRENT_TIMESTAMP
                            WHERE customer_id = %s
                            """,
                            (selected_customer_id,),
                        )

                        update_connection.commit()

                        st.success(
                            "Customer "
                            + selected_customer_id
                            + " updated successfully."
                        )

                        st.rerun()

                    except Exception as error:

                        if update_connection:
                            update_connection.rollback()

                        st.error(
                            "Unable to update customer: "
                            + str(error)
                        )

                    finally:

                        if update_cursor:
                            update_cursor.close()

                        if (
                            update_connection
                            and update_connection.is_connected()
                        ):
                            update_connection.close()

    except Exception as error:

        st.error(
            "Unable to load editable customers: "
            + str(error)
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Loan Collection Management System | Synthetic Data Analytics"
)
