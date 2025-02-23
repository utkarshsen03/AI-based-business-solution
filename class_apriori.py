import pandas as pd
import plotly.express as px
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import seaborn as sns

class Apriori:

    def __init__(self, filepath):
        self.df = pd.read_excel(filepath)
    
    def apply_apriori(self):
        product_list = list(self.df['Product_Names'].map(lambda x:x.lstrip('[').rstrip(']').strip().split(',')))
        te = TransactionEncoder()
        te_ary = te.fit(product_list).transform(product_list)
        product_df = pd.DataFrame(te_ary, columns=te.columns_)
        
        #Applying model
        self.frequent_itemsets = apriori(product_df, min_support=0.3, use_colnames=True)
        
        #Adding a length column to the dataframe
        self.frequent_itemsets['length'] = self.frequent_itemsets['itemsets'].apply(lambda x:len(x))
        
        #Displaying results arranged in descending order based on support
        self.frequent_itemsets.sort_values('support', ascending=False)
        
        return self.frequent_itemsets
        
    def generate_rules(self):
        self.df_ar = association_rules(self.frequent_itemsets, metric = "confidence", min_threshold = 0.5)
        self.df_ar.sort_values(by='confidence',ascending=False,inplace=True)
        temp_df = self.df_ar[(self.df_ar.support > 0.3) & (self.df_ar.confidence > 0.3)].sort_values("confidence", ascending = False)
        return temp_df
        
    def heatmap(self):
        apriori_rules = self.df_ar.copy()
        apriori_rules['lhs_items'] = apriori_rules['antecedents'].apply(lambda x:len(x) )
        apriori_rules[apriori_rules['lhs_items']>1].sort_values('lift', ascending=False).head()
        apriori_rules['antecedents_'] = apriori_rules['antecedents'].apply(lambda a: ','.join(list(a)))
        apriori_rules['consequents_'] = apriori_rules['consequents'].apply(lambda a: ','.join(list(a)))
        pivot = apriori_rules[(apriori_rules['support']>0.1)].pivot(index = 'antecedents_', columns = 'consequents_', values= 'confidence')
        
        fig = px.imshow(pivot,text_auto=True)
        
        return fig