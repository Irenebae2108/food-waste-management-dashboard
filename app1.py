# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 19:05:27 2026

@author: Msi
"""

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="Food Waste Management Dashboard",
    page_icon="🍲",
    layout="wide"
)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pihuri21",
    database="food_waste"
)

query = """
SELECT

c.Claim_ID,
c.Status,
c.Timestamp,

f.Food_ID,
f.Food_Name,
f.Quantity,
f.Expiry_Date,
f.Food_Type,
f.Meal_Type,

p.Provider_ID,
p.Name AS Provider_Name,
p.Type AS Provider_Type,
p.City AS Provider_City,
p.Contact AS Provider_Contact,

r.Receiver_ID,
r.Name AS Receiver_Name,
r.Type AS Receiver_Type,
r.City AS Receiver_City,
r.Contact AS Receiver_Contact

FROM claims_data c

JOIN food_listings_data f
ON c.Food_ID=f.Food_ID

JOIN providers_data p
ON f.Provider_ID=p.Provider_ID

JOIN receivers_data r
ON c.Receiver_ID=r.Receiver_ID
"""

df = pd.read_sql(query, conn)

conn.close()

st.title("🍲 Food Waste Management Dashboard")

st.dataframe(df.head())

st.sidebar.header("🔍 Filters")

# Provider City
city = st.sidebar.multiselect(
    "Select Provider City",
    options=sorted(df["Provider_City"].unique()),
    default=sorted(df["Provider_City"].unique())
)

# Provider Type
provider_type = st.sidebar.multiselect(
    "Provider Type",
    options=sorted(df["Provider_Type"].unique()),
    default=sorted(df["Provider_Type"].unique())
)

# Food Type
food_type = st.sidebar.multiselect(
    "Food Type",
    options=sorted(df["Food_Type"].unique()),
    default=sorted(df["Food_Type"].unique())
)

# Meal Type
meal_type = st.sidebar.multiselect(
    "Meal Type",
    options=sorted(df["Meal_Type"].unique()),
    default=sorted(df["Meal_Type"].unique())
)

# Claim Status
status = st.sidebar.multiselect(
    "Claim Status",
    options=sorted(df["Status"].unique()),
    default=sorted(df["Status"].unique())
)

filtered_df = df[
    (df["Provider_City"].isin(city)) &
    (df["Provider_Type"].isin(provider_type)) &
    (df["Food_Type"].isin(food_type)) &
    (df["Meal_Type"].isin(meal_type)) &
    (df["Status"].isin(status))
]

st.title("🍲 Food Waste Management Dashboard")
st.markdown("### Food Donation & Distribution Analytics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🏢 Providers",
        filtered_df["Provider_ID"].nunique()
    )

with col2:
    st.metric(
        "🤝 Receivers",
        filtered_df["Receiver_ID"].nunique()
    )

with col3:
    st.metric(
        "🍱 Food Listings",
        filtered_df["Food_ID"].nunique()
    )

with col4:
    st.metric(
        "📦 Total Quantity",
        int(filtered_df["Quantity"].sum())
    )

with col5:
    st.metric(
        "📋 Claims",
        filtered_df["Claim_ID"].nunique()
    )
    
st.markdown("---")

st.subheader("📊 Providers & Receivers by City")

city_data = filtered_df.groupby("Provider_City").agg(
    Providers=("Provider_ID", "nunique"),
    Receivers=("Receiver_ID", "nunique")
).reset_index()

fig = px.bar(
    city_data,
    x="Provider_City",
    y=["Providers", "Receivers"],
    barmode="group",
    title="Providers & Receivers by City",
    labels={"value":"Count","Provider_City":"City"}
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🍽️ Food Contribution by Provider Type")

provider_data = filtered_df.groupby("Provider_Type")["Quantity"].sum().reset_index()

fig = px.pie(
    provider_data,
    names="Provider_Type",
    values="Quantity",
    hole=0.45,
    title="Food Quantity Donated by Provider Type"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏙️ Food Listings by City")

listing_data = filtered_df.groupby("Provider_City")["Food_ID"].count().reset_index()

fig = px.bar(
    listing_data,
    x="Provider_City",
    y="Food_ID",
    color="Food_ID",
    title="Food Listings Available in Each City",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🥗 Most Common Food Types")

food_type_data = (
    filtered_df.groupby("Food_Type")
    .size()
    .reset_index(name="Count")
)

fig = px.pie(
    food_type_data,
    names="Food_Type",
    values="Count",
    title="Food Type Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🍽️ Meal Type Distribution")

meal_data = (
    filtered_df.groupby("Meal_Type")
    .size()
    .reset_index(name="Claims")
)

fig = px.bar(
    meal_data,
    x="Meal_Type",
    y="Claims",
    color="Meal_Type",
    text_auto=True,
    title="Claims by Meal Type"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Claim Status")

status_data = (
    filtered_df.groupby("Status")
    .size()
    .reset_index(name="Count")
)

fig = px.pie(
    status_data,
    names="Status",
    values="Count",
    hole=0.5,
    title="Claim Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top Providers by Quantity Donated")

provider_quantity = (
    filtered_df.groupby("Provider_Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    provider_quantity,
    x="Provider_Name",
    y="Quantity",
    color="Quantity",
    text_auto=True,
    title="Top 10 Providers"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📞 Provider Contact Information")

selected_city = st.selectbox(
    "Choose Provider City",
    sorted(filtered_df["Provider_City"].unique())
)

provider_contacts = filtered_df[
    filtered_df["Provider_City"] == selected_city
][["Provider_Name", "Provider_Contact"]].drop_duplicates()

st.dataframe(provider_contacts, use_container_width=True)

st.subheader("📋 Complete Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)