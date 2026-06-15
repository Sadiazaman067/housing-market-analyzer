import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")

st.set_page_config(page_title="RentSearch", page_icon="🏠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
    .stApp { background-color: #f8fafc; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 52px 40px 80px 40px;
        text-align: center;
    }
    .hero-title { font-size: 44px; font-weight: 800; color: white; margin-bottom: 8px; letter-spacing: -1px; }
    .hero-sub { font-size: 17px; color: rgba(255,255,255,0.8); }

    /* Search card */
    .search-card {
        background: white;
        border-radius: 20px;
        padding: 28px 32px 24px 32px;
        box-shadow: 0 8px 40px rgba(102,126,234,0.18);
        max-width: 1000px;
        margin: -44px auto 36px auto;
        position: relative;
        z-index: 10;
    }

    /* Inputs */
    .stTextInput input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important; padding: 11px 16px !important;
        font-size: 15px !important; background: #f8fafc !important;
        color: #1a202c !important;
    }
    .stTextInput input:focus { border-color: #667eea !important; background: white !important; }
    .stNumberInput input {
        border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        background: #f8fafc !important; color: #1a202c !important;
    }
    [data-testid="stSelectbox"] > div > div {
        border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        background: #f8fafc !important; color: #1a202c !important;
    }
    [data-testid="stMultiSelect"] > div > div {
        border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        background: #f8fafc !important;
    }

    /* Search button */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 11px 0 !important;
        font-size: 15px !important; font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(102,126,234,0.45) !important;
    }
    div[data-testid="stButton"] > button:hover { opacity: 0.92 !important; }

    /* Filter label */
    .fl { font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 5px; }

    /* KPI */
    .kpi-card {
        background: white; border-radius: 16px; padding: 20px 16px;
        text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
    }
    .kpi-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; font-weight: 600; }
    .kpi-value { font-size: 26px; font-weight: 800; }
    .kv1{color:#667eea;} .kv2{color:#10b981;} .kv3{color:#f59e0b;} .kv4{color:#ef4444;}

    /* Results label */
    .rlabel { font-size: 14px; color: #64748b; margin: 20px 0 16px 0; font-weight: 500; }

    /* Card */
    .lcard {
        background: white; border-radius: 18px; overflow: hidden;
        margin-bottom: 24px; box-shadow: 0 2px 14px rgba(0,0,0,0.07);
        border: 1px solid #f1f5f9;
    }
    .lcard-body { padding: 16px 18px 18px 18px; }
    .lcard-price { font-size: 22px; font-weight: 800; color: #667eea; margin-bottom: 5px; }
    .lcard-addr { font-size: 13px; color: #64748b; margin-bottom: 10px; line-height: 1.4; }
    .lcard-stats { font-size: 13px; color: #475569; font-weight: 500; margin-bottom: 10px; display: flex; gap: 14px; flex-wrap: wrap; }
    .lcard-zest-low { font-size: 12px; color: #10b981; font-weight: 600; margin-bottom: 8px; }
    .lcard-zest-hi  { font-size: 12px; color: #f59e0b; font-weight: 600; margin-bottom: 8px; }
    .lcard-badges { margin-bottom: 12px; }
    .badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 20px; margin: 2px 4px 2px 0; }
    .bg-green  { background: #dcfce7; color: #166534; }
    .bg-blue   { background: #dbeafe; color: #1e40af; }
    .bg-gray   { background: #f1f5f9; color: #475569; }
    .bg-purple { background: #ede9fe; color: #6d28d9; }
    .lcard-btn {
        display: block; background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; text-align: center; padding: 10px 0; border-radius: 10px;
        text-decoration: none; font-size: 13px; font-weight: 700;
    }
    .no-img {
        width: 100%; height: 195px; background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        display: flex; align-items: center; justify-content: center;
        color: #94a3b8; font-size: 13px; font-weight: 500;
    }
    .empty { text-align: center; padding: 80px 20px; }
    .empty-icon { font-size: 56px; margin-bottom: 16px; }
    .empty-title { font-size: 22px; font-weight: 700; color: #334155; margin-bottom: 8px; }
    .empty-sub { font-size: 14px; color: #94a3b8; }
    .content-wrap { max-width: 1100px; margin: 0 auto; padding: 0 24px 48px 24px; }
</style>
""", unsafe_allow_html=True)

# ---- Hero ----
st.markdown("""
<div class="hero">
    <div class="hero-title">🏠 Find Your Next Rental</div>
    <div class="hero-sub">Search thousands of real listings — updated daily from Zillow</div>
</div>
""", unsafe_allow_html=True)

# ---- Search Card ----
st.markdown('<div class="search-card">', unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns([5, 1, 1])
with r1c1:
    st.markdown('<div class="fl">📍 Location</div>', unsafe_allow_html=True)
    location = st.text_input("loc", placeholder="City, neighborhood, or ZIP — e.g. Austin, TX or 10001", label_visibility="collapsed")
with r1c2:
    st.markdown('<div class="fl">&nbsp;</div>', unsafe_allow_html=True)
    search_clicked = st.button("🔍 Search")
with r1c3:
    st.markdown('<div class="fl">📄 Page</div>', unsafe_allow_html=True)
    page_num = st.number_input("page", 1, 5, 1, label_visibility="collapsed")

r2c1, r2c2, r2c3, r2c4, r2c5 = st.columns(5)
with r2c1:
    st.markdown('<div class="fl">💰 Min Rent</div>', unsafe_allow_html=True)
    min_price = st.number_input("minp", 0, 50000, 0, step=100, label_visibility="collapsed")
with r2c2:
    st.markdown('<div class="fl">💰 Max Rent</div>', unsafe_allow_html=True)
    max_price = st.number_input("maxp", 0, 50000, 0, step=100, label_visibility="collapsed")
with r2c3:
    st.markdown('<div class="fl">🛏 Min Beds</div>', unsafe_allow_html=True)
    bed_min = st.selectbox("bedmin", ["No_Min","1","2","3","4","5"], label_visibility="collapsed")
with r2c4:
    st.markdown('<div class="fl">🛏 Max Beds</div>', unsafe_allow_html=True)
    bed_max = st.selectbox("bedmax", ["No_Max","1","2","3","4","5"], label_visibility="collapsed")
with r2c5:
    st.markdown('<div class="fl">🐾 Pets</div>', unsafe_allow_html=True)
    pets = st.multiselect("pets", ["Large dogs","Small dogs","Cats"], label_visibility="collapsed")

r3c1, r3c2 = st.columns([2, 1])
with r3c1:
    st.markdown('<div class="fl">🏡 Home Type</div>', unsafe_allow_html=True)
    home_types = st.multiselect("htypes",
        ["Houses","Apartments/Condos/Co-ops","Townhomes"],
        default=["Houses","Apartments/Condos/Co-ops"],
        label_visibility="collapsed")
with r3c2:
    st.markdown('<div class="fl">📊 Sort By</div>', unsafe_allow_html=True)
    sort_map = {"Recommended":"Rental_Priority_Score","Newest":"Newest","Price ↑":"Price_Low_High","Price ↓":"Price_High_Low"}
    sort_label = st.selectbox("sort", list(sort_map.keys()), label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# ---- Results ----
st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

if not search_clicked or not location:
    st.markdown("""
    <div class="empty">
        <div class="empty-icon">🔍</div>
        <div class="empty-title">Search for rentals above</div>
        <div class="empty-sub">Enter any US city, neighborhood, or ZIP code to get started</div>
    </div>""", unsafe_allow_html=True)
else:
    with st.spinner(f"Searching rentals in {location}..."):
        try:
            params = {
                "location": location,
                "listingStatus": "For_Rent",
                "page": page_num,
                "sortOrder": sort_map[sort_label],
            }
            if min_price > 0 and max_price > 0:
                params["listPriceRange"] = f"min:{min_price}, max:{max_price}"
            elif min_price > 0:
                params["listPriceRange"] = f"min:{min_price}"
            elif max_price > 0:
                params["listPriceRange"] = f"max:{max_price}"
            if bed_min != "No_Min":
                params["bed_min"] = bed_min
            if bed_max != "No_Max":
                params["bed_max"] = bed_max
            if pets:
                pet_map = {"Large dogs":"Allow large dogs","Small dogs":"Allow small dogs","Cats":"Allow cats"}
                params["pets"] = ", ".join([pet_map[p] for p in pets])
            if home_types:
                params["homeType"] = ", ".join(home_types)

            resp = requests.get(
                "https://private-zillow.p.rapidapi.com/search/byaddress",
                headers={"x-rapidapi-host":"private-zillow.p.rapidapi.com","x-rapidapi-key":API_KEY},
                params=params
            )
            data = resp.json()
            listings = data.get("searchResults", [])
            total = data.get("resultsCount", {}).get("totalMatchingCount", len(listings))

            if not listings:
                st.markdown(f"""
                <div class="empty">
                    <div class="empty-icon">😕</div>
                    <div class="empty-title">No rentals found in {location}</div>
                    <div class="empty-sub">Try a nearby city or a broader search area like "Detroit, MI"</div>
                </div>""", unsafe_allow_html=True)
            else:
                # Prices for KPIs
                prices = []
                for item in listings:
                    v = item.get("property", {}).get("price", {}).get("value", 0)
                    if v and v > 0:
                        prices.append(int(v))

                # KPI row
                k1, k2, k3, k4 = st.columns(4)
                def kpi(col, label, value, cls):
                    col.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value {cls}">{value}</div></div>', unsafe_allow_html=True)

                kpi(k1, "Rentals Found", f"{total:,}", "kv1")
                kpi(k2, "Avg Rent", f"${sum(prices)//len(prices):,}/mo" if prices else "N/A", "kv2")
                kpi(k3, "Lowest Rent", f"${min(prices):,}/mo" if prices else "N/A", "kv3")
                kpi(k4, "Highest Rent", f"${max(prices):,}/mo" if prices else "N/A", "kv4")

                st.markdown(f'<div class="rlabel">Showing <strong>{min(30,len(listings))}</strong> of <strong>{total:,}</strong> rentals in <strong>{location}</strong></div>', unsafe_allow_html=True)

                # Cards
                cols = st.columns(3)
                for i, item in enumerate(listings[:30]):
                    prop    = item.get("property", {})
                    addr    = prop.get("address", {})
                    media   = prop.get("media", {})
                    rental  = prop.get("rental", {})

                    # Address
                    street  = addr.get("streetAddress") or ""
                    city_s  = addr.get("city") or ""
                    state_s = addr.get("state") or ""
                    zipcode = addr.get("zipcode") or ""
                    full_addr = ", ".join(filter(None, [street, city_s, state_s])) + (" " + zipcode if zipcode else "")
                    full_addr = full_addr.strip(", ") or "Address not available"

                    # Price
                    price_val = prop.get("price", {}).get("value")
                    price_str = f"${int(price_val):,}/mo" if price_val else "Contact for price"

                    # Zillow estimate
                    rent_est  = prop.get("estimates", {}).get("rentZestimate")

                    # Details
                    beds      = prop.get("bedrooms")
                    baths     = prop.get("bathrooms")
                    sqft      = prop.get("livingArea")
                    prop_type = prop.get("propertyType") or ""
                    days      = prop.get("daysOnZillow")
                    year_built = prop.get("yearBuilt")
                    can_apply  = rental.get("areApplicationsAccepted", False)

                    # Image
                    img = media.get("propertyPhotoLinks", {}).get("highResolutionLink")

                    # Link — always use zpid-based web URL
                    zpid = prop.get("zpid")
                    if zpid:
                        link = f"https://www.zillow.com/homedetails/{zpid}_zpid/"
                    else:
                        link = "https://www.zillow.com/homes/for_rent/"

                    # --- Build HTML safely with Python variables, no nested f-strings ---

                    img_html = f'<img src="{img}" style="width:100%;height:195px;object-fit:cover;">' \
                               if img else '<div class="no-img">📷 No Photo Available</div>'

                    # Stats
                    stats = []
                    if beds is not None:  stats.append(f"🛏 {beds} bd")
                    if baths is not None: stats.append(f"🚿 {baths} ba")
                    if sqft:              stats.append(f"📐 {int(sqft):,} sqft")
                    stats_html = "  ·  ".join(stats) if stats else ""

                    # Zestimate line
                    zest_html = ""
                    if rent_est and price_val:
                        diff = int(price_val) - int(rent_est)
                        if diff < -50:
                            zest_html = f'<div class="lcard-zest-low">✓ ${abs(diff):,} below Zillow estimate (est. ${int(rent_est):,}/mo)</div>'
                        elif diff > 100:
                            zest_html = f'<div class="lcard-zest-hi">↑ ${diff:,} above Zillow estimate (est. ${int(rent_est):,}/mo)</div>'

                    # Badges
                    badges = []
                    if can_apply:
                        badges.append('<span class="badge bg-green">✓ Apply Now</span>')
                    if days is not None:
                        badges.append(f'<span class="badge bg-gray">{days}d listed</span>')
                    if prop_type:
                        clean = prop_type.replace("singleFamily","Single Family").replace("apartment","Apartment")\
                                         .replace("condo","Condo").replace("townhouse","Townhouse")\
                                         .replace("multiFamily","Multi-Family")
                        badges.append(f'<span class="badge bg-blue">{clean}</span>')
                    if year_built:
                        badges.append(f'<span class="badge bg-purple">Built {year_built}</span>')
                    badges_html = "".join(badges)

                    card_html = f"""
<div class="lcard">
    {img_html}
    <div class="lcard-body">
        <div class="lcard-price">{price_str}</div>
        <div class="lcard-addr">{full_addr}</div>
        <div class="lcard-stats">{stats_html}</div>
        {zest_html}
        <div class="lcard-badges">{badges_html}</div>
        <a href="{link}" target="_blank" class="lcard-btn">View on Zillow →</a>
    </div>
</div>"""
                    with cols[i % 3]:
                        st.markdown(card_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)