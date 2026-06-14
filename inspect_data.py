import pandas as pd

df = pd.read_csv("AmesHousing.csv")
print("Shape:", df.shape)
print("\nColomns:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())