import streamlit as st
import pandas as pd
import os, json
from datetime import datetime

st.set_page_config(page_title="Survey — NourishBox", page_icon="🥗", layout="wide")

RESPONSES_FILE = "survey_responses.json"

def load_responses():
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r") as f:
            return json.load(f)
    return []

def save_response(entry):
    responses = load_responses()
    responses.append(entry)
    with open(RESPONSES_FILE, "w") as f:
        json.dump(responses, f, indent=2)

# ──────────────────────────────────────────────────────────────────────────────
st.title("📋 Customer Survey")
st.caption("Help us understand your meal preferences and health goals. Takes under 2 minutes.")

progress = st.progress(0)
st.divider()

with st.form("survey_form", clear_on_submit=True):
    st.subheader("About you")
    col1, col2 = st.columns(2)

    with col1:
        q1 = st.selectbox(
            "Q1 — What is your age group?  `Age`",
            ["", "Under 22", "22–28", "29–35", "36–45", "46 and above"]
        )
        q3 = st.selectbox(
            "Q3 — Which best describes your occupation?  `Occupation`",
            ["", "Tech / IT", "Finance / Consulting", "Healthcare",
             "Education", "Business / Entrepreneur", "Other"]
        )
        q5 = st.selectbox(
            "Q5 — How often do you order food online per week?  `Order_Frequency`",
            ["", "Rarely (once or less)", "1–2 times", "3–4 times", "5–6 times", "Daily"]
        )

    with col2:
        q2 = st.selectbox(
            "Q2 — How do you identify?  `Gender`",
            ["", "Male", "Female", "Non-binary", "Prefer not to say"]
        )
        q4 = st.selectbox(
            "Q4 — Approximate monthly personal income  `Income`",
            ["", "Below ₹30,000", "₹30,000–₹60,000", "₹60,000–₹1,00,000",
             "₹1,00,000–₹1,50,000", "Above ₹1,50,000"]
        )
        q12 = st.selectbox(
            "Q6 — How much do you spend monthly on food delivery?  `Monthly_Food_Spend`",
            ["", "Below ₹1,000", "₹1,000–₹2,500", "₹2,500–₹4,000",
             "₹4,000–₹6,000", "Above ₹6,000"]
        )

    st.divider()
    st.subheader("Health & food preferences")
    col3, col4 = st.columns(2)

    with col3:
        q6 = st.slider(
            "Q7 — How important is healthy eating to you?  `Health_Consciousness`",
            1, 5, 3,
            help="1 = Not important · 5 = Extremely important"
        )
        q7 = st.selectbox(
            "Q8 — Which type of meal would you most prefer?  `Meal_Preference`",
            ["", "High-protein lunch bowls", "Low-calorie dinner meals",
             "Keto meal plan", "Vegan meal plan", "Balanced mixed meals"]
        )
        q11 = st.selectbox(
            "Q9 — What is your preferred diet type?  `Diet_Type`",
            ["", "No specific diet", "High-protein", "Keto",
             "Vegan", "Low-calorie", "Balanced"]
        )

    with col4:
        q8 = st.selectbox(
            "Q10 — Preferred price per healthy meal  `Price_Range`",
            ["", "Below ₹150", "₹150–₹250", "₹250–₹350", "₹350–₹500", "Above ₹500"]
        )
        q9 = st.slider(
            "Q11 — How interested are you in a weekly healthy meal subscription?  `Subscription_Interest`",
            1, 5, 3,
            help="1 = Not interested · 5 = Very interested"
        )
        q10 = st.selectbox(
            "Q12 — How would you describe your fitness activity level?  `Fitness_Level`",
            ["", "Sedentary", "Lightly active", "Moderately active", "Very active"]
        )

    st.divider()
    submitted = st.form_submit_button("Submit my responses", type="primary", use_container_width=True)

    if submitted:
        required = [q1, q2, q3, q4, q5, q7, q8, q10, q11, q12]
        if any(v == "" for v in required):
            st.error("Please answer all questions before submitting.")
        else:
            entry = {
                "timestamp":             datetime.now().isoformat(),
                "Age":                   q1,
                "Gender":                q2,
                "Occupation":            q3,
                "Income":                q4,
                "Order_Frequency":       q5,
                "Health_Consciousness":  q6,
                "Meal_Preference":       q7,
                "Price_Range":           q8,
                "Subscription_Interest": q9,
                "Fitness_Level":         q10,
                "Diet_Type":             q11,
                "Monthly_Food_Spend":    q12,
            }
            save_response(entry)
            st.success("✅ Thank you! Your response has been recorded.")
            st.balloons()

# ── Responses viewer ───────────────────────────────────────────────────────────
st.divider()
responses = load_responses()
if responses:
    st.subheader(f"📊 Collected responses: {len(responses)}")
    df_resp = pd.DataFrame(responses)
    if "timestamp" in df_resp.columns:
        df_resp = df_resp.drop(columns=["timestamp"])
    st.dataframe(df_resp, use_container_width=True)
    csv = df_resp.to_csv(index=False).encode("utf-8")
    st.download_button("Download responses CSV", csv, "live_responses.csv", "text/csv")
else:
    st.info("No responses collected yet. Be the first to submit!")
