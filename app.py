import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv('bank_data.csv')  # Replace with your filename

# Preprocessing
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)

df['previous_contact'] = df['pdays'].apply(lambda x: 0 if x == 999 else 1)
month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

# App Title
st.title("Bank Marketing Campaign Analysis")

# Sidebar Navigation
section = st.sidebar.radio("Go to", [
    "Data Overview",
    "Exploratory Data Analysis",
    "Client Profile",
    "Campaign Effectiveness",
    "Previous Campaign Impact",
    "Temporal Analysis"
])

# 1. Data Overview
if section == "Data Overview":
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    st.subheader("Data Types")
    st.write(df.dtypes)

# 2. EDA
elif section == "Exploratory Data Analysis":
    st.subheader("Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['age'], bins=30, kde=True, ax=ax, color='#3498db')
    st.pyplot(fig)

    for col in ['job', 'marital', 'education']:
        st.subheader(f"{col.capitalize()} Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x=col, order=df[col].value_counts().index, ax=ax, palette='pastel')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.subheader("Subscription by Job and Education")
    sub_rate = df[df['y'] == 1].groupby(['job', 'education']).size().unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(12,6))
    sub_rate.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    st.pyplot(fig)

    st.subheader("Correlation (Numerical Features)")
    corr = df.select_dtypes(include=np.number).corr()
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# 3. Client Profile
elif section == "Client Profile":
    st.subheader("Subscription Rate by Category")
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e']
    for i, col in enumerate(['job', 'marital', 'education']):
        fig, ax = plt.subplots(figsize=(10,4))
        sns.barplot(x=col, y='y', data=df, ax=ax, color=colors[i])
        plt.xticks(rotation=45)
        st.pyplot(fig)

# 4. Campaign Effectiveness
elif section == "Campaign Effectiveness":
    st.subheader("Duration vs Subscription")
    Q1 = df['duration'].quantile(0.25)
    Q3 = df['duration'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df_no_out = df[(df['duration'] >= lower) & (df['duration'] <= upper)]
    fig, ax = plt.subplots()
    sns.boxplot(x='y', y='duration', data=df_no_out, ax=ax, showfliers=False, palette='Set2')
    st.pyplot(fig)

    st.subheader("Contact Method vs Subscription")
    fig, ax = plt.subplots()
    sns.countplot(x='contact', hue='y', data=df, ax=ax, palette=['#1f77b4', '#ff7f0e'])
    st.pyplot(fig)

    st.subheader("Avg Contacts vs Subscription")
    fig, ax = plt.subplots()
    sns.barplot(x='y', y='campaign', data=df, ax=ax, palette='pastel', estimator='mean', ci=None)
    st.pyplot(fig)

# 5. Previous Campaign Impact
elif section == "Previous Campaign Impact":
    st.subheader("Previous Campaign Outcome vs Subscription")
    fig, ax = plt.subplots()
    sns.countplot(x='poutcome', hue='y', data=df, ax=ax, palette=['#2ca02c', '#d62728'])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Prior Contact vs Subscription Rate")
    fig, ax = plt.subplots()
    sns.barplot(x='previous_contact', y='y', data=df, ax=ax, palette='Set1')
    ax.set_xticklabels(['No', 'Yes'])
    st.pyplot(fig)

# 6. Temporal Analysis
elif section == "Temporal Analysis":
    st.subheader("Monthly Subscriptions")
    fig, ax = plt.subplots()
    sns.countplot(x='month', hue='y', data=df, order=month_order, ax=ax, palette=['#1f77b4', '#ff7f0e'])
    st.pyplot(fig)

    st.subheader("Day of Week Subscriptions")
    fig, ax = plt.subplots()
    sns.countplot(x='day_of_week', hue='y', data=df, 
                  order=['mon','tue','wed','thu','fri'], ax=ax, palette='Set2')
    st.pyplot(fig)
