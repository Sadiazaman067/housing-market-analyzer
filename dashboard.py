import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import pickle
import numpy as np

# ---- Load models and data ----
engine = create_engine("sqlite:///housing.db")

@st.cache_data
def load_data():
    df = pd.read_sql("""
        SELECT p.*, n.NeighborhoodName, s.SalePrice, s.MoSold, s.YrSold, s.SaleCondition
        FROM Properties p
        JOIN Sales s ON p.PID = s.PID
        JOIN Neighborhoods n ON p.NeighborhoodID = n.NeighborhoodID
    """, engine)
    return df

@st.cache_data
def load_views():
    neigh_stats = pd.read_sql("SELECT * FROM neighborhood_stats", engine)
    price_sqft  = pd.read_sql("SELECT * FROM price_per_sqft", engine)
    yearly      = pd.read_sql("SELECT * FROM yearly_trends", engine)
    outliers    = pd.read_sql("SELECT * FROM outlier_properties", engine)
    return neigh_stats, price_sqft, yearly, outliers

with open("model_regression.pkl", "rb") as f:
    reg_model = pickle.load(f)
with open("model_classifier.pkl", "rb") as f:
    clf_model = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

feature_importance = pd.read_csv("feature_importances.csv", header=0)
feature_importance.columns = ["Feature", "Importance"]

df = load_data()
neigh_stats, price_sqft, yearly, outliers = load_views()

# ---- Sidebar navigation ----
st.sidebar.title("🏠 Housing Market Analyzer")
page = st.sidebar.radio("Navigate", ["Market Overview", "Price Predictor", "Model Performance"])

