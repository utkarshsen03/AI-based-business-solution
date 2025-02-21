import streamlit as st
from  class_apriori import Apriori
from visualization import  Visualization

st.header("AI-Based Businness Assistant")

with st.sidebar:
    sales_file = st.file_uploader("Upload Sales File:")
    expense_file = st.file_uploader("Upload Expense File:")
    
if sales_file is not None and expense_file is not None:
    visuals = Visualization(sales_file,expense_file)
    apriori = Apriori(sales_file)
    
    visuals.data_cleaning()
    visuals.data_preprocessing()
    visuals.products_dataframe()
    
    options = st.multiselect("Select graph for visuals:",["Top Products","Monthly Quantity Sold",
                                                          "Week day-wise analysis of Quantity Sold","Monthly Sales","Week days-wise Sales analysis",
                                                          "Most Sold Categories","Top 10 Customers","Distribution of Payment Methods","Daily Sales Fluctuations",
                                                          "Expenses","Monthly Expenses","Profit"])
    
    unique_customers, unique_products, total_revenue, average_sales, total_expense = visuals.descriptive_statistics()
    col1, col2, col3 = st.columns(3)
    
    col1.write(f"**Total Customer: {unique_customers}**")
    col2.write(f"**Total Products: {unique_products}**")
    col3.write(f"**Total Revenue Generated: {total_revenue}**")
    col1.write(f"**Average Sales: {average_sales}**")
    col2.write(f"**Total Expenses: {total_expense}**")
    
    frequent_itemset = apriori.apply_apriori()
    st.write(frequent_itemset)

    
    
    for field in options:
        if field == "Top Products":
            st.subheader("Top Products Sold")
            products, fig = visuals.top_products()
            
            st.plotly_chart(fig)
            
            st.write(f"Most Sold product is **{products.index[0]}**. with **{products[0]}** quantities sold.")
            st.write(f"Least Sold Product is **{products.index[-1]}** with **{products[-1]}** quantities sold.")
                
        if field == "Monthly Quantity Sold":
            st.subheader("Quantities Sold per Month")
            monthly_quantity_sale, fig = visuals.monthly_quantity_sale()
            
            st.plotly_chart(fig)
            
            st.write(f"**{monthly_quantity_sale.index[0]}** was by far the busiest month with **{monthly_quantity_sale[0]}** quantities sold.")
            st.write(f"**{monthly_quantity_sale.index[-1]}** experienced the least sale with only **{monthly_quantity_sale[-1]}** quantities sold.")
            
        if field == "Week day-wise analysis of Quantity Sold":
            st.subheader("Quantities Sold On Days of the Week")
            weekly_quantity_sold,fig = visuals.weekly_quantity_sale()
            
            st.plotly_chart(fig)
            
            st.write(f"On an average, the customer buys more product on **{weekly_quantity_sold.index[0]}**")
            st.write(f"The sale is comparitively low on **{weekly_quantity_sold.index[-1]}**.")
            
        if field == "Monthly Sales":
            st.subheader("Sales per Month")
            monthly_sales, fig = visuals.monthly_sale_amount()
            
            st.plotly_chart(fig)
            
            st.write(f"**{monthly_sales.index[0]}** experienced the highest amount of sales and **{monthly_sales.index[-1]}** the least amoount.")
            
        if field == "Week days-wise Sales analysis":
            st.subheader("Average Amount received on Days of the Week")
            weekly_sales, fig = visuals.weekly_sale_amount()
            
            st.plotly_chart(fig)
            
            st.write(f"On an average **{weekly_sales.index[0]}** experienced the highest amount of sales and **{weekly_sales.index[-1]}** the least amoount.")
            
        if field == "Most Sold Categories":
            st.subheader("Categories Sold Distribution")
            category_sold, fig = visuals.categorical_sale()
            
            st.plotly_chart(fig)
            
            st.write(f"The most popular Category was **{category_sold.index[0]}**.")
            st.write(f"Not many people bought products from **{category_sold.index[-1]}** category.")
            
        if field == "Top 10 Customers":
            st.subheader("Top 10 Customers Based on Amount Spend")
            customers, fig = visuals.customer_sale()
            
            st.plotly_chart(fig)
            
            st.write(f"**{customers.index[0]}** spend the highest amount.")
            
        if field == "Distribution of Payment Methods":
            st.subheader("Payment Methods Used")
            payment, fig = visuals.payment_method()
            
            st.plotly_chart(fig)
            
            st.write(f"Different payment methods used are: {list(payment['Payment_Mode'].unique())}")
            
        if field == "Daily Sales Fluctuations":
            st.subheader("Daily Sales Fluctuations")
            fig = visuals.daily_sale()
            st.plotly_chart(fig)
            
        if field == "Expenses":
            st.subheader("Expenses")
            expenses, fig = visuals.expenses()
            st.plotly_chart(fig)
            
        if field == "Monthly Expenses":
            st.subheader("Amount Spend per Month")
            monthly_expenses, fig = visuals.monthly_expenses()
            
            st.plotly_chart(fig)
            
            monthly_expenses.sort_values("Total_Expense",inplace=True,ascending=False)
            st.write(f"The most expensive month was **{monthly_expenses['Month'].iloc[0]}** with an expense of **{monthly_expenses['Total_Expense'].iloc[0]}**.")
            
        if field == "Profit":
            st.subheader("Monthly Profit Earned")
            profit, fig = visuals.profit_analysis()
            
            st.plotly_chart(fig)
            
            profit.sort_values('Profit',inplace=True,ascending=False)
            st.write(f"**{profit['Month'].iloc[0]}** was the most profitable month with profit of **{round(profit['Profit'].iloc[0],2)}%**.")
            st.write(f"**{profit['Month'].iloc[-1]}** was the least profitable month.**{round(profit['Profit'].iloc[-1],2)}%**")
            
            
        