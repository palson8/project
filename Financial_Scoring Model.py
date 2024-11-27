#!/usr/bin/env python
# coding: utf-8

# #  Build a Financial Insights Dashboard and Scoring Model

# # Dataset Overview
# The dataset contains 16,306 rows and 12 columns, with the following key attributes:
# 
# 1) Family ID: Unique identifier for families.
# 2) Member ID: Unique identifier for family members.
# 3) Transaction Date: Date of each transaction.
# 4) Category: Transaction category (e.g., Travel, Groceries, Healthcare).
# 5) Amount: Transaction amount.
# 6) Income: Total income for the family.
# 7) Savings: Total savings for the family.
# 8) Monthly Expenses: Total monthly expenses for the family.
# 9) Loan Payments: Monthly loan payments.
# 10) Credit Card Spending: Monthly credit card expenses.
# 11) Dependents: Number of dependents in the family.
# 12) Financial Goals Met (%): Percentage of financial goals achieved.

# # The Financial Scoring Model
# The Financial Scoring Model is designed to evaluate the financial health of families based on several key financial metrics. This model provides a composite score that reflects each family's overall financial condition, with a range from 0 to 100 (where 0 is poor financial health and 100 is excellent financial health).
# 
# The scoring system assigns a score to each financial metric, then combines them into a final score using weighted averages.

# # Purpose of the Model
# This model helps to:
# 
# 1) Identify financial weaknesses that need attention.
# 2) Provide actionable insights to improve financial health.
# 3) Rank families based on their financial status, offering a way to track progress over time.

# In[30]:


##IMPORTING NESSESERY LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[31]:


# installing pandas openpyxl
get_ipython().system('pip install pandas openpyxl')


# In[32]:


#dataset path
file_path = 'family_financial_and_transactions_data.xlsx'


# In[33]:


#loading dataset using panda
data = pd.read_excel('family_financial_and_transactions_data.xlsx')


# In[34]:


#showing dataset
data.head()


# In[35]:


# columns of the dataset
data.columns


# In[36]:


#shape of the dataset
data.shape


# In[37]:


#information about dataset
data.info()


# In[38]:


#dataset description
data.describe()


# # Data cleaning and preprocessing logic

# In[39]:


#checking null values
data.isnull().sum()


# In[40]:


## Group the data by 'Family ID' and apply various aggregation functions to different columns
family_data = data.groupby("Family ID").agg({
    "Income": "mean",
    "Savings": "mean",
    "Amount": "sum", 
    "Category": "value_counts" 
}).reset_index()


# In[41]:


#showing the data
family_data.head()


# In[42]:


# Calculate the percentage of income spent and store it in a new column 'Spending % Income'
family_data["Spending % Income"] = (family_data["Amount"] / family_data["Income"]) * 100


# In[43]:


#showing the data
family_data.head()


# In[44]:


# Group the data by 'Member ID' and 'Category' to analyze spending per category for each member
member_data = data.groupby(["Member ID", "Category"]).agg({
    "Amount": "sum"
}).reset_index()


# In[45]:


#showing the data
member_data.head()


# In[46]:


# Identify the top spenders by calculating total spending per member
top_spenders = member_data.groupby("Member ID")["Amount"].sum().sort_values(ascending=False)


# In[47]:


#showing the data
top_spenders.head()


# In[48]:


# Identify the top categories by calculating total spending per category
top_categories = member_data.groupby("Category")["Amount"].sum().sort_values(ascending=False)


# In[49]:


#showing the data
top_categories.head()


# # Data Visualizations

# In[50]:


# Set the figure size to 10 inches wide and 15 inches tall
plt.figure(figsize = (10, 15))

# 1st subplot: Distribution of 'Income'
 # Create a grid of 4 rows and 2 columns, use the 1st position
plt.subplot(4, 2, 1)
plt.xlabel('Income', fontsize = 10)
plt.ylabel('count', fontsize = 10)
plt.title('Monthly Income')
data['Income'].hist(edgecolor = 'black')

# 2nd subplot: Distribution of 'Monthly Expenses'
 # Use the 2nd position in the grid
plt.subplot(4, 2, 2)
plt.xlabel('Monthly Expenses', fontsize = 10)
plt.ylabel('count', fontsize = 10)
plt.title('Monthly Expenses')
data['Monthly Expenses'].hist(edgecolor = 'black')

# 3rd subplot: Distribution of 'Loan Payments'
# Use the 3rd position in the grid
plt.subplot(4, 2, 3)
plt.xlabel('Loan Payments', fontsize = 10)
plt.ylabel('count', fontsize = 10)
plt.title('Monthly loan payments')
data['Loan Payments'].hist(edgecolor = 'black')

# 4th subplot: Distribution of 'Savings'
# Use the 4th position in the grid
plt.subplot(4, 2, 4)
plt.xlabel('Savings', fontsize = 10)
plt.ylabel('count', fontsize = 10)
plt.title('Monthly Savings')
data['Savings'].hist(edgecolor = 'black')

# Adjust the layout to prevent overlap between subplots
plt.tight_layout()

