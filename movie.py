import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
st.title("Movie Rental Shop Analysis")
# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Load tables
actor = pd.read_csv('actor.csv')
address = pd.read_csv('address.csv')
category = pd.read_csv('category.csv')
city = pd.read_csv('city.csv')
country = pd.read_csv('country.csv')
customer = pd.read_csv('customer.csv')
film = pd.read_csv('film.csv')
film_actor = pd.read_csv('film_actor.csv')
film_category = pd.read_csv('film_category.csv')
inventory = pd.read_csv('inventory.csv')
language = pd.read_csv('language.csv')
payment = pd.read_csv('payment.csv')
rental = pd.read_csv('rental.csv')
staff = pd.read_csv('staff.csv')
store = pd.read_csv('store.csv')

print("All DataFrames loaded! (actor, address, category, city, country, customer, film, film_actor, film_category, inventory, language, payment, rental, staff, store)")

st.write(f"Number of rentals: {len(rental)}")
st.write(f"Number of payments: {len(payment)}")
st.write(f"Number of films: {len(film)}")
st.write(f"Number of customers: {len(customer)}")

print("\n--- Film Table Sample ---")
print(film.head(2))

print("\n--- Rental Table Sample ---")
print(rental.head(2))

print("\n--- Missing Values Check ---")
print("Missing values in Payment:")
print(payment.isnull().sum())

print("\nMissing values in Rental:")
print(rental.isnull().sum())

print("\n--- Duplicate Check ---")
print(f"Duplicate rental IDs: {rental['rental_id'].duplicated().sum()}")
print(f"Duplicate payment IDs: {payment['payment_id'].duplicated().sum()}")

# Convert rental dates from string to datetime
rental['rental_date'] = pd.to_datetime(rental['rental_date'])
rental['return_date'] = pd.to_datetime(rental['return_date'])

# Convert payment dates
payment['payment_date'] = pd.to_datetime(payment['payment_date'])

print("Dates converted to datetime. Check new types:")
print(rental[['rental_date', 'return_date']].dtypes)

# 1. Rental duration calculation (difference in days)
rental['rental_duration_days'] = (rental['return_date'] - rental['rental_date']).dt.days

# 2. Extract Year-Month for payments (e.g., '2005-05')
payment['payment_month'] = payment['payment_date'].dt.to_period('M')

print(rental[['rental_date', 'return_date', 'rental_duration_days']].head(3))
print(payment[['payment_date', 'payment_month']].head(3))

# Inner join on rental_id
rental_payment = pd.merge(rental, payment, on='rental_id', how='inner')
print(f"Records after Merge 1 (Rental + Payment): {len(rental_payment)}")
print(rental_payment[['rental_id', 'customer_id_x', 'amount']].head(2))

# Join Inventory table
rental_inv = pd.merge(rental_payment, inventory, on='inventory_id', how='inner')

# Join Film table
master_table = pd.merge(rental_inv, film, on='film_id', how='inner')

print(f"Records after Merge 2 (Adding Inventory & Film): {len(master_table)}")
print(master_table[['rental_id', 'amount', 'title', 'rating']].head(2))

# Link movie to category ID (telling Pandas to use explicit suffixes to avoid collisions)
master_with_cat_id = pd.merge(master_table, film_category, on='film_id', how='left', suffixes=('_master', '_cat'))

# Get category name
final_master = pd.merge(master_with_cat_id, category, on='category_id', how='left', suffixes=('_master', '_cat'))

# Rename 'name' from category table to 'category_name' just to be clear
final_master = final_master.rename(columns={'name': 'category_name'})

print("Category successfully added to Final Master Table!")
print(final_master[['title', 'category_name', 'amount']].head(3))

total_revenue = final_master['amount'].sum()
total_rentals = len(final_master)
avg_rental_payment = final_master['amount'].mean()

st.header("--- Key Performance Indicators ---")
st.write(f"Total Lifetime Revenue: ${total_revenue:,.2f}")
st.write(f"Total Number of Rentals: {total_rentals:,}")
st.write(f"Average Revenue per Rental Transaction: ${avg_rental_payment:.2f}")

st.header("\n-- Top 5 Highest Earning Movie Categories --")
top_categories = final_master.groupby('category_name')['amount'].sum().sort_values(ascending=False).head(5)
st.write(top_categories)

st.header("\n-- Best Customers by Revenue --")
top_customers = final_master.groupby('customer_id_x')['amount'].sum().sort_values(ascending=False).head(3)
st.write("Customer IDs:", top_customers.index.tolist())

plt.figure(figsize=(10, 6))
cat_revenue = final_master.groupby('category_name')['amount'].sum().sort_values(ascending=False).reset_index()

sns.barplot(data=cat_revenue, x='amount', y='category_name', palette="viridis")
plt.title("Total Revenue by Movie Category")
plt.xlabel("Revenue ($)")
plt.ylabel("Category")
st.pyplot(plt)

plt.figure(figsize=(8, 5))
# Filtering out NaNs (unreturned movies)
durations = final_master['rental_duration_days'].dropna()

sns.histplot(durations, bins=10, kde=False, color='skyblue')
plt.title("Distribution of Rental Durations")
plt.xlabel("Days Rented")
plt.ylabel("Number of Rentals")
st.pyplot(plt)

plt.figure(figsize=(10, 5))
# Group by payment month (converting Period to string index)
monthly_revenue = final_master.groupby(final_master['payment_month'].astype(str))['amount'].sum()

plt.plot(monthly_revenue.index, monthly_revenue.values, marker='o', linestyle='-', color='purple')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)