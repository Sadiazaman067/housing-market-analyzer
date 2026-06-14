import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, r2_score, classification_report
from sklearn.preprocessing import LabelEncoder
import pickle

# ---- Load data from SQL database (not raw CSV) ----
engine = create_engine("sqlite:///housing.db")

df = pd.read_sql("""
    SELECT 
        p.LotArea, p.LotFrontage, p.OverallQual, p.OverallCond,
        p.YearBuilt, p.YearRemodAdd, p.GrLivArea, p.TotalBsmtSF,
        p.BedroomAbvGr, p.FullBath, p.HalfBath, p.GarageCars, p.GarageArea,
        n.NeighborhoodName, s.SalePrice, s.YrSold
    FROM Properties p
    JOIN Sales s ON p.PID = s.PID
    JOIN Neighborhoods n ON p.NeighborhoodID = n.NeighborhoodID
""", engine)

print(f"Loaded {len(df)} rows from database")

# ---- Preprocessing ----
# Fill missing numeric values with median
df["LotFrontage"] = df["LotFrontage"].fillna(df["LotFrontage"].median())
df["TotalBsmtSF"] = df["TotalBsmtSF"].fillna(0)
df["GarageCars"] = df["GarageCars"].fillna(0)
df["GarageArea"] = df["GarageArea"].fillna(0)

# Encode neighborhood as a number
le = LabelEncoder()
df["NeighborhoodEncoded"] = le.fit_transform(df["NeighborhoodName"])

# Save the label encoder so the dashboard can use it later
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# ---- Features and target ----
features = [
    "LotArea", "LotFrontage", "OverallQual", "OverallCond",
    "YearBuilt", "YearRemodAdd", "GrLivArea", "TotalBsmtSF",
    "BedroomAbvGr", "FullBath", "HalfBath", "GarageCars",
    "GarageArea", "NeighborhoodEncoded"
]

X = df[features]
y_reg = df["SalePrice"]

# ---- REGRESSION: Predict Sale Price ----
print("\n--- REGRESSION: Predicting Sale Price ---")

X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)

# Baseline: Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
print(f"Linear Regression R²: {r2_score(y_test, lr_preds):.3f}")
print(f"Linear Regression MAE: ${mean_absolute_error(y_test, lr_preds):,.0f}")

# Random Forest with cross-validation
rf = RandomForestRegressor(random_state=42)
cv_scores = cross_val_score(rf, X, y_reg, cv=5, scoring="r2")
print(f"\nRandom Forest CV R² scores: {cv_scores.round(3)}")
print(f"Mean CV R²: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

# Hyperparameter tuning with GridSearchCV
print("\nRunning GridSearchCV (this may take a minute)...")
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5]
}
grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3, scoring="r2", n_jobs=-1)
grid_search.fit(X_train, y_train)

best_rf = grid_search.best_estimator_
best_preds = best_rf.predict(X_test)
print(f"Best params: {grid_search.best_params_}")
print(f"Tuned Random Forest R²: {r2_score(y_test, best_preds):.3f}")
print(f"Tuned Random Forest MAE: ${mean_absolute_error(y_test, best_preds):,.0f}")

# Save the best regression model
with open("model_regression.pkl", "wb") as f:
    pickle.dump(best_rf, f)
print("Regression model saved: model_regression.pkl")

# ---- CLASSIFICATION: Predict if house is overpriced ----
print("\n--- CLASSIFICATION: Overpriced vs Fair Price ---")

# Label: overpriced = SalePrice > 110% of neighborhood average
neigh_avg = df.groupby("NeighborhoodName")["SalePrice"].transform("mean")
df["Overpriced"] = (df["SalePrice"] > neigh_avg * 1.1).astype(int)
print(f"Overpriced houses: {df['Overpriced'].sum()} / {len(df)}")

y_clf = df["Overpriced"]
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_clf, test_size=0.2, random_state=42)

# Random Forest Classifier
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train_c, y_train_c)
clf_preds = rfc.predict(X_test_c)
print("\nClassification Report:")
print(classification_report(y_test_c, clf_preds, target_names=["Fair Price", "Overpriced"]))

# Save classifier
with open("model_classifier.pkl", "wb") as f:
    pickle.dump(rfc, f)
print("Classifier saved: model_classifier.pkl")

# ---- Feature importance ----
importances = pd.Series(best_rf.feature_importances_, index=features).sort_values(ascending=False)
print("\nTop 5 features driving price:")
print(importances.head())

# Save feature importances for dashboard
importances.to_csv("feature_importances.csv")
print("Feature importances saved: feature_importances.csv")