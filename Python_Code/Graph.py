import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load House Price Dataset
df = pd.read_csv("D:\House_Price_Prediction_524_524\Dataset\dataset.csv")

#Display first 5 records
print(df.head())

#Dataset information
print(df.info())

#Statistical summary
print(df.describe())

#Histogram 
plt.hist(df["price"], bins=30)
plt.xlabel("House Price")
plt.ylabel("Frequency")
plt.title("House Price Distribution")
plt.show()

#Box Plot
plt.boxplot(df["price"])
plt.ylabel("House Price")
plt.title("Box Plot of House Prices")
plt.show()

#Pie Chart - Furnishing
furnishing_count = df["furnishing"].value_counts()
plt.pie(
    furnishing_count,
    labels=furnishing_count.index,
    autopct="%1.1f%%"
)
plt.title("Furnishing Status Distribution")
plt.show()

#Bar Chart - Average Price by BHK
avg_price = df.groupby("bhk")["price"].mean()
plt.bar(
    avg_price.index.astype(str),
    avg_price.values
)

plt.xlabel("BHK")
plt.ylabel("Average Price")
plt.title("Average House Price by BHK")
plt.show()

#Correlation Matrix
numeric_data = df[
    ["square_feet", "price_per_sqft", "price", "bhk"]
]
print("\nCorrelation Matrix:")
print(numeric_data.corr()) 
plt.figure(figsize=(8, 6))
plt.imshow(
    numeric_data.corr(),
    cmap="coolwarm",
    interpolation="nearest"
)
plt.colorbar()
plt.xticks(
    range(len(numeric_data.columns)),
    numeric_data.columns,
    rotation=45
)
plt.yticks(
    range(len(numeric_data.columns)),
    numeric_data.columns
)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()