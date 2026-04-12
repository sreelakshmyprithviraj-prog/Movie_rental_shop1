import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading all tables directly
actor = pd.read_csv("actor.csv")
address = pd.read_csv("address.csv")
category = pd.read_csv("category.csv")
city = pd.read_csv("city.csv")
country = pd.read_csv("country.csv")
customer = pd.read_csv("customer.csv")
film = pd.read_csv("film.csv")
film_actor = pd.read_csv("film_actor.csv")
film_category = pd.read_csv("film_category.csv")
inventory = pd.read_csv("inventory.csv")
language = pd.read_csv("language.csv")
payment = pd.read_csv("payment.csv")
rental = pd.read_csv("rental.csv")
staff = pd.read_csv("staff.csv")
store = pd.read_csv("store.csv")


# Let's verify the row counts of our most important tables
print(f"Total Customers: {customer.shape[0]}")
print(f"Total Movies: {film.shape[0]}")
print(f"Total Rental Events: {rental.shape[0]}")
print(f"Total Payments Made: {payment.shape[0]}")


# Look at the payment data
payment.head()


# Look at the rental data
rental.head()


# This sums up the empty values in each column
payment.isnull().sum()


# Convert text dates to real datetime logic
payment['payment_date'] = pd.to_datetime(payment['payment_date'])
rental['rental_date'] = pd.to_datetime(rental['rental_date'])
rental['return_date'] = pd.to_datetime(rental['return_date'])

# Drop useless columns from payment table to clean it up
payment = payment.drop(columns=['last_update'], errors='ignore')

# Show that the conversion worked
print("Data Types in Payment Table:")
print(payment.dtypes)


# Extract the period/month from the actual payment date
payment['payment_month'] = payment['payment_date'].dt.to_period('M')

# Calculate how many days a movie was rented
rental['rental_duration_days'] = (rental['return_date'] - rental['rental_date']).dt.days

# Show the new columns
print("New columns created successfully!")


# Merge 1
master_table = pd.merge(payment, rental, on='rental_id', how='left')
master_table.head(3)


# Merge 2
master_table = pd.merge(master_table, inventory, on='inventory_id', how='left')


# Merge 3
master_table = pd.merge(master_table, film[['film_id', 'title']], on='film_id', how='left')


# Merge 4
master_table = pd.merge(master_table, customer[['customer_id', 'first_name', 'last_name']], on='customer_id', how='left')

# Let's create a full name column for convenience
master_table['customer_name'] = master_table['first_name'] + " " + master_table['last_name']


# Merge 5 & 6
master_table = pd.merge(master_table, film_category, on='film_id', how='left')
master_table = pd.merge(master_table, category[['category_id', 'name']], on='category_id', how='left')

# Rename the category name column so it makes more sense
master_table = master_table.rename(columns={'name': 'category_name'})

print(f"Master table has {master_table.shape[0]} rows and {master_table.shape[1]} columns!")


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


# Grouping by the movie title and summing the money spent
top_movies = master_table.groupby('title')['amount'].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Highest Earning Movies:")
print(top_movies)


plt.figure(figsize=(10, 5))
revenue_by_cat = master_table.groupby('category_name')['amount'].sum().sort_values(ascending=False)

# Make a barplot
sns.barplot(x=revenue_by_cat.values, y=revenue_by_cat.index, palette='viridis', hue=revenue_by_cat.index, legend=False)
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