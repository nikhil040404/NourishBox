import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.data import generate_survey_data

st.set_page_config(page_title="Analytics — NourishBox", page_icon="🥗", layout="wide")

st.title("🔬 Predictive Analytics")
st.caption("ML-based subscription prediction using survey data — which customers are most likely to subscribe?")

df = generate_survey_data(100)

# ── Encode features ────────────────────────────────────────────────────────────
encode_maps = {
    "Age":            {"Under 22": 1, "22–28": 2, "29–35": 3, "36–45": 4, "46 and above": 5},
    "Order_Frequency":{"Rarely": 1, "1–2 times/week": 2, "3–4 times/week": 3, "5–6 times/week": 4, "Daily": 5},
    "Fitness_Level":  {"Sedentary": 1, "Lightly active": 2, "Moderately active": 3, "Very active": 4},
    "Income":         {"Below ₹30,000": 1, "₹30,000–₹60,000": 2, "₹60,000–₹1,00,000": 3,
                       "₹1,00,000–₹1,50,000": 4, "Above ₹1,50,000": 5},
    "Monthly_Food_Spend": {"Below ₹1,000": 1, "₹1,000–₹2,500": 2, "₹2,500–₹4,000": 3,
                           "₹4,000–₹6,000": 4, "Above ₹6,000": 5},
}
df_enc = df.copy()
for col, mapping in encode_maps.items():
    df_enc[col] = df_enc[col].map(mapping)

# binary target
df_enc["High_Intent"] = (df_enc["Subscription_Interest"] >= 4).astype(int)

feature_cols = ["Health_Consciousness", "Fitness_Level", "Monthly_Food_Spend",
                "Order_Frequency", "Income", "Age"]

# ── Simple logistic regression (pure numpy, no sklearn required) ───────────────
X_raw = df_enc[feature_cols].values.astype(float)
X_mean, X_std = X_raw.mean(0), X_raw.std(0) + 1e-8
X = (X_raw - X_mean) / X_std
y = df_enc["High_Intent"].values.astype(float)

# gradient descent
w = np.zeros(X.shape[1])
b = 0.0
lr = 0.05
for _ in range(2000):
    z    = X @ w + b
    pred = 1 / (1 + np.exp(-z))
    dw   = X.T @ (pred - y) / len(y)
    db   = (pred - y).mean()
    w   -= lr * dw
    b   -= lr * db

probs     = 1 / (1 + np.exp(-(X @ w + b)))
predicted = (probs >= 0.5).astype(int)
accuracy  = (predicted == y).mean()

# feature importance via abs(w * std)
importance = np.abs(w)
imp_df = pd.DataFrame({
    "Feature":    [c.replace("_", " ") for c in feature_cols],
    "Importance": importance,
}).sort_values("Importance", ascending=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Model accuracy",       f"{accuracy*100:.1f}%")
k2.metric("High-intent predicted",f"{predicted.sum()}")
k3.metric("Precision",            f"{(predicted & y.astype(int)).sum() / max(predicted.sum(),1):.2f}")
k4.metric("Recall",               f"{(predicted & y.astype(int)).sum() / max(y.sum(),1):.2f}")

st.info("Model: Logistic Regression (gradient descent). Features are standardised. Target = Subscription_Interest ≥ 4.")
st.divider()

# ── Feature importance ─────────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    st.subheader("Feature importance")
    fig = px.bar(imp_df, x="Importance", y="Feature", orientation="h",
                 color="Importance", color_continuous_scale=["#c0dd97","#1D9E75"])
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0),
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Predicted probability distribution")
    fig2 = px.histogram(x=probs, nbins=20, color_discrete_sequence=["#1D9E75"],
                        labels={"x": "Predicted subscription probability"})
    fig2.add_vline(x=0.5, line_dash="dash", line_color="#E24B4A", annotation_text="Threshold")
    fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Participant scoring table ──────────────────────────────────────────────────
