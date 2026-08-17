import pandas as pd
import matplotlib.pyplot as plt


# Load the real Online Retail dataset
print("Loading Online Retail dataset...")


df = pd.read_excel("data/Online Retail.xlsx")


print("Dataset loaded successfully!")


# Show the first 5 rows
print("\nFirst 5 rows:")

print(df.head())


# Show the size of the dataset
print("\nDataset size:")

print(df.shape)

# -----------------------------------------
# EXPLORE THE DATASET
# -----------------------------------------

print("\nColumn names:")

print(df.columns.tolist())

print("\nData types:")

print(df.dtypes)

print("\nMissing values:")

print(df.isnull().sum())

print("\nDuplicate rows:")

duplicates = df.duplicated().sum()

print(duplicates)

print("\nStatistical summary:")

print(
    df[
        [
            "Quantity",
            "UnitPrice"
        ]
    ].describe()
)
# -----------------------------------------
# SAVE ORIGINAL ROW COUNT
# -----------------------------------------

original_rows = len(df)

print("\nOriginal number of rows:")
print(original_rows)
# -----------------------------------------
# REMOVE DUPLICATES
# -----------------------------------------

df = df.drop_duplicates()

print("\nRows after removing duplicates:")
print(len(df))
# -----------------------------------------
# REMOVE MISSING PRODUCT DESCRIPTIONS
# -----------------------------------------

df = df.dropna(
    subset=["Description"]
)

print("\nRows after removing missing descriptions:")
print(len(df))
# -----------------------------------------
# REMOVE CANCELLED ORDERS
# -----------------------------------------

df = df[
    ~df["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
]

print("\nRows after removing cancelled orders:")
print(len(df))
# -----------------------------------------
# REMOVE INVALID QUANTITIES
# -----------------------------------------

df = df[
    df["Quantity"] > 0
]

print("\nRows after removing non-positive quantities:")
print(len(df))
# -----------------------------------------
# REMOVE INVALID PRICES
# -----------------------------------------

df = df[
    df["UnitPrice"] > 0
]

print("\nRows after removing non-positive prices:")
print(len(df))
# -----------------------------------------
# CLEANING SUMMARY
# -----------------------------------------

cleaned_rows = len(df)

rows_removed = original_rows - cleaned_rows

percentage_removed = (
    rows_removed / original_rows
) * 100


print("\n===== CLEANING SUMMARY =====")

print(f"Original rows: {original_rows:,}")

print(f"Cleaned rows: {cleaned_rows:,}")

print(f"Rows removed: {rows_removed:,}")

print(
    f"Percentage removed: "
    f"{percentage_removed:.2f}%"
)
# -----------------------------------------
# CREATE REVENUE COLUMN
# -----------------------------------------

df["Revenue"] = (
    df["Quantity"]
    *
    df["UnitPrice"]
)


print("\nRevenue example:")

print(
    df[
        [
            "Description",
            "Quantity",
            "UnitPrice",
            "Revenue"
        ]
    ].head()
)
# -----------------------------------------
# BUSINESS KPIs
# -----------------------------------------

total_revenue = df["Revenue"].sum()

total_units = df["Quantity"].sum()

total_orders = df["InvoiceNo"].nunique()

unique_products = df["StockCode"].nunique()

average_transaction_revenue = df["Revenue"].mean()


print("\n===== BUSINESS KPIs =====")

print(
    f"Total Revenue: "
    f"£{total_revenue:,.2f}"
)

print(
    f"Total Units Sold: "
    f"{total_units:,}"
)

print(
    f"Total Orders: "
    f"{total_orders:,}"
)

print(
    f"Unique Products: "
    f"{unique_products:,}"
)

print(
    f"Average Revenue per Transaction Row: "
    f"£{average_transaction_revenue:,.2f}"
)
# -----------------------------------------
# TOP 10 PRODUCTS BY REVENUE
# -----------------------------------------

product_revenue = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_products = product_revenue.head(10)

print("\n===== TOP 10 PRODUCTS BY REVENUE =====")

print(top_products)

# -----------------------------------------
# CHART 1: TOP PRODUCTS BY REVENUE
# -----------------------------------------

plt.figure(figsize=(10, 6))

top_products.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Products by Revenue")

plt.xlabel("Revenue (£)")

plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "images/top_products.png",
    dpi=300
)

plt.show()
# -----------------------------------------
# REVENUE BY COUNTRY
# -----------------------------------------

country_revenue = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== TOP 10 COUNTRIES BY REVENUE =====")

print(
    country_revenue.head(10)
)
# -----------------------------------------
# CHART 2: INTERNATIONAL MARKETS
# -----------------------------------------

international_revenue = (
    country_revenue
    .drop(
        "United Kingdom",
        errors="ignore"
    )
    .head(10)
)


plt.figure(figsize=(10, 6))


international_revenue.sort_values().plot(
    kind="barh"
)


plt.title(
    "Top 10 International Markets by Revenue"
)

plt.xlabel(
    "Revenue (£)"
)

plt.ylabel(
    "Country"
)

plt.tight_layout()


plt.savefig(
    "images/top_countries.png",
    dpi=300
)

plt.show()

# -----------------------------------------
# MONTHLY REVENUE ANALYSIS
# -----------------------------------------

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)


df["Month"] = (
    df["InvoiceDate"]
    .dt
    .to_period("M")
)


monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
)


print("\n===== MONTHLY REVENUE =====")

print(monthly_revenue)

# -----------------------------------------
# CHART 3: MONTHLY REVENUE
# -----------------------------------------

plt.figure(figsize=(10, 6))


monthly_revenue.plot(
    kind="line",
    marker="o"
)


plt.title(
    "Monthly Revenue Trend"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Revenue (£)"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()


plt.savefig(
    "images/monthly_revenue.png",
    dpi=300
)


plt.show()

# -----------------------------------------
# AVERAGE ORDER VALUE
# -----------------------------------------

order_revenue = (
    df.groupby("InvoiceNo")["Revenue"]
    .sum()
)


average_order_value = (
    order_revenue.mean()
)


print("\n===== AVERAGE ORDER VALUE =====")


print(
    f"Average Order Value: "
    f"£{average_order_value:,.2f}"
)
# -----------------------------------------
# REVENUE BY DAY OF WEEK
# -----------------------------------------

df["DayOfWeek"] = (
    df["InvoiceDate"]
    .dt
    .day_name()
)


day_revenue = (
    df.groupby("DayOfWeek")["Revenue"]
    .sum()
)


day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


day_revenue = (
    day_revenue
    .reindex(day_order)
    .dropna()
)


print("\n===== REVENUE BY DAY =====")

print(day_revenue)

# -----------------------------------------
# CHART 4: REVENUE BY DAY
# -----------------------------------------

plt.figure(figsize=(10, 6))


day_revenue.plot(
    kind="bar"
)


plt.title(
    "Revenue by Day of Week"
)

plt.xlabel(
    "Day"
)

plt.ylabel(
    "Revenue (£)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()


plt.savefig(
    "images/revenue_by_day.png",
    dpi=300
)


plt.show()

# -----------------------------------------
# SAVE CLEANED DATA
# -----------------------------------------

df.to_csv(
    "data/cleaned_online_retail.csv",
    index=False
)


print(
    "\nCleaned dataset saved successfully!"
)


print(
    "\nAnalysis completed successfully!"
)

