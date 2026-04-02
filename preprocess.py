import pandas as pd

df = pd.read_csv("marketing_campaign.csv", sep = '\t')

customer = df[['ID', 'Education', 'Marital_Status', 'Year_Birth', 'Dt_Customer', 'Income', 'Kidhome', 'Teenhome', 'Recency', 'Complain', 'AcceptedCmp1', 'AcceptedCmp2']]
customer.columns = ['CustomerID', 'EducationCode', 'MaritalStatusCode', 'Year_Birth', 'Dt_Customer', 'Income', 'Kidhome', 'Teenhome', 'Recency', 'ComplainFlag', 'AcceptedCmp1', 'AcceptedCmp2']
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], dayfirst=True)
df['Dt_Customer'] = df['Dt_Customer'].dt.strftime('%d-%b-%Y').str.upper()

customer.to_csv("customer.csv", index = False)

profile = df[['ID', 'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth']]
profile.columns = ['CustomerID', 'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth']

profile.to_csv("profile_customer.csv", index = False)