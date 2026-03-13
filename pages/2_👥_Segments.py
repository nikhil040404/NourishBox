import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.data import generate_survey_data

st.set_page_config(page_title="Segments — NourishBox", page_icon="🥗", layout="wide")

st.title("👥 Customer Segments")
st.caption("Which customers are most likely to subscribe, and which segment generates the highest revenue potential?")

df = generate_survey_data(100)

# ── Top KPIs ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total respondents",    f"{len(df)}")
k2.metric("Avg health score",     f"{df['Health_Consciousness'].mean():.1f} / 5")
k3.metric("Avg subscription interest", f"{df['Subscription_Interest'].mean():.1f} / 5")
k4.metric("High-intent (≥4)",     f"{(df['Subscription_Interest'] >= 4).sum()} ({(df['Subscription_Interest'] >= 4).mean()*100:.0f}%)")

st.divider()

# ── Charts row 1 ───────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("Subscription interest by occupation")
    occ_avg = df.groupby("Occupation")["Subscription_Interest"].mean().sort_values(ascending=True).reset_index()
    fig = px.bar(occ_avg, x="Subscription_Interest", y="Occupation",
                 orientation="h", color="Subscription_Interest",
                 color_continuous_scale=["#c0dd97","#1D9E75"],
                 labels={"Subscription_Interest": "Avg score (1–5)", "Occupation": ""},
                 range_color=[1, 5])
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0),
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(range=[0, 5])
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Meal preference distribution")
    meal_counts = df["Meal_Preference"].value_counts().reset_index()
    meal_counts.columns = ["Meal", "Count"]
    fig2 = px.pie(meal_counts, names="Meal", values="Count", hole=0.55,
                  color_discrete_sequence=["#1D9E75","#3266ad","#EF9F27","#7F77DD","#E24B4A"])
    fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), showlegend=True,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts row 2 ───────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("Health consciousness distribution")
    hc = df["Health_Consciousness"].value_counts().sort_index().reset_index()
    hc.columns = ["Score", "Count"]
    fig3 = px.bar(hc, x="Score", y="Count",
                  color="Score", color_continuous_scale=["#c0dd97","#1D9E75"],
                  labels={"Score": "Score (1–5)", "Count": "Number of respondents"})
    fig3.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Health score vs subscription interest")
    fig4 = px.scatter(df, x="Health_Consciousness", y="Subscription_Interest",
                      color="Occupation", size_max=10,
                      opacity=0.7,
                      labels={"Health_Consciousness": "Health consciousness (1–5)",
                              "Subscription_Interest": "Subscription interest (1–5)"},
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig4.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Correlation analysis ───────────────────────────────────────────────────────
st.subheader("Correlation with subscription interest")
st.caption("How strongly each variable predicts willingness to subscribe")

score_map = {
    "Age":               {"Under 22": 1, "22–28": 2, "29–35": 3, "36–45": 4, "46 and above": 5},
    "Order_Frequency":   {"Rarely": 1, "1–2 times/week": 2, "3–4 times/week": 3, "5–6 times/week": 4, "Daily": 5},
    "Fitness_Level":     {"Sedentary": 1, "Lightly active": 2, "Moderately active": 3, "Very active": 4},
    "Income":            {"Below ₹30,000": 1, "₹30,000–₹60,000": 2, "₹60,000–₹1,00,000": 3,
                          "₹1,00,000–₹1,50,000": 4, "Above ₹1,50,000": 5},
    "Monthly_Food_Spend":{"Below ₹1,000": 1, "₹1,000–₹2,500": 2, "₹2,500–₹4,000": 3,
                          "₹4,000–₹6,000": 4, "Above ₹6,000": 5},
}
df_num = df.copy()
for col, mapping in score_map.items():
    df_num[col] = df_num[col].map(mapping)

numeric_cols = ["Health_Consciousness", "Fitness_Level", "Monthly_Food_Spend",
                "Order_Frequency", "Income", "Age"]
corr_data = []
for col in numeric_cols:
    val = df_num[col].corr(df_num["Subscription_Interest"])
    corr_data.append({"Variable": col.replace("_", " "), "Correlation": round(val, 2)})

corr_df = pd.DataFrame(corr_data).sort_values("Correlation", ascending=True)
fig_corr = px.bar(corr_df, x="Correlation", y="Variable", orientation="h",
                  color="Correlation", color_continuous_scale=["#c0dd97","#1D9E75"],
                  range_color=[0, 1],
                  labels={"Correlation": "Pearson r", "Variable": ""})
fig_corr.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
fig_corr.update_xaxes(range=[0, 1])
st.plotly_chart(fig_corr, use_container_width=True)

st.divider()

# ── Raw data table ─────────────────────────────────────────────────────────────
with st.expander("View raw survey data (100 participants)"):
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "nourishbox_survey_data.csv", "text/csv")