# ================================================================
# PAGE 1: Market Overview
# ================================================================
if page == "Market Overview":
    st.title("📊 Ames Housing Market Overview")
    st.markdown("Analyzing **2,930 home sales** across **28 neighborhoods** in Ames, Iowa.")

    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Median Sale Price", f"${df['SalePrice'].median():,.0f}")
    col2.metric("Avg Sale Price", f"${df['SalePrice'].mean():,.0f}")
    col3.metric("Total Sales", f"{len(df):,}")
    col4.metric("Neighborhoods", "28")

    st.divider()

    # Avg price by neighborhood
    st.subheader("Average Sale Price by Neighborhood")
    fig1 = px.bar(
        neigh_stats.sort_values("avg_price", ascending=True),
        x="avg_price", y="NeighborhoodName",
        orientation="h",
        labels={"avg_price": "Avg Sale Price ($)", "NeighborhoodName": "Neighborhood"},
        color="avg_price", color_continuous_scale="Blues"
    )
    fig1.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # Price per sqft
    st.subheader("Price Per Square Foot by Neighborhood")
    fig2 = px.bar(
        price_sqft.sort_values("avg_price_per_sqft", ascending=False),
        x="NeighborhoodName", y="avg_price_per_sqft",
        labels={"avg_price_per_sqft": "Avg $/sqft", "NeighborhoodName": "Neighborhood"},
        color="avg_price_per_sqft", color_continuous_scale="Greens"
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Year over year trends
    st.subheader("Year-Over-Year Sales Trends")
    fig3 = px.line(
        yearly, x="YrSold", y="avg_price",
        markers=True,
        labels={"avg_price": "Avg Sale Price ($)", "YrSold": "Year"},
    )
    fig3.update_traces(line_color="#636EFA", line_width=3)
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Sale price distribution
    st.subheader("Sale Price Distribution")
    fig4 = px.histogram(df, x="SalePrice", nbins=50, color_discrete_sequence=["#636EFA"])
    fig4.update_layout(xaxis_title="Sale Price ($)", yaxis_title="Count")
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # Outliers table
    st.subheader("🚨 Outlier Properties (Priced 50%+ Above Neighborhood Average)")
    st.dataframe(outliers.head(20), use_container_width=True)

# ================================================================
# PAGE 2: Price Predictor
# ================================================================
elif page == "Price Predictor":
    st.title("🔮 Home Price Predictor")
    st.markdown("Enter home details below to get an **AI-powered price estimate**.")

    col1, col2 = st.columns(2)

    with col1:
        neighborhood = st.selectbox("Neighborhood", sorted(le.classes_))
        overall_qual = st.slider("Overall Quality (1-10)", 1, 10, 5)
        overall_cond = st.slider("Overall Condition (1-10)", 1, 10, 5)
        year_built   = st.number_input("Year Built", 1872, 2010, 1990)
        year_remod   = st.number_input("Year Remodeled", 1950, 2010, 2000)
        gr_liv_area  = st.number_input("Above Ground Living Area (sqft)", 300, 6000, 1500)
        total_bsmt   = st.number_input("Total Basement Area (sqft)", 0, 3000, 800)

    with col2:
        lot_area     = st.number_input("Lot Area (sqft)", 1000, 100000, 10000)
        lot_frontage = st.number_input("Lot Frontage (ft)", 0, 200, 70)
        bedrooms     = st.number_input("Bedrooms Above Ground", 0, 8, 3)
        full_bath    = st.number_input("Full Bathrooms", 0, 4, 2)
        half_bath    = st.number_input("Half Bathrooms", 0, 2, 0)
        garage_cars  = st.number_input("Garage Capacity (cars)", 0, 4, 2)
        garage_area  = st.number_input("Garage Area (sqft)", 0, 1500, 400)

    if st.button("Predict Price", type="primary"):
        neigh_encoded = le.transform([neighborhood])[0]
        input_data = pd.DataFrame([{
            "LotArea": lot_area, "LotFrontage": lot_frontage,
            "OverallQual": overall_qual, "OverallCond": overall_cond,
            "YearBuilt": year_built, "YearRemodAdd": year_remod,
            "GrLivArea": gr_liv_area, "TotalBsmtSF": total_bsmt,
            "BedroomAbvGr": bedrooms, "FullBath": full_bath,
            "HalfBath": half_bath, "GarageCars": garage_cars,
            "GarageArea": garage_area, "NeighborhoodEncoded": neigh_encoded
        }])

        predicted_price = reg_model.predict(input_data)[0]
        is_overpriced   = clf_model.predict(input_data)[0]

        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("Estimated Sale Price", f"${predicted_price:,.0f}")
        col2.metric("Market Assessment", "⚠️ Above Market" if is_overpriced else "✅ Fair Price")

        # Show neighborhood context
        neigh_avg = neigh_stats[neigh_stats["NeighborhoodName"] == neighborhood]["avg_price"].values[0]
        diff = predicted_price - neigh_avg
        st.info(f"Neighborhood avg: **${neigh_avg:,.0f}** | This estimate is **${abs(diff):,.0f} {'above' if diff > 0 else 'below'}** the neighborhood average.")

# ================================================================
# PAGE 3: Model Performance
# ================================================================
elif page == "Model Performance":
    st.title("🤖 Model Performance")
    st.markdown("Evaluation results for the Random Forest models trained on Ames Housing data.")

    st.subheader("Regression Model — Predicting Sale Price")
    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", "0.898")
    col2.metric("Mean Abs Error", "$16,494")
    col3.metric("CV Mean R²", "0.877 ± 0.027")

    st.markdown("""
    - Trained on **2,344 homes**, tested on **586 homes**
    - Hyperparameters tuned via **GridSearchCV** (3-fold CV)
    - Best params: `max_depth=20`, `n_estimators=200`, `min_samples_split=2`
    """)

    st.divider()

    st.subheader("Top Features Driving Price")
    fig5 = px.bar(
    feature_importance.sort_values("Importance"),
    x="Importance", y="Feature", orientation="h",
    color="Importance", color_continuous_scale="Blues"
)
    fig5.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

    st.divider()

    st.subheader("Classification Model — Overpriced vs Fair Price")
    col1, col2 = st.columns(2)
    col1.metric("Overall Accuracy", "85%")
    col2.metric("Overpriced Precision", "87%")

    st.markdown("""
    - **Target**: Is the home priced more than 10% above its neighborhood average?
    - **808 overpriced** homes out of 2,930 total
    - Fair Price recall: **96%** | Overpriced recall: **61%**
    """)