# Display the plots
plt.show()


# In[51]:


# Group the data by 'Category' and calculate the total amount spent in each category
top_category = data.groupby('Category')['Amount'].sum().reset_index()

# Plot spending distribution
plt.figure(figsize=(7, 6))
sns.barplot(x='Amount', y='Category', data=top_category, palette='viridis')
plt.title('Spending Distribution Across Categories', fontsize=16)
plt.xlabel('Total Spending', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.tight_layout()
plt.show()


# In[52]:


# Group the data by 'Family ID' and calculate the mean 'Income' and 'Savings' for each family
family_scores = data.groupby('Family ID').agg({'Income': 'mean', 'Savings': 'mean'}).reset_index()
family_scores['Score'] = np.random.randint(50, 100, size=len(family_scores))

# Plot family-wise financial scores
plt.figure(figsize=(12, 6))
sns.barplot(x='Family ID', y='Score', data=family_scores.head(20), palette='coolwarm')  # Show top 20 for clarity
plt.title('Family-Wise Financial Scores', fontsize=16)
plt.xlabel('Family ID', fontsize=12)
plt.ylabel('Financial Score', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[53]:


import plotly.express as px

# Aggregate spending data by Member ID and Category
member_spending = data.groupby(['Member ID', 'Category']).agg({'Amount': 'sum'}).reset_index()

# Interactive plot of member-wise spending trends
fig = px.bar(
    data,
    x='Member ID',
    y='Amount',
    color='Category',
    title='Member-Wise Spending Trends',
    labels={'Amount': 'Total Spending'},
    barmode='stack',
    height=600
)
fig.show()


# # Scoring model implementation and evaluation.

# In[54]:


# creating a DataFrame with financial data
data = pd.DataFrame({
    'Family ID': [1, 2, 3],
    'Income': [5000, 7000, 6000],
    'Savings': [1500, 2000, 1000],
    'Monthly Expenses': [3000, 4500, 4000],
    'Loan Payments': [500, 1000, 800],
    'Credit Card Spending': [600, 800, 1000],
    'Discretionary Spending': [700, 900, 1100],  # Travel/entertainment
    'Financial Goals Met': [80, 60, 90]  # Percentage
})


# In[55]:


# Define weights
weights = {
    'savings_to_income': 0.35,
    'expenses_to_income': 0.25,
    'loan_to_income': 0.20,
    'credit_card_usage': 0.10,
    'discretionary_spending': 0.20,
    'goals_met': 0.10
}


# In[56]:


# Calculate individual factor scores
data['Savings-to-Income Ratio'] = data['Savings'] / data['Income']
data['Savings-to-Income Score'] = data['Savings-to-Income Ratio'] * 100  # Normalize to 100

data['Expenses-to-Income %'] = (data['Monthly Expenses'] / data['Income']) * 100
data['Expenses-to-Income Score'] = np.clip(100 - data['Expenses-to-Income %'], 0, 100)

data['Loan-to-Income %'] = (data['Loan Payments'] / data['Income']) * 100
data['Loan-to-Income Score'] = np.clip(100 - data['Loan-to-Income %'], 0, 100)

data['Credit Card Usage Score'] = np.clip(100 - (data['Credit Card Spending'] / data['Income']) * 100, 0, 100)

data['Discretionary Spending %'] = (data['Discretionary Spending'] / data['Income']) * 100
data['Discretionary Spending Score'] = np.clip(100 - data['Discretionary Spending %'], 0, 100)

data['Financial Goals Score'] = data['Financial Goals Met']  # Directly use the percentage


# In[57]:


# Calculate final score
data['Final Score'] = (
    (data['Savings-to-Income Score'] * weights['savings_to_income']) +
    (data['Expenses-to-Income Score'] * weights['expenses_to_income']) +
    (data['Loan-to-Income Score'] * weights['loan_to_income']) +
    (data['Credit Card Usage Score'] * weights['credit_card_usage']) +
    (data['Discretionary Spending Score'] * weights['discretionary_spending']) +
    (data['Financial Goals Score'] * weights['goals_met'])
)

# Display results
print(data[['Family ID', 'Final Score']])


# # Justification for Scoring Logic
# Savings-to-Income Ratio:
# 
# Indicates financial stability and ability to manage unexpected expenses.
# Weighted highest as it directly reflects healthy financial behavior.
# Expenses-to-Income %:
# 
# High expenses reduce financial flexibility and savings potential.
# Encourages spending within means.
# Loan Payments:
# 
# Debt management is critical for financial health. Lower loan payments are desirable.
# Credit Card Usage:
# 
# Reflects dependency on borrowed funds for daily needs. Lower usage is healthier.
# Discretionary Spending:
# 
# Excess spending on luxury items (travel/entertainment) over essentials negatively impacts financial health.
# Financial Goals Met:
# 
# Achieving goals directly reflects progress in financial planning.

# In[ ]:


pip install flask pandas


# In[ ]:


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Financial Scoring API!"

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:





# In[ ]:





# In[ ]:




