import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

class Apriori:

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_excel(filepath)
    
    def preprocess_data(self):
        transactions = []
        for _, row in self.df.iterrows():
            products = row['Product_Names'].split(', ')
            quantities = list(map(int, row['Quantities_Sold'].split(', ')))
            for product, quantity in zip(products, quantities):
                if quantity > 0:
                    transactions.append((row['Invoice_ID'], product, quantity))
        transaction_df = pd.DataFrame(transactions, columns=['Invoice_ID', 'Item', 'Quantity'])
        basket = transaction_df.pivot_table(index='Invoice_ID', columns='Item', values='Quantity', fill_value=0)
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)
        self.basket = basket
        return basket
    
    def apply_apriori(self, min_support=0.05):
        frequent_itemsets = apriori(self.basket, min_support=min_support, use_colnames=True)
        self.frequent_itemsets = frequent_itemsets
        return frequent_itemsets
    
    def generate_rules(self, metric='lift', min_threshold=1.0):
        rules = association_rules(self.frequent_itemsets, metric=metric, min_threshold=min_threshold)
        return rules

if __name__=="__main__": 
    
    foo = Apriori(filepath=r"C:\Users\RAJ\Desktop\sales_dataset.xlsx")
    foo1=foo.preprocess_data()
    foo2=foo.apply_apriori()
    foo3=foo.generate_rules()
    print("Complete")