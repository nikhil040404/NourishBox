import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Dashboard — NourishBox", page_icon="🥗", layout="wide")

st.title("📊 Business Dashboard")
st.caption("Financial projections and operational metrics for NourishBox — Phase 1 (Bengaluru)")

# ── Projections data ───────────────────────────────────────────────────────────
months = ["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12"]
subscribers  = [30, 60, 100, 145, 195, 250, 310, 370, 430, 490, 550, 620]
revenue      = [s * 5800 for s in subscribers]
cogs         = [r * 0.38 for r in revenue]
gross_profit = [r - c for r, c in zip(revenue, cogs)]
fixed_costs  = [120000] * 12
net          = [g - f for g, f in zip(gross_profit, fixed_costs)]

df_proj = pd.DataFrame({
    "Month":       months,
    "Subscribers": subscribers,
    "Revenue":     revenue,
    "COGS":        cogs,
    "Gross Profit":gross_profit,
    "Fixed Costs": fixed_costs,
    "Net P&L":     net,
})

# ── Assumptions sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("Model assumptions")
    avg_sub_value = st.slider("Avg subscription value (₹/mo)", 3000, 10000, 5800, step=100)
    gross_margin  = st.slider("Gross margin (%)", 40, 75, 62)
    fixed_cost_mo = st.slider("Fixed costs / month (₹)", 50000, 300000, 120000, step=5000)
    starting_subs = st.slider("Starting subscribers (M1)", 10, 100, 30)

    revenue_sim      = [s * avg_sub_value for s in subscribers]
    revenue_sim[0]   = starting_subs * avg_sub_value
    cogs_sim         = [r * (1 - gross_margin / 100) for r in revenue_sim]
    gross_profit_sim = [r - c for r, c in zip(revenue_sim, cogs_sim)]
    net_sim          = [g - fixed_cost_mo for g in gross_profit_sim]

    st.markdown("---")
    breakeven = next((i+1 for i, n in enumerate(net_sim) if n >= 0), None)
    if breakeven:
        st.success(f"Break-even: **Month {breakeven}**")
    else:
        st.warning("Break-even beyond Month 12 — adjust assumptions")

# ── KPI row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Year-1 revenue (projected)", f"₹{sum(revenue_sim)/100000:.1f}L")
k2.metric("Subscribers at M12",         f"{subscribers[-1]}")
k3.metric("Gross margin",               f"{gross_margin}%")
k4.metric("Year-1 net P&L",             f"₹{sum(net_sim)/100000:.1f}L",
          delta="Profit" if sum(net_sim) > 0 else "Loss")

st.divider()

# ── Revenue chart ──────────────────────────────────────────────────────────────
st.subheader("Monthly revenue vs costs")
fig = go.Figure()
fig.add_bar(name="Revenue", x=months, y=revenue_sim,
            marker_color="#1D9E75", opacity=0.85)
fig.add_bar(name="COGS", x=months, y=cogs_sim,
            marker_color="#f0997b", opacity=0.85)
fig.add_bar(name="Fixed costs", x=months, y=[fixed_cost_mo]*12,
            marker_color="#b4b2a9", opacity=0.85)
fig.add_scatter(name="Net P&L", x=months, y=net_sim,
                mode="lines+markers", line=dict(color="#185FA5", width=2),
                marker=dict(size=7))
fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
fig.update_layout(
    barmode="overlay",
    margin=dict(l=0, r=0, t=10, b=0),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", y=1.08),
    yaxis_tickprefix="₹", yaxis_tickformat=",.0f",
)
st.plotly_chart(fig, use_container_width=True)

# ── Subscribers chart ──────────────────────────────────────────────────────────
st.subheader("Subscriber growth")
fig2 = px.area(x=months, y=subscribers,
               labels={"x": "Month", "y": "Active subscribers"},
               color_discrete_sequence=["#1D9E75"])
fig2.update_traces(fillcolor="rgba(29,158,117,0.15)")
fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Segment revenue contribution ───────────────────────────────────────────────
st.subheader("Revenue by customer segment")
seg_data = pd.DataFrame({
    "Segment":   ["Tech/IT", "Health millennials", "Young parents", "Finance", "Healthcare", "Others"],
    "Revenue_K": [34.4, 41.5, 36.1, 21.5, 10.7, 19.1],
    "Sub_likelihood": [84, 79, 61, 58, 54, 38],
})
fig3 = px.scatter(seg_data, x="Sub_likelihood", y="Revenue_K", size="Revenue_K",
                  text="Segment", color="Revenue_K",
                  color_continuous_scale=["#c0dd97","#1D9E75"],
                  labels={"Sub_likelihood": "Subscription likelihood (%)",
                          "Revenue_K": "Revenue potential (₹K/mo)"},
                  size_max=50)
fig3.update_traces(textposition="top center", textfont_size=11)
fig3.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0),
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── P&L summary table ──────────────────────────────────────────────────────────
st.subheader("Monthly P&L summary")
df_display = pd.DataFrame({
    "Month":        months,
    "Subscribers":  subscribers,
    "Revenue (₹)":  [f"₹{r:,.0f}" for r in revenue_sim],
    "COGS (₹)":     [f"₹{c:,.0f}" for c in cogs_sim],
    "Gross Profit": [f"₹{g:,.0f}" for g in gross_profit_sim],
    "Net P&L (₹)":  [f"₹{n:,.0f}" for n in net_sim],
})
st.dataframe(df_display, use_container_width=True, hide_index=True)
