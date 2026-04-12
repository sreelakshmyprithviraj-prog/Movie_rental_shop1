# Movie Rental Data Analysis

## Overview
This project presents a comprehensive data analysis pipeline based on a movie rental business dataset. By taking a granular relational database export—spread across 15 separate CSV files—and reconstructing it using Python and Pandas, this project uncovers critical business insights around revenue, movie performance, and customer rental trends.

## Key Skills Demonstrated
This repository serves as a practical portfolio piece showcasing proficiency in the following areas:
- **Data Cleaning & Wrangling:** Converting raw text columns into robust datetime formats, dropping irrelevant metadata, and engineering new features (such as calculating the duration of rentals in days).
- **Relational Data Joins:** Reconstructing a normalized, SQL-like schema back into a logical, unified Master Table using sequential Pandas `pd.merge()` operations.
- **Exploratory Data Analysis (EDA):** Aggregating operational data to calculate top-level Key Performance Indicators (KPIs) such as Total Revenue, Average Revenue per Rental, and Top Performing Movies.
- **Data Visualization:** Leveraging `matplotlib` and `seaborn` to build professional, intuitive charts that transform data into actionable insights, including revenue comparisons by genre and chronological business growth trends.

## Project Structure
- **`Student_Movie_Rental_Analysis.ipynb`** - The primary Jupyter Notebook containing the fully documented, step-by-step analysis workflow.
- **`movie.ipynb`** - Secondary/Sandbox notebook for data testing and analysis drafting.
- **`*.csv` data files** - The raw data tables representing the movie rental database schema (including `payment`, `rental`, `film`, `customer`, `category`, and more).

## How to Use

1. **Clone the repository** to your local machine:
   ```bash
   git clone <your-repository-url>
   cd Movie_rental_shop
   ```

2. **Install Dependencies**: 
   Ensure you have a Python environment set up. You will need the standard PyData stack. Install the requirements via pip:
   ```bash
   pip install pandas matplotlib seaborn jupyter
   ```

3. **Launch the Environment**:
   Start Jupyter to view the notebooks interactively:
   ```bash
   jupyter notebook
   ```

4. **Run the Analysis**: 
   Open `Student_Movie_Rental_Analysis.ipynb` in your browser or IDE. The notebook is thoroughly commented and fully self-contained. Execute the cells sequentially from top to bottom to witness the data loading, cleaning, relational merging, and final visualization generation.
