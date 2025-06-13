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
    fig, ax = plt.subplots()
    sns.histplot(df['age'], bins=30, kde=True, color='teal', ax=ax)
    ax.set_title("Age Distribution")
    st.pyplot(fig)

elif query == "Subscription by Job":
    st.subheader("Subscription Rate by Job")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x='job', y='y', data=df, palette='viridis', ax=ax)
    ax.set_title("Subscription Rate by Job")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif query == "Subscription by Education":
    st.subheader("Subscription Rate by Education")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x='education', y='y', data=df, palette='magma', ax=ax)
    ax.set_title("Subscription Rate by Education")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif query == "Effect of Contact Method":
    st.subheader("Contact Method vs Subscription")
    fig, ax = plt.subplots()
    sns.countplot(x='contact', hue='y', data=df, palette='Set2', ax=ax)
    ax.set_title("Contact Method vs Subscription")
    st.pyplot(fig)

elif query == "Duration vs Subscription":
    st.subheader("Call Duration vs Subscription")
    df['duration_cleaned'] = df['duration'].clip(upper=df['duration'].quantile(0.95))  # Remove extreme outliers
    fig, ax = plt.subplots()
    sns.violinplot(x='y', y='duration_cleaned', data=df, palette='coolwarm', ax=ax)
    ax.set_title("Call Duration vs Subscription")
    st.pyplot(fig)

elif query == "Campaign Count vs Subscription":
    st.subheader("Number of Contacts vs Subscription")
    fig, ax = plt.subplots()
    sns.violinplot(x='y', y='campaign', data=df, palette='cubehelix', ax=ax)
    ax.set_title("Number of Contacts vs Subscription")
    st.pyplot(fig)

elif query == "Previous Campaign Outcome":
    st.subheader("Previous Campaign Outcome vs Subscription")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.countplot(x='poutcome', hue='y', data=df, palette='husl', ax=ax)
    ax.set_title("Previous Campaign Outcome vs Subscription")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif query == "Subscription by Month":
    st.subheader("Month-wise Subscription Trends")
    month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    fig, ax = plt.subplots()
    sns.countplot(x='month', hue='y', data=df, order=month_order, palette='Paired', ax=ax)
    ax.set_title("Subscription by Month")
    st.pyplot(fig)

elif query == "Correlation Analysis":
    st.subheader("Correlation of Numerical Features")
    corr = df.select_dtypes(include='number').corr()
    st.dataframe(corr.style.background_gradient(cmap='coolwarm').format("{:.2f}"))
