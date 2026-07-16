# 🍲 Food Waste Management Dashboard
An interactive Streamlit dashboard for analyzing food donation and food waste management using **MySQL**, **Python**, **Pandas**, and **Plotly**. The dashboard provides insights into food providers, receivers, food listings, claims, and donation trends through interactive visualizations.

---

## 📌 Project Overview

Food waste is a major global challenge while many people still face food insecurity. This project helps analyze surplus food distribution by connecting food providers with receivers and visualizing important insights through an interactive dashboard.

The application integrates data from multiple relational tables stored in MySQL and presents them in an easy-to-understand dashboard.

---

## ✨ Features

- Interactive Streamlit dashboard
- MySQL database integration
- Dynamic sidebar filters
- KPI cards
- Interactive Plotly visualizations
- Provider contact search
- Download filtered dataset as CSV
- Responsive dashboard layout

---

## 📊 Dashboard Visualizations

The dashboard answers the following business questions:

- Number of food providers and receivers in each city
- Food contribution by provider type
- Contact information of providers by city
- Top receivers based on food claimed
- Total quantity of food available
- Food listings by city
- Most commonly available food types
- Food claims for each food item
- Providers with the highest successful claims
- Claim status distribution (Completed, Pending, Cancelled)
- Average quantity claimed per receiver
- Most claimed meal type
- Total quantity donated by each provider

---

## 🗂️ Dataset

The project consists of four datasets:

### Providers
- Provider_ID
- Name
- Type
- Address
- City
- Contact

### Receivers
- Receiver_ID
- Name
- Type
- City
- Contact

### Food Listings
- Food_ID
- Food_Name
- Quantity
- Expiry_Date
- Provider_ID
- Provider_Type
- Location
- Food_Type
- Meal_Type

### Claims
- Claim_ID
- Food_ID
- Receiver_ID
- Status
- Timestamp

---

## 🛠️ Technologies Used

- Python
- Streamlit
- MySQL
- SQL
- Pandas
- Plotly
- MySQL Connector

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/food-waste-management-dashboard.git
```

Move into the project folder

```bash
cd food-waste-management-dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🗄️ Database

Import the following CSV files into MySQL:

- providers_data.csv
- receivers_data.csv
- food_listings_data.csv
- claims_data.csv

Update your MySQL credentials inside `app.py`.

---

## 📸 Dashboard Preview

Add screenshots here.

Example:

```
images/dashboard.png
images/providers.png
images/claims.png
```

---

## 📁 Project Structure

```
food-waste-management-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── providers_data.csv
├── receivers_data.csv
├── food_listings_data.csv
├── claims_data.csv
├── images/
│   ├── dashboard.png
│   ├── claims.png
│   └── providers.png
└── sql/
    └── database.sql
```

---

## 🚀 Future Enhancements

- User authentication
- Email notifications
- Interactive maps
- AI-powered recommendations
- Real-time data updates
- Predictive analytics for food demand

## 📄 License

This project is developed for educational purposes.
