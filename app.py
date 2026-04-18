import oracledb as odb
import streamlit as st
import pandas as pd
#Before we start, I wanted to clarify that due to some technical issues I am working with my own database for
#this project (As instructed by Professor Selim). I am aware that there is only 80% credit for working solo,
#but I still wanted to go the extra mile and do a couple more functions to see if I can get a little more credit.

#To start off, we must establish a connection to our database.
connect = odb.connect(user = 'retail_user', password = 'password', dsn = 'localhost:1521/XEPDB1')#
cursor = connect.cursor()
#This also initializes our "home" UI page, which will be important for the program.
if "page" not in st.session_state:
    st.session_state.page = "home"

#This function will allow us to go through the several different sections in our app.
def go_to(page_name):
    st.session_state.page = page_name

#This function acts as a basis for my app to display desired information to the user.
def run_query(query, params = None):
    cursor.execute(query, params or {})
    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()
    if not rows:
        st.warning("No results found.")
        return
    
    df = pd.DataFrame(rows, columns = columns)
    st.dataframe(df, use_container_width = True)

#From this point, I will write different feature functions for our app. Our functions will likely start with 
#user-given parameters. Then, we will use a query to pull information that fits the user's request, and display
#it to the user.

#For the first feature, we will simply view all of the customers in our database.
def view_all_cus_screen():
    st.title("All Customers On Record")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Customer Results"):
            query = """
            SELECT CustomerID, Year_Birth, EducationCode, MaritalStatusCode, Income
            FROM CUSTOMER
            """
            params = {}

            run_query(query, params)

    with col2:
        if st.button("Back to Home"):
            go_to("home")


#For the second feature, the function will check for users who joined within a given date range.
def new_users_within_date_screen():
    st.title("Users Who Joined Within a Given Date Range")
    start = st.text_input("Enter Your Starting Date (YYYY-MM-DD): ", key = "start_date")
    end = st.text_input("Enter Your Ending Date (YYYY-MM-DD): ", key = "end_date")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Search Orders"):
            if not start.strip() or not end.strip():
                st.error("Error: One or more of your fields is missing.")
                return
            
            if start > end:
                st.error("Error: Your start date cannot be larger than your end date.")
                return

            query = """
            SELECT CustomerID, Dt_Customer
            FROM CUSTOMER
            WHERE (Dt_Customer BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD') AND TO_DATE(:end_date, 'YYYY-MM-DD'))
            """

            params = {
                "start_date": start,
                "end_date": end
            }

            run_query(query, params)

    with col2:
        if st.button("Back to Home"):
            go_to("home")


#For the third feature, the function will check for a customer's purchase history.
def customer_purchase_history_screen():
    st.title("Customer Purchase History")
    cus_id = st.text_input("Enter your customer's ID: ", key = "desired_cus_id")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Search Purchase History"):
            if not cus_id.strip():
                st.error("Error: Your field is missing.")
                return
            
            if not cus_id.isdigit():
                st.error("Error: Your ID must be a number.")
                return

            query = """
            SELECT c.CustomerID,
            cp.MntWines, cp.MntFruits, cp.MntMeatProducts,
            cp.MntFishProducts, cp.MntSweetProducts, cp.MntGoldProds
            FROM customer c
            JOIN customer_profile cp ON c.CustomerID = cp.CustomerID
            WHERE c.CustomerID = :desired_cus_id
            """
            params = {
            "desired_cus_id": int(cus_id)
            }

            run_query(query, params)

    with col2:
        if st.button("Back to Home"):
            go_to("home")


#For the fourth feature, the function will provide customer education levels.
def cus_edu_levels_screen():
    st.title("Levels of Customer Education")
    edu_lvl = st.text_input("Enter the Desired Education Level: ", key = "desired_edu")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Search Customers With Matching Education Level"):
            if not edu_lvl:
                st.error("Error: Your field is missing.")
                return
            
            query = """
            SELECT CustomerID, EducationCode, Income
            FROM customer
            WHERE EducationCode = :desired_edu
            """
            params = {
                "desired_edu": edu_lvl
            }

            run_query(query, params)

    with col2:
        if st.button("Back to Home"):
            go_to("home")       


