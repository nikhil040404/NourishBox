import streamlit as st

st.set_page_config(
    page_title="NourishBox — Healthy Cloud Kitchen",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebarNav"] { font-size: 0.9rem; }
  .metric-card {
    background: #f8fdf9;
    border: 1px solid #c3e6cb;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
  }
  .section-tag {
    display: inline-block;
    background: #e1f5ee;
    color: #085041;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 3px 10px;
    border-radius: 4px;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
  }
  .pill {
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 3px;
    color: #555;
  }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-tag">Cloud Kitchen Concept</div>', unsafe_allow_html=True)
st.title("🥗 NourishBox")
st.subheader("Healthy meals for urban professionals — delivered.")

st.markdown("""
A delivery-only cloud kitchen serving nutritionally balanced meals to time-pressed professionals.  
No dine-in. No compromise on health. Just great food, on a schedule that fits your life.
""")

pills = ["Delivery-only model", "Subscription-first", "Data-driven menus",
         "Urban professionals", "Nutritionist-approved"]
st.markdown(" ".join(f'<span class="pill">{p}</span>' for p in pills), unsafe_allow_html=True)

st.divider()

# ── The Problem ────────────────────────────────────────────────────────────────
st.subheader("The Problem")
col1, col2, col3 = st.columns(3)
with col1:
    st.error("⏰ **No time to cook**\n\nUrban professionals work 9–11 hours daily. Meal planning is simply not feasible on weekdays.")
with col2:
    st.error("🍔 **Unhealthy delivery options**\n\nZomato & Swiggy list thousands of restaurants — but nutrition-first options are buried and unverified.")
with col3:
    st.error("📉 **No consistency or trust**\n\nHealthy restaurants vary by day and chef. No reliable nutrition labelling. No routine possible.")

st.divider()

# ── The Solution ───────────────────────────────────────────────────────────────
st.subheader("The Solution")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("🏭 **Cloud Kitchen Model**\nZero dine-in costs. Better ingredients at a competitive price.")
with col2:
    st.success("📦 **Subscription Delivery**\nWeekly & monthly meal plans. Predictable revenue, reduced waste.")
with col3:
    st.success("🥦 **Nutritionist-Designed**\nEvery meal calorie-counted, macro-balanced, diet-filtered.")
with col4:
    st.success("📊 **Data-Driven**\nOrder history & survey data power smarter meal recommendations.")

st.divider()

# ── Key Metrics ────────────────────────────────────────────────────────────────
st.subheader("Business Model at a Glance")
m1, m2, m3, m4, m5, m6 = st.columns(6)
metrics = [
    ("Primary Revenue", "Subscriptions"),
    ("Target Margin", "58–65%"),
    ("Phase 1 City", "Bengaluru"),
    ("Target Market", "2.4M users"),
    ("Break-even", "14–18 months"),
    ("Avg Sub Value", "₹5,800/mo"),
]
for col, (label, val) in zip([m1, m2, m3, m4, m5, m6], metrics):
    with col:
        st.metric(label, val)

st.divider()

# ── Navigation hint ────────────────────────────────────────────────────────────
st.info("👈 Use the sidebar to explore: **Menu**, **Customer Segments**, **Survey**, **Dashboard**, and **Analytics**.")
