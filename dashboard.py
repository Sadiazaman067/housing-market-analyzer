import streamlit as st
import streamlit.components.v1 as components
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
    .stApp { background-color: #f0f4ff; }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
    [data-testid="stSidebar"] {display:none;}
    [data-testid="collapsedControl"] {display:none;}
    .block-container { padding: 0 !important; }

    /* Inputs light mode */
    .stTextInput input {
        border: 2px solid #e2e8f0 !important; border-radius: 12px !important;
        padding: 11px 16px !important; font-size: 15px !important;
        background: white !important; color: #1a202c !important;
    }
    .stTextInput input:focus { border-color: #667eea !important; }
    .stNumberInput input {
        border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        background: white !important; color: #1a202c !important;
    }
    [data-testid="stSelectbox"] > div > div {
        border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        background: white !important; color: #1a202c !important;
    }
    [data-testid="stMultiSelect"] > div > div {
        border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        background: white !important;
    }

    /* Search button */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 13px 0 !important;
        font-size: 16px !important; font-weight: 700 !important;
        width: 100% !important; letter-spacing: 0.4px !important;
        box-shadow: 0 4px 18px rgba(102,126,234,0.5) !important;
        margin-top: 22px !important;
    }
    div[data-testid="stButton"] > button:hover {
        box-shadow: 0 6px 24px rgba(102,126,234,0.65) !important;
        opacity: 0.95 !important;
    }

    /* Filter label */
    .fl { font-size: 11px; font-weight: 700; color: #64748b;
          text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }

    /* KPI */
    .kpi-card { background: white; border-radius: 16px; padding: 20px 16px;
        text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
    .kpi-label { font-size: 11px; color: #94a3b8; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 6px; font-weight: 600; }
    .kpi-value { font-size: 26px; font-weight: 800; }
    .kv1{color:#667eea;} .kv2{color:#10b981;} .kv3{color:#f59e0b;} .kv4{color:#ef4444;}

    .rlabel { font-size: 14px; color: #64748b; margin: 20px 0 16px 0; font-weight: 500; }
    .empty { text-align: center; padding: 80px 20px; }
    .empty-icon { font-size: 56px; margin-bottom: 16px; }
    .empty-title { font-size: 22px; font-weight: 700; color: #334155; margin-bottom: 8px; }
    .empty-sub { font-size: 14px; color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ---- Hero banner ----
st.markdown("""
<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
     padding:56px 40px 56px 40px;text-align:center;">
    <div style="font-size:44px;font-weight:800;color:white;margin-bottom:10px;letter-spacing:-1px;">
        🏠 Find Your Next Rental
    </div>
    <div style="font-size:17px;color:rgba(255,255,255,0.82);">
        Search thousands of real listings — updated daily from Zillow
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Search form ----
st.markdown("""
<div style="background:white;padding:28px 40px 24px 40px;
     box-shadow:0 4px 24px rgba(102,126,234,0.10);border-bottom:1px solid #e2e8f0;">
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding: 24px 32px 8px 32px; background:white;">', unsafe_allow_html=True)

    # Row 1: Location (wide) + Search button
    c_loc, c_btn = st.columns([6, 1])
    with c_loc:
        st.markdown('<div class="fl">📍 Location</div>', unsafe_allow_html=True)
        location = st.text_input("loc", placeholder="City, neighborhood, or ZIP — e.g. Austin, TX or 10001",
                                  label_visibility="collapsed")
    with c_btn:
        search_clicked = st.button("Search")

    # Row 2: Filters
    f1, f2, f3, f4, f5, f6, f7 = st.columns(7)
    with f1:
        st.markdown('<div class="fl">💰 Min Rent</div>', unsafe_allow_html=True)
        min_price = st.number_input("minp", 0, 50000, 0, step=100, label_visibility="collapsed")
    with f2:
        st.markdown('<div class="fl">💰 Max Rent</div>', unsafe_allow_html=True)
        max_price = st.number_input("maxp", 0, 50000, 0, step=100, label_visibility="collapsed")
    with f3:
        st.markdown('<div class="fl">🛏 Min Beds</div>', unsafe_allow_html=True)
        bed_min = st.selectbox("bedmin", ["No_Min","1","2","3","4","5"], label_visibility="collapsed")
    with f4:
        st.markdown('<div class="fl">🛏 Max Beds</div>', unsafe_allow_html=True)
        bed_max = st.selectbox("bedmax", ["No_Max","1","2","3","4","5"], label_visibility="collapsed")
    with f5:
        st.markdown('<div class="fl">🐾 Pets</div>', unsafe_allow_html=True)
        pets = st.multiselect("pets", ["Large dogs","Small dogs","Cats"], label_visibility="collapsed")
    with f6:
        st.markdown('<div class="fl">📅 Move-in Date</div>', unsafe_allow_html=True)
        move_in = st.date_input("movein", value=None, label_visibility="collapsed")
    with f7:
        st.markdown('<div class="fl">📊 Sort By</div>', unsafe_allow_html=True)
        sort_map = {
            "Recommended": "Rental_Priority_Score",
            "Newest Listed": "Newest",
            "Price: Low to High": "Price_Low_High",
            "Price: High to Low": "Price_High_Low",
        }
        sort_label = st.selectbox("sort", list(sort_map.keys()), label_visibility="collapsed")

    # Row 3: Home type + page
    g1, g2, g3, g4 = st.columns([3, 1, 1, 1])
    with g1:
        st.markdown('<div class="fl">🏡 Home Type</div>', unsafe_allow_html=True)
        home_types = st.multiselect("htypes",
            ["Houses","Apartments/Condos/Co-ops","Townhomes"],
            default=["Houses","Apartments/Condos/Co-ops"],
            label_visibility="collapsed")
    with g2:
        st.markdown('<div class="fl">📍 Radius (miles)</div>', unsafe_allow_html=True)
        radius = st.selectbox("radius", ["Any","1","2","5","10","20","30","50"], label_visibility="collapsed")
    with g3:
        st.markdown('<div class="fl">📐 Min sqft</div>', unsafe_allow_html=True)
        min_sqft = st.number_input("minsqft", 0, 10000, 0, step=100, label_visibility="collapsed")
    with g4:
        st.markdown('<div class="fl">📄 Page</div>', unsafe_allow_html=True)
        page_num = st.number_input("page", 1, 5, 1, label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

# ---- Divider ----
st.markdown('<div style="height:32px;background:#f0f4ff;"></div>', unsafe_allow_html=True)

# ---- Results ----
st.markdown('<div style="padding:0 32px 48px 32px;">', unsafe_allow_html=True)

def make_card(img, price_str, full_addr, stats_html, zest_html, badges_html, link):
    img_tag = (f'<img src="{img}" style="width:100%;height:200px;object-fit:cover;display:block;">'
               if img else
               '<div style="width:100%;height:200px;background:linear-gradient(135deg,#f1f5f9,#e2e8f0);'
               'display:flex;align-items:center;justify-content:center;color:#94a3b8;'
               'font-size:13px;font-weight:500;">📷 No Photo Available</div>')

    zest_block = (f'<div style="font-size:12px;font-weight:600;margin-bottom:8px;">{zest_html}</div>'
                  if zest_html else '')
    badge_block = (f'<div style="margin-bottom:12px;">{badges_html}</div>'
                   if badges_html else '')
    stats_block = (f'<div style="font-size:13px;color:#475569;font-weight:500;margin-bottom:10px;">{stats_html}</div>'
                   if stats_html else '')

    return f"""
<div style="background:white;border-radius:18px;overflow:hidden;margin-bottom:24px;
     box-shadow:0 2px 14px rgba(0,0,0,0.07);border:1px solid #f1f5f9;
     font-family:'Inter',sans-serif;transition:transform 0.2s;">
    {img_tag}
    <div style="padding:16px 18px 18px 18px;">
        <div style="font-size:22px;font-weight:800;color:#667eea;margin-bottom:5px;">{price_str}</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:10px;line-height:1.4;">{full_addr}</div>
        {stats_block}
        {zest_block}
        {badge_block}
        <a href="{link}" target="_blank"
           style="display:block;background:linear-gradient(135deg,#667eea,#764ba2);
           color:white;text-align:center;padding:10px 0;border-radius:10px;
           text-decoration:none;font-size:13px;font-weight:700;font-family:'Inter',sans-serif;">
           View on Zillow →
        </a>
    </div>
</div>"""

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
            if bed_min != "No_Min": params["bed_min"] = bed_min
            if bed_max != "No_Max": params["bed_max"] = bed_max
            if pets:
                pet_map = {"Large dogs":"Allow large dogs","Small dogs":"Allow small dogs","Cats":"Allow cats"}
                params["pets"] = ", ".join([pet_map[p] for p in pets])
            if home_types:
                params["homeType"] = ", ".join(home_types)
            if move_in:
                params["move_in_date"] = move_in.strftime("%m/%d/%Y")
            if radius and radius != "Any":
                params["radius"] = radius
            if min_sqft > 0:
                params["squareFeetRange"] = f"min:{min_sqft}"

            resp = requests.get(
                "https://private-zillow.p.rapidapi.com/search/byaddress",
                headers={"x-rapidapi-host":"private-zillow.p.rapidapi.com",
                         "x-rapidapi-key":API_KEY},
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
                    <div class="empty-sub">Try a nearby city or broader area like "Detroit, MI"</div>
                </div>""", unsafe_allow_html=True)
            else:
                prices = [int(i.get("property",{}).get("price",{}).get("value",0))
                          for i in listings
                          if i.get("property",{}).get("price",{}).get("value",0)]

                # KPIs
                k1,k2,k3,k4 = st.columns(4)
                with k1:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Rentals Found</div><div class="kpi-value kv1">{total:,}</div></div>', unsafe_allow_html=True)
                with k2:
                    avg = f"${sum(prices)//len(prices):,}/mo" if prices else "N/A"
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Avg Rent</div><div class="kpi-value kv2">{avg}</div></div>', unsafe_allow_html=True)
                with k3:
                    lo = f"${min(prices):,}/mo" if prices else "N/A"
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Lowest Rent</div><div class="kpi-value kv3">{lo}</div></div>', unsafe_allow_html=True)
                with k4:
                    hi = f"${max(prices):,}/mo" if prices else "N/A"
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Highest Rent</div><div class="kpi-value kv4">{hi}</div></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="rlabel">Showing <strong>{min(30,len(listings))}</strong> of <strong>{total:,}</strong> rentals in <strong>{location}</strong></div>', unsafe_allow_html=True)

                # Build cards per column
                col_cards = [[], [], []]
                for i, item in enumerate(listings[:30]):
                    prop    = item.get("property", {})
                    addr    = prop.get("address", {})
                    media   = prop.get("media", {})
                    rental  = prop.get("rental", {})

                    street  = addr.get("streetAddress") or ""
                    city_s  = addr.get("city") or ""
                    state_s = addr.get("state") or ""
                    zipcode = addr.get("zipcode") or ""
                    parts   = [p for p in [street, city_s, state_s] if p]
                    full_addr = ", ".join(parts) + (" " + zipcode if zipcode else "")
                    full_addr = full_addr or "Address not available"

                    price_val = prop.get("price", {}).get("value")
                    price_str = f"${int(price_val):,}/mo" if price_val else "Contact for price"
                    rent_est  = prop.get("estimates", {}).get("rentZestimate")
                    beds      = prop.get("bedrooms")
                    baths     = prop.get("bathrooms")
                    sqft      = prop.get("livingArea")
                    prop_type = prop.get("propertyType") or ""
                    days      = prop.get("daysOnZillow")
                    year_built = prop.get("yearBuilt")
                    can_apply  = rental.get("areApplicationsAccepted", False)
                    img = media.get("propertyPhotoLinks", {}).get("highResolutionLink")
                    zpid = prop.get("zpid")
                    link = (f"https://www.zillow.com/homedetails/{zpid}_zpid/"
                            if zpid else "https://www.zillow.com")

                    # Stats
                    stat_parts = []
                    if beds is not None:  stat_parts.append(f"🛏 {int(beds)} bd")
                    if baths is not None: stat_parts.append(f"🚿 {int(baths)} ba")
                    if sqft:              stat_parts.append(f"📐 {int(sqft):,} sqft")
                    stats_html = "  ·  ".join(stat_parts)

                    # Zestimate
                    zest_html = ""
                    if rent_est and price_val:
                        diff = int(price_val) - int(rent_est)
                        if diff < -50:
                            zest_html = f'<span style="color:#10b981;">✓ ${abs(diff):,} below Zillow est. (${int(rent_est):,}/mo)</span>'
                        elif diff > 100:
                            zest_html = f'<span style="color:#f59e0b;">↑ ${diff:,} above Zillow est. (${int(rent_est):,}/mo)</span>'

                    # Badges — all inline styles, no CSS classes
                    badge_parts = []
                    if can_apply:
                        badge_parts.append('<span style="background:#dcfce7;color:#166534;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;margin-right:5px;white-space:nowrap;">✓ Apply Now</span>')
                    if days is not None:
                        badge_parts.append(f'<span style="background:#f1f5f9;color:#475569;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;margin-right:5px;white-space:nowrap;">{int(days)}d listed</span>')
                    if prop_type:
                        clean = (prop_type.replace("singleFamily","Single Family")
                                          .replace("apartment","Apartment")
                                          .replace("condo","Condo")
                                          .replace("townhouse","Townhouse")
                                          .replace("multiFamily","Multi-Family"))
                        badge_parts.append(f'<span style="background:#dbeafe;color:#1e40af;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;margin-right:5px;white-space:nowrap;">{clean}</span>')
                    if year_built:
                        badge_parts.append(f'<span style="background:#ede9fe;color:#6d28d9;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;white-space:nowrap;">Built {year_built}</span>')
                    badges_html = "".join(badge_parts)

                    col_cards[i % 3].append(
                        make_card(img, price_str, full_addr, stats_html, zest_html, badges_html, link)
                    )

                # Render using components.html — bypasses markdown sanitizer completely
                col1, col2, col3 = st.columns(3)
                for ci, col in enumerate([col1, col2, col3]):
                    with col:
                        if col_cards[ci]:
                            html = (
                                "<html><head>"
                                "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap' rel='stylesheet'>"
                                "<style>body{margin:0;padding:4px;background:transparent;}"
                                "a{text-decoration:none;}"
                                "</style></head>"
                                f"<body>{''.join(col_cards[ci])}</body></html>"
                            )
                            components.html(html, height=len(col_cards[ci]) * 430, scrolling=False)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)