#For the fifth feature, the function will check for the top 10 highest spending customers on the database.
def top_spending_cus_screen():
    st.title("Top 10 All-Time Highest Spenders")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Top 10 Spender Results"):
            query = """
            SELECT c.CustomerID,
            SUM(
                NVL(cp.MntWines,0) + NVL(cp.MntFruits,0) + NVL(cp.MntMeatProducts,0) +
                NVL(cp.MntFishProducts,0) + NVL(cp.MntSweetProducts,0) + NVL(cp.MntGoldProds,0)
            ) AS total_spent
            FROM customer c
            JOIN customer_profile cp ON c.CustomerID = cp.CustomerID
            GROUP BY c.CustomerID
            ORDER BY total_spent DESC
            FETCH FIRST 10 ROWS ONLY
            """
            params = {}

            run_query(query, params)
    
    with col2:
        if st.button("Back to Home"):
            go_to("home")

#For the sixth feature, the function will pull customers who have had no previous interactions with campaigns.
def customers_no_campaign_screen():
    st.title("Customers With No Campaign Activity")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Find Customers"):
            query = """
            SELECT c.CustomerID
            FROM customer c
            LEFT JOIN customer_campaign cc ON c.CustomerID = cc.CustomerID
            WHERE cc.CustomerID IS NULL
            """

            run_query(query, {})

    with col2:
        if st.button("Back to Home"):
            go_to("home")

#For the seventh feature, this function will pull the performance of each campaign
def campaign_performance_screen():
    st.title("Campaign Performance")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Campaign Results"):
            query = """
            SELECT c.CampaignName, COUNT(*) AS responses
            FROM campaign c
            JOIN customer_campaign cc ON c.CampaignID = cc.CampaignID
            WHERE cc.Response = 1
            GROUP BY c.CampaignName
            ORDER BY responses DESC
            """

            run_query(query, {})

    with col2:
        if st.button("Back to Home"):
            go_to("home")


#For the eighth and final category, the function will find customers within a specified income range.
def search_customers_by_income_screen():
    st.title("Search Customers by Income Range")
    min_income = st.text_input("Enter Minimum Income:", key="min_income")
    max_income = st.text_input("Enter Maximum Income:", key="max_income")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Search Customers"):
            if not min_income.strip() or not max_income.strip():
                st.error("Error: One or more fields are missing.")
                return
            
            if not min_income.isdigit() or not max_income.isdigit():
                st.error("Error: Your values must both be numbers.")
                return

            query = """
            SELECT CustomerID, Income, EducationCode, MaritalStatusCode
            FROM customer
            WHERE Income BETWEEN :min_inc AND :max_inc
            ORDER BY Income DESC
            """

            params = {
                "min_inc": int(min_income),
                "max_inc": int(max_income)
            }

            run_query(query, params)

    with col2:
        if st.button("Back to Home"):
            go_to("home")

#After defining all of the functions, we will make a home screen with all of the required buttons to reach
#each function.
def home_screen():
    st.title("Retail CSL Dashboard")
    st.write("Select an Option:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("View All Customers"):
            go_to("view_all_cus")

        if st.button("New Users Who Joined Within a Given Date Range"):
            go_to("new_users_within_date")

        if st.button("View a Customer's Purchase History"):
            go_to("customer_purchase_history")

        if st.button("View Education Levels of Customers"):
            go_to("cus_edu_levels")

    with col2:
        if st.button("View Top Spending Customers"):
            go_to("top_spending_cus")

        if st.button("View Customers With No Recorded Campaign Activity"):
            go_to("customers_no_campaign")

        if st.button("View Campaign Performance Metrics"):
            go_to("campaign_performance")

        if st.button("Search For a Specific Customer Income"):
            go_to("search_customers_by_income")


#These final if-statements check for the current session page based on given inputs.
if st.session_state.page == "home":
    home_screen()

elif st.session_state.page == "view_all_cus":
    view_all_cus_screen()

elif st.session_state.page == "new_users_within_date":
    new_users_within_date_screen()

elif st.session_state.page == "customer_purchase_history":
    customer_purchase_history_screen()

elif st.session_state.page == "cus_edu_levels":
    cus_edu_levels_screen()

elif st.session_state.page == "top_spending_cus":
    top_spending_cus_screen()

elif st.session_state.page == "customers_no_campaign":
    customers_no_campaign_screen()

elif st.session_state.page == "campaign_performance":
    campaign_performance_screen()

elif st.session_state.page == "search_customers_by_income":
    search_customers_by_income_screen()
