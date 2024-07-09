import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Evidence(tk.Tk):

    def __init__(self):

        self.title = "Business_Programming_TEC"
        self.geometry = "500x350"
        self.tq1 = "Which product category generates the most sales?"
        self.tq2 = "What is the average shipping cost per category?"
        self.tq3 = "Which market generates the most and least profit?"
        self.tq4 = "What is the amount of products sold per market?"
        self.background = '#F5F4F0'
        self.count = 2
        #file read
        self.df = pd.read_excel("Global_Superstore.xlsx")
        self.GUI_Launch()

    def GUI_Launch(self):

        # initializing the GUI
        root = tk.Tk()
        root.config(bg=self.background)
        root.title(self.title)
        # defining the size of the GUI
        root.geometry(self.geometry)

        # Creating the main_frame that will show the other frames
        main_frame = tk.Frame(root)

        # Bind the <Return> key to the move_next_page function
        root.bind('<Return>', lambda event=None: self.move_next_page())
        # Bind <Escape> key to quit the application
        root.bind("<Escape>", quit)

        # Code for the first page or Login_Page
        self.page_1 = tk.Frame(main_frame)
        self.page_1_lb = tk.Label(self.page_1, text='Enter password:', font=('Bold', 15))
        self.page_1_lb.pack()
        self.page_1_entry = tk.Entry(self.page_1, width=40, show="*", foreground="#1877f2", bd=5, relief=tk.FLAT)
        self.page_1_entry.pack(pady=10)
        self.page_1_entry.focus_set()
        self.page_1.pack(pady=50)
        login_button = Button(self.page_1, text='Login', font=('Bold', 12), bg='#1877f2', fg='white', width=8,
                              relief=tk.FLAT, command=self.move_next_page)
        login_button.pack(pady=5)

        self.result_1_lb = tk.Label(self.page_1, text='', font=('Bold', 12), fg='red')
        self.result_1_lb.pack(pady=10)

        # Code for the second page
        self.page_2 = tk.Frame(main_frame)
        page_2_lb = tk.Label(self.page_2, text='What do you want to know?', font=('Bold', 18))
        page_2_lb.pack(pady=5)
        b1 = Button(self.page_2, text=self.tq1, font=('Bold', 12), width=50, bg='#1877f2', fg='white',relief=tk.FLAT,
                    command=self.trigger_question_1)
        b2 = Button(self.page_2, text=self.tq2, font=('Bold', 12), width=50, bg='#1877f2', fg='white',relief=tk.FLAT,
                    command=self.trigger_question_2)
        b3 = Button(self.page_2, text=self.tq3, font=('Bold', 12), width=50, bg='#1877f2', fg='white',relief=tk.FLAT,
                    command=self.trigger_question_3)
        b4 = Button(self.page_2, text=self.tq4, font=('Bold', 12), width=50, bg='#1877f2', fg='white',relief=tk.FLAT,
                    command=self.trigger_question_4)
        b5 = Button(self.page_2, text='Quit', font=('Bold', 12), bg='#FF0000', fg='white', relief=tk.FLAT, width=8,
                    command=quit)
        b1.pack(pady=5)
        b2.pack(pady=5)
        b3.pack(pady=5)
        b4.pack(pady=5)
        b5.pack(pady=5)

        # pack everything in the main_frame
        main_frame.pack(fill=tk.BOTH, expand=True)
        # crucial mainloop to run the GUI
        root.mainloop()

    def move_next_page(self):
        # Variable that stores the password
        password = "Password"

        # Loop that analyzes the password and displays user information if password is wrong
        if self.page_1_entry.get() != password:
            if self.count == 0:
                quit()
            elif self.count == 1:
                self.result_1_lb.config(text="Attention! \n Only " + str(self.count) + " try left! \n""The system will "
                                        "close if failed again!")
                self.count -= 1

            elif len(self.page_1_entry.get()) == 0:
                self.result_1_lb.config(text="No input! Try again!")

            else:
                self.result_1_lb.config(text="Wrong password! Try again! \n You have " + str(self.count) +
                                             " tries left!")
                self.count -= 1

        else:
            self.page_1.pack_forget()
            self.page_2.pack(pady=50)

    def trigger_question_1(self):
        sales = self.df["Sales"]
        sales_total = np.sum(sales)

        # Here the pie chart is created
        data = self.df.groupby("Category")["Sales"].sum()
        sns.set_theme()
        data.plot.pie(autopct="%.2f%%")
        plt.title("Sales contribution per category")
        plt.show()

        # Created an array that hold all categories
        category_array = self.df['Category'].unique()

        # A further array to display ranking in the console
        amount_array = np.array([])

        # loop that puts % of sales per category and stores values in an array
        for category in category_array:
            percent_per_category = self.df.groupby("Category").get_group(category)["Sales"].sum()/sales_total
            amount_array = np.append(amount_array, percent_per_category)

        # Now we sort the array from biggest to lowest
        sorted_array = np.sort(amount_array)[::-1]

        # Console summary for the user
        print("\n")
        print("---------------------------------------------------------------------------------"
              "\nSummary trigger question 1 \n")
        print("As you can see, all Categories almost equally contribute to the generated Sales!"
              "\nNonetheless, we get the following ranking:")

        i = 0
        # A nested loop is created to match the sorted amounts with the correct category
        for amount in sorted_array:
            for category in category_array:
                sales_sum = self.df.groupby("Category").get_group(category)["Sales"].sum()

                if amount == self.df.groupby("Category").get_group(category)["Sales"].sum()/sales_total:
                    print("Rank " + str(i+1) + " --> " + category + " generates " + f"{amount*100:.2f}" +
                          "% of total profits! The category generated  USD --> " 
                          f"{sales_sum:.2f}")
                    i += 1

    def trigger_question_2(self):
        # Here the bar plot gets initialized
        shipping_per_category = self.df.groupby("Category")["Shipping Cost"].mean().reset_index()
        sns.set_theme()
        ax = sns.barplot(data=shipping_per_category, x="Shipping Cost", y="Category",
                         estimator=sum, errorbar=None, hue="Category", palette="muted")

        # Put label on each bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', label_type='edge')

        # More specifications for the bar plot
        ax.set(title="Average shipping cost per category")
        ax.bar_label(ax.containers[0], label_type='edge')
        ax.tick_params(axis='x', rotation=1)
        plt.show()

        # Here the descriptive statistics are programmed
        category_array = self.df['Category'].unique()

        print("\n")
        print("---------------------------------------------------------------------------------"
              "\nSummary trigger question 2 \n")
        print("After analyzing the shipping cost we can conclude the following:")

        for category in category_array:
            average = self.df.groupby("Category").get_group(category)["Shipping Cost"].mean()
            total = self.df.groupby("Category").get_group(category)["Shipping Cost"].sum()
            amount_sold_per_category = self.df.groupby("Category").get_group(category)["Product Amount"].sum()
            average_per_unit = average / amount_sold_per_category

            print("Category --> '" + category + "' has average shipping costs of " + f"{average:.2f}" + "USD."
                  + " The total shipping costs amount to --> " + f"{total:.2f}" + "USD")
            print(str(amount_sold_per_category) + " products were sold of the category '" + category + "' --> "
                  + " Therefore, the average shipping cost per sold unit is " + f"{average_per_unit:.5f}"+"USD")

    def trigger_question_3(self):

        # Here the pie chart is created
        data = self.df.groupby("Market")["Profit"].sum()
        sns.set_theme()
        data.plot.pie(autopct="%.2f%%")
        plt.title("Total profit per market")
        plt.show()

        # Code for descriptive output
        profit = self.df["Profit"]
        profit_total = np.sum(profit)

        # Some further work to display ranking in the console
        profit_array = np.array([])

        # Created an array that hold all markets
        market_array = self.df['Market'].unique()

        for market in market_array:
            percent_per_market = self.df.groupby("Market").get_group(market)["Profit"].sum()/profit_total
            profit_array = np.append(profit_array, percent_per_market)

        # Now we sort the array from biggest to lowest
        sorted_profit = np.sort(profit_array)[::-1]

        # Console summary for the user
        print("\n")
        print("---------------------------------------------------------------------------------"
              "\nSummary trigger question 3 \n")
        print("As you can see, all the markets contribute in different amounts to the final profit!"
              "\nWe get the following ranking:")

        # A nested loop is created to match the sorted profits with the correct market
        i = 0
        for profit in sorted_profit:
            for market in market_array:
                profit_market = self.df.groupby("Market").get_group(market)["Profit"].sum()
                if profit == self.df.groupby("Market").get_group(market)["Profit"].sum()/profit_total:
                    print("Rank " + str(i+1) + " --> " + market + " generates " + f"{profit*100:.2f}" +
                          "% of total profits! The profit generated in USD --> " +
                          f"{profit_market:.2f}")
                    i += 1

    def trigger_question_4(self):
        product_amount_per_market = self.df.groupby("Market")["Product Amount"].sum().reset_index()
        sns.set_theme()
        ax = sns.barplot(data=product_amount_per_market, x="Market", y="Product Amount",
                         estimator=sum, errorbar=None, hue="Market",palette="deep")

        # Put label on each bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', label_type='edge')

        # More specifications for the bar plot
        ax.set(title="Amount of products sold per market")
        ax.bar_label(ax.containers[0], label_type='edge')
        ax.tick_params(axis='x', rotation=1)
        plt.show()

        # Here comes the code for the descriptive output
        print("\n")
        print("---------------------------------------------------------------------------------"
              "\nSummary trigger question 4 \n")
        print("After analyzing the amount of sold products per market we can conclude the following:")

        # Code for descriptive output
        amount_sold = self.df["Product Amount"]
        profit_total = np.sum(amount_sold)

        # Some further work to display ranking in the console
        sold_amount_array = np.array([])

        # Created an array that hold all markets
        market_array = self.df['Market'].unique()

        for market in market_array:
            products_sold_per_market = self.df.groupby("Market").get_group(market)["Product Amount"].sum()
            sold_amount_array = np.append(sold_amount_array, products_sold_per_market)

        # Now we sort the array from biggest to lowest
        sorted_amount_sold = np.sort(sold_amount_array)[::-1]

        # A nested loop is created to match the sorted profits with the correct market
        i = 0
        for amount in sorted_amount_sold:
            for market in market_array:
                if amount == self.df.groupby("Market").get_group(market)["Product Amount"].sum():
                    print("Rank " + str(i + 1) + " --> In market '" + market + "' " + str(amount) +
                          " products were sold")
                    i += 1

        print("The difference between the best and worst selling market is " + str(np.max(sorted_amount_sold) - np.min(
            sorted_amount_sold)) + " products!")
        print("Since this is a rather huge span between the max and min value the standard deviation is:")
        print("Std --> " + str(np.std(sorted_amount_sold)))
        print("On the other hand the mean of the amount of products sold equals: ")
        print("Mean --> " + str(np.mean(sorted_amount_sold)))
        print("Consequently, the amount of sold products per market have a significant spread or "
              "variability from the mean!")


start = Evidence()