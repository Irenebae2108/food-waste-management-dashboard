# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Food Waste Management Dashboard",
    page_icon="🍲",
    layout="wide"
)

# ---------------------------------------------------
# Load CSV Files
# ---------------------------------------------------
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

# ---------------------------------------------------
# Rename Provider Columns
# ---------------------------------------------------
providers.rename(columns={
    "Name": "Provider_Name",
    "Type": "Provider_Type",
    "City": "Provider_City",
    "Contact": "Provider_Contact"
}, inplace=True)

# ---------------------------------------------------
# Rename Receiver Columns
# ---------------------------------------------------
receivers.rename(columns={
    "Name": "Receiver_Name",
    "Type": "Receiver_Type",
    "City": "Receiver_City",
    "Contact": "Receiver_Contact"
}, inplace=True)

# ---------------------------------------------------
# Merge Data
# ---------------------------------------------------
df = claims.merge(food, on="Food_ID", how="left")

df = df.merge(
    providers,
    on="Provider_ID",
    how="left"
)

df = df.merge(
    receivers,
    on="Receiver_ID",
    how="left"
)

# Convert dates
df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.title("🍲 Food Waste Management Dashboard")
st.markdown("### Food Donation & Distribution Analytics")

# Uncomment once to check the merged columns
# st.write(df.columns.tolist())

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("🔍 Dashboard Filters")

# Provider City
city = st.sidebar.multiselect(
    "Provider City",
    sorted(df["Provider_City"].dropna().unique()),
    default=sorted(df["Provider_City"].dropna().unique())
)

# Provider Type
provider_type = st.sidebar.multiselect(
    "Provider Type",
    sorted(df["Provider_Type"].dropna().unique()),
    default=sorted(df["Provider_Type"].dropna().unique())
)

# Food Type
food_type = st.sidebar.multiselect(
    "Food Type",
    sorted(df["Food_Type"].dropna().unique()),
    default=sorted(df["Food_Type"].dropna().unique())
)

# Meal Type
meal_type = st.sidebar.multiselect(
    "Meal Type",
    sorted(df["Meal_Type"].dropna().unique()),
    default=sorted(df["Meal_Type"].dropna().unique())
)

# Claim Status
status = st.sidebar.multiselect(
    "Claim Status",
    sorted(df["Status"].dropna().unique()),
    default=sorted(df["Status"].dropna().unique())
)

# ---------------------------------------------------
# Apply Filters
# ---------------------------------------------------
filtered_df = df[
    (df["Provider_City"].isin(city)) &
    (df["Provider_Type"].isin(provider_type)) &
    (df["Food_Type"].isin(food_type)) &
    (df["Meal_Type"].isin(meal_type)) &
    (df["Status"].isin(status))
]

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
st.markdown("---")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "🏢 Providers",
        filtered_df["Provider_ID"].nunique()
    )

with kpi2:
    st.metric(
        "🤝 Receivers",
        filtered_df["Receiver_ID"].nunique()
    )

with kpi3:
    st.metric(
        "🍱 Food Listings",
        filtered_df["Food_ID"].nunique()
    )

with kpi4:
    st.metric(
        "📦 Total Quantity",
        int(filtered_df["Quantity"].sum())
    )

with kpi5:
    st.metric(
        "📋 Total Claims",
        filtered_df["Claim_ID"].nunique()
    )

# ---------------------------------------------------
# Additional Statistics
# ---------------------------------------------------
c1, c2, c3 = st.columns(3)

completed = (filtered_df["Status"] == "Completed").sum()
pending = (filtered_df["Status"] == "Pending").sum()
cancelled = (filtered_df["Status"] == "Cancelled").sum()

with c1:
    st.success(f"✅ Completed Claims: {completed}")

with c2:
    st.warning(f"⏳ Pending Claims: {pending}")

with c3:
    st.error(f"❌ Cancelled Claims: {cancelled}")

st.markdown("---")

# ===================================================
# VISUALIZATIONS
# ===================================================

# ---------------------------------------------------
# Chart 1 : Providers & Receivers by City
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

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
        color_discrete_sequence=["#2E8B57", "#FF8C00"]
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 2 : Provider Type Contribution
# ---------------------------------------------------

with col2:

    provider_data = (
        filtered_df.groupby("Provider_Type")["Quantity"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        provider_data,
        names="Provider_Type",
        values="Quantity",
        hole=0.45,
        title="Food Contribution by Provider Type"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 3 : Food Listings by City
# ---------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    listing_data = (
        filtered_df.groupby("Provider_City")["Food_ID"]
        .count()
        .reset_index()
    )

    fig = px.bar(
        listing_data,
        x="Provider_City",
        y="Food_ID",
        color="Food_ID",
        title="Food Listings by City",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 4 : Food Type Distribution
# ---------------------------------------------------

with col4:

    food_type_data = (
        filtered_df.groupby("Food_Type")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        food_type_data,
        names="Food_Type",
        values="Count",
        hole=0.40,
        title="Food Type Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 5 : Meal Type Distribution
# ---------------------------------------------------

col5, col6 = st.columns(2)

with col5:

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
        title="Most Claimed Meal Types"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 6 : Claim Status Distribution
# ---------------------------------------------------

with col6:

    status_data = (
        filtered_df.groupby("Status")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        status_data,
        names="Status",
        values="Count",
        hole=0.50,
        title="Claim Status Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 7 : Top Providers
# ---------------------------------------------------

col7, col8 = st.columns(2)

with col7:

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
        title="Top 10 Providers by Quantity Donated"
    )

    fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Chart 8 : Top Receivers
# ---------------------------------------------------

with col8:

    receiver_quantity = (
        filtered_df.groupby("Receiver_Name")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        receiver_quantity,
        x="Receiver_Name",
        y="Quantity",
        color="Quantity",
        text_auto=True,
        title="Top 10 Receivers by Quantity Claimed"
    )

    fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(fig, use_container_width=True)

st.subheader("🍛 Most Claimed Food Items")

food_claim = (
    filtered_df.groupby("Food_Name")
    .size()
    .reset_index(name="Claims")
    .sort_values("Claims", ascending=False)
    .head(10)
)

fig = px.bar(
    food_claim,
    x="Food_Name",
    y="Claims",
    color="Claims",
    text_auto=True,
    title="Top 10 Claimed Food Items"
)

fig.update_layout(xaxis_tickangle=-40)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📅 Claims Over Time")

claims_time = (
    filtered_df.groupby(filtered_df["Timestamp"].dt.date)
    .size()
    .reset_index(name="Claims")
)

fig = px.line(
    claims_time,
    x="Timestamp",
    y="Claims",
    markers=True,
    title="Daily Food Claims"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏙️ Total Food Quantity by City")

city_qty = (
    filtered_df.groupby("Provider_City")["Quantity"]
    .sum()
    .reset_index()
)

fig = px.bar(
    city_qty,
    x="Provider_City",
    y="Quantity",
    color="Quantity",
    text_auto=True,
    title="Food Quantity by City"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏢 Quantity Donated by Provider")

provider_qty = (
    filtered_df.groupby("Provider_Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    provider_qty,
    x="Provider_Name",
    y="Quantity",
    color="Quantity",
    text_auto=True,
    title="Top Providers by Quantity Donated"
)

fig.update_layout(xaxis_tickangle=-40)

st.plotly_chart(fig, use_container_width=True)

