import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. LOAD THE DATA
# --------------------------------------------------

df = pd.read_csv("sales_data.csv")

print("\nFIRST 5 ROWS:")
print(df.head())


# --------------------------------------------------
# 2. UNDERSTAND THE DATA
# --------------------------------------------------

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns)

print("\nDATA TYPES:")
print(df.dtypes)

print("\nMISSING VALUES:")
print(df.isnull().sum())


# --------------------------------------------------
# 3. CONVERT DATE COLUMN
# --------------------------------------------------

df["date"] = pd.to_datetime(df["date"])

print("\nDATE COLUMN AFTER CONVERSION:")
print(df["date"].head())


# --------------------------------------------------
# 4. CALCULATE REVENUE
# --------------------------------------------------

# Revenue before discount
df["gross_revenue"] = df["units_sold"] * df["unit_price"]

# Discount amount
df["discount_amount"] = df["gross_revenue"] * df["discount"]

# Final revenue after discount
df["revenue"] = df["gross_revenue"] - df["discount_amount"]

print("\nDATA WITH REVENUE:")
print(
    df[
        [
            "product",
            "units_sold",
            "unit_price",
            "discount",
            "revenue"
        ]
    ].head()
)


# --------------------------------------------------
# 5. BASIC STATISTICS
# --------------------------------------------------

total_revenue = df["revenue"].sum()

average_revenue = df["revenue"].mean()

total_units = df["units_sold"].sum()

highest_sale = df["revenue"].max()


print("\nSALES SUMMARY")

print(f"Total Revenue: €{total_revenue:.2f}")

print(f"Average Revenue per Sale: €{average_revenue:.2f}")

print(f"Total Units Sold: {total_units}")

print(f"Highest Single Sale: €{highest_sale:.2f}")


# --------------------------------------------------
# 6. REVENUE BY PRODUCT
# --------------------------------------------------

product_revenue = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nREVENUE BY PRODUCT:")
print(product_revenue)


# Find the best product
best_product = product_revenue.idxmax()

print(f"\nBest Product by Revenue: {best_product}")


# --------------------------------------------------
# 7. REVENUE BY REGION
# --------------------------------------------------

region_revenue = (
    df.groupby("region")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nREVENUE BY REGION:")
print(region_revenue)


best_region = region_revenue.idxmax()

print(f"\nBest Performing Region: {best_region}")


# --------------------------------------------------
# 8. CREATE A MONTH COLUMN
# --------------------------------------------------

df["month"] = df["date"].dt.strftime("%Y-%m")

monthly_revenue = df.groupby("month")["revenue"].sum()

print("\nMONTHLY REVENUE:")
print(monthly_revenue)


# --------------------------------------------------
# 9. NUMPY ANALYSIS
# --------------------------------------------------

revenue_array = df["revenue"].to_numpy()

numpy_average = np.mean(revenue_array)

numpy_maximum = np.max(revenue_array)

numpy_minimum = np.min(revenue_array)


print("\nNUMPY ANALYSIS:")

print(f"Average Revenue: €{numpy_average:.2f}")

print(f"Maximum Revenue: €{numpy_maximum:.2f}")

print(f"Minimum Revenue: €{numpy_minimum:.2f}")


# Count sales above average
above_average_sales = np.sum(
    revenue_array > numpy_average
)

print(
    f"Number of Sales Above Average: "
    f"{above_average_sales}"
)


# --------------------------------------------------
# 10. MATPLOTLIB - REVENUE BY PRODUCT
# --------------------------------------------------

plt.figure(figsize=(8, 5))

product_revenue.plot(kind="bar")

plt.title("Total Revenue by Product")

plt.xlabel("Product")

plt.ylabel("Revenue (€)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("revenue_by_product.png")

plt.show()


# --------------------------------------------------
# 11. MATPLOTLIB - MONTHLY REVENUE
# --------------------------------------------------

plt.figure(figsize=(8, 5))

monthly_revenue.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Revenue Trend")

plt.xlabel("Month")

plt.ylabel("Revenue (€)")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig("monthly_revenue.png")

plt.show()


# --------------------------------------------------
# 12. UNITS SOLD VS REVENUE
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["units_sold"],
    df["revenue"],
    alpha=0.7
)

plt.title("Units Sold vs Revenue")

plt.xlabel("Units Sold")

plt.ylabel("Revenue (€)")

plt.tight_layout()

plt.savefig("units_vs_revenue.png")

plt.show()


# --------------------------------------------------
# 13. SAVE CLEANED DATA
# --------------------------------------------------

df.to_csv(
    "cleaned_sales_data.csv",
    index=False
)

print(
    "\nAnalysis completed successfully!"
)

print(
    "Cleaned dataset saved as cleaned_sales_data.csv"
)