st.subheader("Participant subscription scores")
df_scored = df.copy()
df_scored["Sub_Probability"] = probs.round(3)
df_scored["Prediction"]      = np.where(predicted == 1, "High intent", "Low intent")
df_scored["Actual"]          = np.where(y == 1, "High intent", "Low intent")
df_scored = df_scored.sort_values("Sub_Probability", ascending=False)

top_n = st.slider("Show top N participants by probability", 5, 100, 20)
st.dataframe(
    df_scored[["Participant_ID","Occupation","Health_Consciousness",
               "Fitness_Level","Sub_Probability","Prediction","Actual"]].head(top_n),
    use_container_width=True, hide_index=True
)

st.divider()

# ── Live predictor ─────────────────────────────────────────────────────────────
st.subheader("🔮 Live subscriber predictor")
st.caption("Enter a customer profile to predict their subscription likelihood.")

lc1, lc2, lc3 = st.columns(3)
with lc1:
    in_health   = st.slider("Health consciousness", 1, 5, 4)
    in_fitness  = st.selectbox("Fitness level", ["Sedentary","Lightly active","Moderately active","Very active"], index=2)
with lc2:
    in_freq     = st.selectbox("Order frequency", ["Rarely","1–2 times/week","3–4 times/week","5–6 times/week","Daily"], index=2)
    in_income   = st.selectbox("Income", ["Below ₹30,000","₹30,000–₹60,000","₹60,000–₹1,00,000","₹1,00,000–₹1,50,000","Above ₹1,50,000"], index=2)
with lc3:
    in_spend    = st.selectbox("Monthly food spend", ["Below ₹1,000","₹1,000–₹2,500","₹2,500–₹4,000","₹4,000–₹6,000","Above ₹6,000"], index=2)
    in_age      = st.selectbox("Age group", ["Under 22","22–28","29–35","36–45","46 and above"], index=2)

fitness_map = {"Sedentary":1,"Lightly active":2,"Moderately active":3,"Very active":4}
freq_map    = {"Rarely":1,"1–2 times/week":2,"3–4 times/week":3,"5–6 times/week":4,"Daily":5}
income_map  = {"Below ₹30,000":1,"₹30,000–₹60,000":2,"₹60,000–₹1,00,000":3,"₹1,00,000–₹1,50,000":4,"Above ₹1,50,000":5}
spend_map   = {"Below ₹1,000":1,"₹1,000–₹2,500":2,"₹2,500–₹4,000":3,"₹4,000–₹6,000":4,"Above ₹6,000":5}
age_map     = {"Under 22":1,"22–28":2,"29–35":3,"36–45":4,"46 and above":5}

x_input = np.array([[in_health, fitness_map[in_fitness], spend_map[in_spend],
                      freq_map[in_freq], income_map[in_income], age_map[in_age]]], dtype=float)
x_norm  = (x_input - X_mean) / X_std
prob_in = float(1 / (1 + np.exp(-(x_norm @ w + b))))

col_res, col_gauge = st.columns([1, 2])
with col_res:
    st.metric("Subscription probability", f"{prob_in*100:.1f}%")
    if prob_in >= 0.7:
        st.success("High intent — strong subscription candidate")
    elif prob_in >= 0.4:
        st.warning("Medium intent — nurture with trial offer")
    else:
        st.error("Low intent — not ready for subscription")

with col_gauge:
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob_in * 100, 1),
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar":  {"color": "#1D9E75" if prob_in >= 0.5 else "#E24B4A"},
            "steps":[{"range":[0,40],"color":"#fcebeb"},
                     {"range":[40,70],"color":"#faeeda"},
                     {"range":[70,100],"color":"#e1f5ee"}],
            "threshold":{"line":{"color":"gray","width":2},"value":50},
        }
    ))
    fig_g.update_layout(height=220, margin=dict(l=20,r=20,t=20,b=10),
                        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_g, use_container_width=True)
