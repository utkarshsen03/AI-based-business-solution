import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

class Visualization:
    def __init__(self,sale_filepath,expense_filepath):
        self.sales_df = pd.read_excel(sale_filepath,index_col=None)
        self.expense_df = pd.read_excel(expense_filepath,index_col=0)
        
    def data_cleaning(self):
        self.sales_df.dropna(inplace=True)
        
        self.sales_df['Date_Time']=pd.to_datetime(self.sales_df['Date_Time'])
        
        self.sales_df['Month'] = self.sales_df['Date_Time'].dt.month_name()
        self.sales_df['Day'] = self.sales_df['Date_Time'].dt.day_name()
        
        self.sales_df.drop(columns=["Invoice_ID"],inplace=True)
        
    def data_preprocessing(self):
        self.sales_df['Month']=self.sales_df['Date_Time'].dt.month_name()
        self.sales_df['Day'] = self.sales_df['Date_Time'].dt.day_name()
        
        self.sales_df['Paid_Amount'] = self.sales_df['Total_Sale_Amount']-self.sales_df['Discount_Applied']
        
        self.sales_df['Payment_Mode'] = self.sales_df['Payment_Mode'].astype('category')
        self.sales_df['Categories'] = self.sales_df['Categories'].astype('category')
    
        self.sales_df['Product_Names'].str.strip()
    
    def products_dataframe(self):                        
        self.products = self.sales_df[['Customer_ID', 'Product_IDs', 'Product_Names', 'Categories',
                         'Quantities_Sold', 'Unit_Prices', 'Month', 'Day', 'Payment_Mode']].copy()

        columns_to_explode = ['Product_IDs', 'Product_Names', 'Categories', 'Quantities_Sold', 'Unit_Prices']
        self.products[columns_to_explode] = self.products[columns_to_explode].astype(str).apply(lambda x: x.str.split(','))

        self.products = self.products.explode(columns_to_explode)
    
        
        self.products['Product_Names'] = self.products['Product_Names'].str.strip()
        self.products['Categories'] = self.products['Categories'].str.strip()
        
        self.products['Quantities_Sold'] = pd.to_numeric(self.products['Quantities_Sold'], errors='coerce')
        self.products['Unit_Prices'] = pd.to_numeric(self.products['Unit_Prices'], errors='coerce')

        self.products['Total_Price'] = self.products['Quantities_Sold'] * self.products['Unit_Prices']

    def descriptive_statistics(self):
        unique_customers = self.sales_df['Customer_ID'].nunique()
        unique_products = self.products["Product_Names"].nunique()
        total_revenue = self.sales_df['Total_Sale_Amount'].sum()
        average_sales = self.sales_df["Total_Sale_Amount"].mean()
        
        total_expense = self.expense_df.sum().sum()
        
        return unique_customers, unique_products, total_revenue, average_sales, total_expense
        
    def top_products(self):
        top_products = self.products.groupby('Product_Names')['Quantities_Sold'].sum().sort_values(ascending=False)
        fig = px.bar(top_products,x=top_products.index,y='Quantities_Sold',log_y =True,title = "Top Products")
        
        return top_products, fig
        
    def monthly_quantity_sale(self):
        month_sale = self.products.groupby('Month')['Quantities_Sold'].sum().sort_values(ascending=False)
        fig = px.bar(month_sale,x=month_sale.index,y='Quantities_Sold',log_y =True)
        
        return month_sale, fig
    
    def weekly_quantity_sale(self):
        week_sale = self.products.groupby('Day')['Quantities_Sold'].sum().sort_values(ascending=False)
        fig = px.bar(week_sale,x=week_sale.index,y='Quantities_Sold',log_y =True,title="Daily Quantity Sold")
        
        return week_sale, fig
    
    def monthly_sale_amount(self):
        month_sale = self.products.groupby('Month')['Total_Sale_Amount'].sum().sort_values(ascending=False)
        fig = px.bar(month_sale,x=month_sale.index,y='Total_Sale_Amount',log_y =True, title= "Monthly Sales")
        
        return month_sale, fig
    
    def weekly_sale_amount(self):
        week_sale = self.products.groupby('Day')['Total_Sale_Amount'].sum().sort_values(ascending=False)
        fig = px.bar(week_sale,x=week_sale.index,y='Total_Sale_Amount',log_y =True,title="Daily Sales")
        
        return week_sale, fig
    
    def categorical_sale(self):
        sales_cat = self.products.groupby('Categories')['Total_Price'].mean().sort_values(ascending=False)
        fig = px.pie(sales_cat,names=sales_cat.index,values='Total_Price',title='Total Sales by Category',hole=0.5)
        
        return sales_cat, fig
    
    def customer_sale(self):
        high_spenders = self.products.groupby('Customer_ID')['Total_Price'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(high_spenders,x=high_spenders.index, y=high_spenders.values, log_y =True,title='Top 10 Spenders')
        fig.update_layout(xaxis_title="Customers", yaxis_title="Total Amount Spent")
        
        return high_spenders, fig
        
    def payment_method(self):
        payment_analysis = self.sales_df.groupby('Payment_Mode')['Total_Sale_Amount'].sum().sort_values(ascending=False).reset_index()
        fig = px.pie(payment_analysis, names='Payment_Mode', values='Total_Sale_Amount', 
                     title='Percentage of Total Sales by Payment Mode',hole=0.4)
    
        return payment_analysis, fig

    
    def daily_sale(self):
        new_df = self.df.sort_values("Date_Time")
        fig = px.line(new_df,x="Date_Time",y="Paid_Amount",title="Daily Sales Plot")
        return fig
    
    def expenses(self):
        total_expense = self.expense_data.sum()
        fig = px.bar(x=total_expense.index, y=total_expense.values)
        
        return total_expense, fig
    
    def  monthly_expenses(self):
        monthly_expense = self.expense_data.sum(axis=1).reset_index()
        monthly_expense.columns = ["Month","Total_Expense"]
        fig = px.bar(monthly_expense, x=monthly_expense['Month'], y=monthly_expense['Total_Expense'])
        
        return monthly_expense, fig
    
    def profit_analysis(self):
        monthly_expense = self.expense_data.sum(axis=1).reset_index()
        monthly_expense.columns = ["Month","Total_Expense"]
        
        monthly_sale = self.df.groupby("Month")['Paid_Amount'].agg('sum').reset_index()
        
        temp_df = pd.merge(monthly_sale,monthly_expense,on="Month")
        
        temp_df['Profit'] = (temp_df["Paid_Amount"] - temp_df["Total_Expense"])/temp_df["Paid_Amount"] * 100
        
        fig = px.bar(temp_df, x=temp_df['Month'], y=temp_df['Profit'])
        
        return temp_df,fig
    
# if __name__ == '__main__':
#     sales_df = Visualization('sales_dataset.xlsx')
#     sales_df.data_cleaning()
#     sales_df.data_preprocessing()
#     foo = sales_df.products_dataframe()
#     top_products = sales_df.top_products()
#     monthly_sale = sales_df.monthly_sale()
#     weekly_sale = sales_df.weekly_sale()
    
#     top_products.show()
#     monthly_sale.show()
#     weekly_sale.show()