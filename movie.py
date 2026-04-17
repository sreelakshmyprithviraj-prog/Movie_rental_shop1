import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
st.write("Debug: The app has started loading!")
actor=pd.read_csv("actor.csv")
address=pd.read_csv("address.csv")
category=pd.read_csv("category.csv")
city=pd.read_csv("city.csv")
country=pd.read_csv("country.csv")
customer=pd.read_csv("customer.csv")
film_actor=pd.read_csv("film_actor.csv")
film_category=pd.read_csv("film_category.csv")
film=pd.read_csv("film.csv")
inventory=pd.read_csv("inventory.csv")
language=pd.read_csv("language.csv")
payment=pd.read_csv("payment.csv")
rental=pd.read_csv("rental.csv")
staff=pd.read_csv("staff.csv")
store=pd.read_csv("store.csv")


#1. Gather all your dataframes into a dictionary based on your loaded variables
dataframes = {
    'actor': actor, 'address': address, 'category': category, 'city': city,
    'country': country, 'customer': customer, 'film_actor': film_actor,
    'film_category': film_category, 'film': film, 'inventory': inventory,
    'language': language, 'payment': payment, 'rental': rental,
    'staff': staff, 'store': store
}

# 2. Define a helper function to identify if a column contains datetime strings
def is_date_column(s):
    # We only care about object types (which usually contain strings)
    if not pd.api.types.is_object_dtype(s):
        return False
    
    # Drop any empty/NaN values to test
    s_clean = s.dropna()
    if s_clean.empty:
        return False
    
    try:
        # Check if the first 100 non-null values can be parsed as dates 
        # Using format='mixed' handles various date structures safely
        pd.to_datetime(s_clean.head(100), errors='raise', format='mixed')
        return True
    except (ValueError, TypeError, OverflowError):
        # If the values fail to parse, it's not a datetime column
        return False

# 3. Iterate through all variables and safely convert valid date columns 
for name, df in dataframes.items():
    converted_cols = []
    
    for col in df.columns:
        if is_date_column(df[col]):
            # If the column passes our check, convert it in-place
            df[col] = pd.to_datetime(df[col], errors='coerce', format='mixed')
            converted_cols.append(col)
            
    if converted_cols:
        print(f"Dataframe '{name}': successfully converted {converted_cols} to datetime64.")


total_revenue = payment['amount'].sum()
print(f"{total_revenue/1000:,.1f}K")


total_customer=len(customer)
print(total_customer)


total_orders=len(payment)
print(f"{total_orders/1000:,.1f}K")


print(f"Total Movies: {film.shape[0]}")

#Convert columns to datetime
payment['payment_date'] = pd.to_datetime(payment['payment_date'])
rental['rental_date'] = pd.to_datetime(rental['rental_date'])
rental['return_date'] = pd.to_datetime(rental['return_date']) 


#Extract the period/month from the actual payment date
payment['payment_month'] = payment['payment_date'].dt.to_period('M')

# Calculate how many days a movie was rented
rental['rental_duration_days'] = (rental['return_date'] - rental['rental_date']).dt.days


print("New columns created successfully!")



# Merge 1. Connect payments to rentals
master_table = pd.merge(payment, rental, on='rental_id', how='left')

# Merge 2. Connect to inventory (this gives us the film_id)
master_table = pd.merge(master_table, inventory, on='inventory_id', how='left')

# Merge 3: Connecting to film_category
master_table = pd.merge(master_table, film_category, on='film_id', how='left', suffixes=('', '_fc'))

# Merge 4: Connecting to film
master_table = pd.merge(master_table, film, on='film_id', how='left', suffixes=('', '_f'))

# Merge 5: Connecting to category
master_table = pd.merge(master_table, category, on='category_id', how='left', suffixes=('', '_cat'))
master_table = master_table.rename(columns={'name': 'category_name', 'name_cat': 'category_name'})

# Total Revenue
total_revenue = master_table['amount'].sum()

# Total count of successful payments/rentals
total_rentals = master_table['payment_id'].count()

# Average amount spent per transaction
average_payment = master_table['amount'].mean()

print(f"Top Level KPIs")
print(f"----------------------")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Rentals Processed: {total_rentals:,}")
print(f"Average Revenue per Rental: ${average_payment:,.2f}")


top_movies = master_table.groupby('title')['amount'].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Highest Earning Movies:")
print(top_movies)


plt.figure(figsize=(10, 5))
# Use 'category_name' (from Merge 5) and 'amount' (from the payment table)
revenue_by_cat = master_table.groupby('category_name')['amount'].sum().sort_values(ascending=False)

sns.barplot(x=revenue_by_cat.values, y=revenue_by_cat.index, palette='viridis', hue=revenue_by_cat.index)
plt.title('Total Revenue by Movie Category')
plt.xlabel('Total Revenue ($)')
plt.ylabel('Category')
plt.show()


plt.figure(figsize=(8, 4))
# Convert our 'period' month to string so the plot likes it
monthly_rev = master_table.groupby(master_table['payment_month'].astype(str))['amount'].sum()

plt.plot(monthly_rev.index, monthly_rev.values, marker='o', color='green', linewidth=2)
plt.title('Monthly Store Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
