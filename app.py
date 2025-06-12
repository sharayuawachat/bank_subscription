import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your fixed dataset
df = pd.read_csv("Bank.csv")

st.title("📊 Bank Marketing Campaign Insights")
st.markdown("Ask a question or choose a topic below to explore insights.")

# Option 1: Use selectbox to guide analysis
query = st.selectbox("Choose an analysis:", [
    "Age Distribution",
    "Subscription by Job",
    "Subscription by Education",
    "Effect of Contact Method",
    "Duration vs Subscription",
    "Campaign Count vs Subscription",
    "Previous Campaign Outcome",
    "Subscription by Month",
    "Correlation Analysis"
])

# Conditional rendering based on user query
if query == "Age Distribution":
    st.subheader("Age Distribution")
    sns.histplot(df['age'], bins=30, kde=True, color='teal')
    st.pyplot()

elif query == "Subscription by Job":
    st.subheader("Subscription Rate by Job")
    sns.barplot(x='job', y='y', data=df, palette='viridis')
    plt.xticks(rotation=45)
    st.pyplot()

elif query == "Subscription by Education":
    st.subheader("Subscription Rate by Education")
    sns.barplot(x='education', y='y', data=df, palette='magma')
    plt.xticks(rotation=45)
    st.pyplot()

elif query == "Effect of Contact Method":
    st.subheader("Contact Method vs Subscription")
    sns.countplot(x='contact', hue='y', data=df, palette='Set2')
    st.pyplot()

elif query == "Duration vs Subscription":
    st.subheader("Call Duration vs Subscription")
    df['duration_cleaned'] = df['duration'].clip(upper=df['duration'].quantile(0.95))  # Remove extreme outliers
    sns.violinplot(x='y', y='duration_cleaned', data=df, palette='coolwarm')
    st.pyplot()

elif query == "Campaign Count vs Subscription":
    st.subheader("Number of Contacts vs Subscription")
    sns.violinplot(x='y', y='campaign', data=df, palette='cubehelix')
    st.pyplot()

elif query == "Previous Campaign Outcome":
    st.subheader("Previous Campaign Outcome vs Subscription")
    sns.countplot(x='poutcome', hue='y', data=df, palette='husl')
    plt.xticks(rotation=45)
    st.pyplot()

elif query == "Subscription by Month":
    st.subheader("Month-wise Subscription Trends")
    month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    sns.countplot(x='month', hue='y', data=df, order=month_order, palette='Paired')
    st.pyplot()

elif query == "Correlation Analysis":
    st.subheader("Correlation of Numerical Features")
    corr = df.select_dtypes(include='number').corr()
    st.dataframe(corr.style.background_gradient(cmap='coolwarm').set_precision(2))
