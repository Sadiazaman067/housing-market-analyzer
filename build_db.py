import pandas as pd
from sqlalchemy import create_engine

# Load raw data
df = pd.read_csv("AmesHousing.csv")

# Clean column names: remove spaces and slashes for easier SQL use
df.columns = [c.replace(" ", "").replace("/", "") for c in df.columns]

# ---- Build Neighborhoods table ----
neighborhoods = df["Neighborhood"].dropna().unique()
neighborhoods_df = pd.DataFrame({
    "NeighborhoodID": range(1, len(neighborhoods) + 1),
    "NeighborhoodName": neighborhoods
})

# Map neighborhood name -> ID
neigh_map = dict(zip(neighborhoods_df["NeighborhoodName"], neighborhoods_df["NeighborhoodID"]))
df["NeighborhoodID"] = df["Neighborhood"].map(neigh_map)

# ---- Build Properties table ----
properties_cols = [
    "PID", "NeighborhoodID", "LotArea", "LotFrontage",
    "OverallQual", "OverallCond", "YearBuilt", "YearRemodAdd",
    "GrLivArea", "TotalBsmtSF", "BedroomAbvGr", "FullBath", "HalfBath",
    "GarageCars", "GarageArea", "HouseStyle", "BldgType"
]
properties_df = df[properties_cols].drop_duplicates(subset="PID")

# ---- Build Sales table ----
sales_cols = ["PID", "SalePrice", "MoSold", "YrSold", "SaleType", "SaleCondition"]
sales_df = df[sales_cols].copy()
sales_df.insert(0, "SaleID", range(1, len(sales_df) + 1))

# ---- Write to SQLite database ----
engine = create_engine("sqlite:///housing.db")

neighborhoods_df.to_sql("Neighborhoods", engine, if_exists="replace", index=False)
properties_df.to_sql("Properties", engine, if_exists="replace", index=False)
sales_df.to_sql("Sales", engine, if_exists="replace", index=False)

print("Database built successfully: housing.db")
print(f"Neighborhoods: {len(neighborhoods_df)} rows")
print(f"Properties: {len(properties_df)} rows")
print(f"Sales: {len(sales_df)} rows")