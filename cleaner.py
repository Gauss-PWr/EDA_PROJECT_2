import pandas as pd
import os
import matplotlib

numerics = [
    'Age' , 'Annual_Income' , 'Changed_Credit_Limit', 'Monthly_Balance', 
    'Num_of_Delayed_Payment', 'Amount_invested_monthly', 'Num_of_Loan',
    'Outstanding_Debt' 
]

def splitter(string, idx):
    if isinstance(string, str):
        split = string.split()
        result = split[idx]
    else:
        result = string
    return result

def cleaning(df):
    for column in df.columns.tolist():
        df[column] = df[column].apply(lambda x: x.strip('_') if isinstance(x, str) else x)

    df['Monthly_Balance'] = df['Monthly_Balance'].apply(lambda x: x.strip() if isinstance(x, str) else x)

    df['Payment_Behaviour'] = df['Payment_Behaviour'].apply(
        lambda x: 'High_spent_Small_value_payments' if x == '!@9#%8' else x
    )

    df['Occupation'] = df['Occupation'].fillna('N/A')
    df['Occupation'] = df['Occupation'].apply(lambda x: 'N/A' if x == '' else x)
    df['Type_of_Loan'] = df['Type_of_Loan'].fillna('Not Specified')
    df['Credit_Mix'] = df['Credit_Mix'].apply(lambda x: 'N/A' if x == '' else x)

    df['Credit_History_Age_Year'] = df['Credit_History_Age'].apply(lambda x: splitter(x, 0))
    df['Credit_History_Age_Year'] = pd.to_numeric(df['Credit_History_Age_Year'], errors='coerce')
    df['Credit_History_Age_Month'] = df['Credit_History_Age'].apply(lambda x: splitter(x, 3))
    df['Credit_History_Age_Month'] = pd.to_numeric(df['Credit_History_Age_Month'], errors='coerce')
    df['Credit_History_Age_Month'] = df['Credit_History_Age_Month'].apply(lambda x: x/12)
    df['Credit_History_Age_Numeric'] = df['Credit_History_Age_Month'] + df['Credit_History_Age_Year']
    df['Credit_History_Age'] = df['Credit_History_Age_Numeric']

    df = df.drop(['Credit_History_Age_Numeric', 'Credit_History_Age_Month', 'Credit_History_Age_Year'], axis='columns')

    for column in numerics:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    return df