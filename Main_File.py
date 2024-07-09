import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Read the dataset
df = pd.read_excel("Global_Superstore.xlsx")

# Setting the title of the app
st.title("Business Programming TEC")

# Password input
password = st.text_input("Enter password:", type="password")

if 'count' not in st.session_state:
    st.session_state.count = 2

# Correct password
correct_password = "Password"

if password == correct_password:
    st.session_state.count = 2  # Reset count on successful login
    st.success("Logged in successfully!")

    st.header("What do you want to know?")
    tq1 = "Which product category generates the most sales?"
    tq2 = "What is the average shipping cost per category?"
    tq3 = "Which market generates the most and least profit?"
    tq4 = "What is the amount of products sold per market?"

    if st.button(tq1):
        sales_total = df["Sales"].sum()
        data = df.groupby("Category")["Sales"].sum()
        fig, ax = plt.subplots()
        data.plot.pie(autopct="%.2f%%", ax=ax)
        ax.set_title("Sales contribution per category")
        st.pyplot(fig)

        # Display ranking
        category_array = df['Category'].unique()
        amount_array = np.array(
            [df.groupby("Category").get_group(category)["Sales"].sum() / sales_total for category in category_array])
        sorted_array = np.sort(amount_array)[::-1]

        st.write("As you can see, all Categories almost equally contribute to the generated Sales!")
        st.write("Nonetheless, we get the following ranking:")

        for i, amount in enumerate(sorted_array):
            for category in category_array:
                if amount == df.groupby("Category").get_group(category)["Sales"].sum() / sales_total:
                    sales_sum = df.groupby("Category").get_group(category)["Sales"].sum()
                    st.write(
                        f"Rank {i + 1} --> {category} generates {amount * 100:.2f}% of total profits! The category generated  USD --> {sales_sum:.2f}")

    if st.button(tq2):
        shipping_per_category = df.groupby("Category")["Shipping Cost"].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=shipping_per_category, x="Shipping Cost", y="Category", estimator=sum, errorbar=None,
                    hue="Category", palette="muted", ax=ax)
        ax.set(title="Average shipping cost per category")
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', label_type='edge')
        st.pyplot(fig)

        category_array = df['Category'].unique()
        st.write("After analyzing the shipping cost we can conclude the following:")
        for category in category_array:
            average = df.groupby("Category").get_group(category)["Shipping Cost"].mean()
            total = df.groupby("Category").get_group(category)["Shipping Cost"].sum()
            amount_sold_per_category = df.groupby("Category").get_group(category)["Product Amount"].sum()
            average_per_unit = average / amount_sold_per_category

            st.write(
                f"Category --> '{category}' has average shipping costs of {average:.2f} USD. The total shipping costs amount to --> {total:.2f} USD")
            st.write(
                f"{amount_sold_per_category} products were sold of the category '{category}' --> Therefore, the average shipping cost per sold unit is {average_per_unit:.5f} USD")

    if st.button(tq3):
        data = df.groupby("Market")["Profit"].sum()
        fig, ax = plt.subplots()
        data.plot.pie(autopct="%.2f%%", ax=ax)
        ax.set_title("Total profit per market")
        st.pyplot(fig)

        profit_total = df["Profit"].sum()
        market_array = df['Market'].unique()
        profit_array = np.array(
            [df.groupby("Market").get_group(market)["Profit"].sum() / profit_total for market in market_array])
        sorted_profit = np.sort(profit_array)[::-1]

        st.write(
            "As you can see, all the markets contribute in different amounts to the final profit! We get the following ranking:")

        for i, profit in enumerate(sorted_profit):
            for market in market_array:
                profit_market = df.groupby("Market").get_group(market)["Profit"].sum()
                if profit == df.groupby("Market").get_group(market)["Profit"].sum() / profit_total:
                    st.write(
                        f"Rank {i + 1} --> {market} generates {profit * 100:.2f}% of total profits! The profit generated in USD --> {profit_market:.2f}")

    if st.button(tq4):
        product_amount_per_market = df.groupby("Market")["Product Amount"].sum().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=product_amount_per_market, x="Market", y="Product Amount", estimator=sum, errorbar=None,
                    hue="Market", palette="deep", ax=ax)
        ax.set(title="Amount of products sold per market")
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', label_type='edge')
        st.pyplot(fig)

        amount_sold = df["Product Amount"].sum()
        market_array = df['Market'].unique()
        sold_amount_array = np.array(
            [df.groupby("Market").get_group(market)["Product Amount"].sum() for market in market_array])
        sorted_amount_sold = np.sort(sold_amount_array)[::-1]

        st.write("After analyzing the amount of sold products per market we can conclude the following:")

        for i, amount in enumerate(sorted_amount_sold):
            for market in market_array:
                if amount == df.groupby("Market").get_group(market)["Product Amount"].sum():
                    st.write(f"Rank {i + 1} --> In market '{market}' {amount} products were sold")

        st.write(
            f"The difference between the best and worst selling market is {np.max(sorted_amount_sold) - np.min(sorted_amount_sold)} products!")
        st.write(
            f"Since this is a rather huge span between the max and min value the standard deviation is: {np.std(sorted_amount_sold)}")
        st.write(f"On the other hand the mean of the amount of products sold equals: {np.mean(sorted_amount_sold)}")
        st.write(
            "Consequently, the amount of sold products per market have a significant spread or variability from the mean!")

elif password:
    if st.session_state.count == 0:
        st.error("The system will close if failed again!")
        st.stop()
    else:
        st.error(f"Wrong password! Try again! You have {st.session_state.count} tries left!")
        st.session_state.count -= 1

    if len(password) == 0:
        st.warning("No input! Try again!")
