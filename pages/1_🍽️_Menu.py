import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.data import MENU_ITEMS, SUBSCRIPTION_PLANS

st.set_page_config(page_title="Menu — NourishBox", page_icon="🥗", layout="wide")

st.title("🍽️ Our Menu")
st.caption("Every meal is nutritionist-verified. Calories, protein, fat, and carbs shown upfront.")

# ── Filters ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 2])
with col1:
    category_filter = st.selectbox(
        "Filter by category",
        ["All", "High-Protein", "Keto", "Vegan", "Low-Calorie"]
    )
with col2:
    max_cal = st.slider("Max calories per meal", 200, 600, 600, step=10)

df = pd.DataFrame(MENU_ITEMS)
filtered = df.copy()
if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]
filtered = filtered[filtered["calories"] <= max_cal]

st.markdown(f"**{len(filtered)} meals** match your filters")
st.divider()

# ── Meal cards ─────────────────────────────────────────────────────────────────
category_colors = {
    "High-Protein": "#e1f5ee",
    "Keto":         "#faeeda",
    "Vegan":        "#eaf3de",
    "Low-Calorie":  "#e6f1fb",
}

for i in range(0, len(filtered), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(filtered):
            row = filtered.iloc[i + j]
            bg  = category_colors.get(row["category"], "#f8f8f8")
            with col:
                st.markdown(f"""
                <div style="background:{bg};border-radius:10px;padding:1rem;margin-bottom:0.5rem;">
                  <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;
                              letter-spacing:0.05em;color:#444;margin-bottom:6px;">
                    {row['category']}
                  </div>
                  <div style="font-size:1rem;font-weight:600;color:#111;margin-bottom:8px;">
                    {row['name']}
                  </div>
                  <div style="display:flex;gap:10px;font-size:0.78rem;color:#555;margin-bottom:8px;">
                    <span>🔥 {row['calories']} kcal</span>
                    <span>💪 {row['protein']}g protein</span>
                  </div>
                  <div style="display:flex;gap:10px;font-size:0.75rem;color:#777;margin-bottom:10px;">
                    <span>Carbs: {row['carbs']}g</span>
                    <span>Fat: {row['fat']}g</span>
                  </div>
                  <div style="font-size:1rem;font-weight:600;color:#0f6e56;">₹{row['price']}</div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ── Subscription Plans ─────────────────────────────────────────────────────────
st.subheader("📦 Subscription Plans")
st.caption("Subscribe weekly or monthly. Pause, skip, or cancel anytime.")

plan_cols = st.columns(3)
for col, plan in zip(plan_cols, SUBSCRIPTION_PLANS):
    with col:
        is_popular = plan["name"] == "Complete"
        border = "2px solid #1D9E75" if is_popular else "1px solid #ddd"
        badge  = '<div style="background:#e1f5ee;color:#085041;font-size:0.7rem;font-weight:600;padding:3px 10px;border-radius:4px;display:inline-block;margin-bottom:8px;">Most popular</div>' if is_popular else ""
        st.markdown(f"""
        <div style="border:{border};border-radius:12px;padding:1.2rem;text-align:center;">
          {badge}
          <div style="font-size:1.1rem;font-weight:600;color:#111;">{plan['name']}</div>
          <div style="font-size:0.8rem;color:#666;margin:6px 0 10px;">{plan['description']}</div>
          <div style="font-size:1.4rem;font-weight:700;color:#0f6e56;">₹{plan['price_per_month']:,}</div>
          <div style="font-size:0.72rem;color:#888;margin-bottom:10px;">per month</div>
          <div style="font-size:0.8rem;color:#555;">
            {plan['meals_per_week']} meals/week &nbsp;·&nbsp; {plan['diet_options']} diet options
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
