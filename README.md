# 🥗 NourishBox — Healthy Cloud Kitchen App

A Streamlit web app for the NourishBox healthy cloud kitchen concept — serving urban professionals in Indian metro cities with nutritionist-approved, subscription-based meal delivery.

## Live Demo

Deploy instantly on [Streamlit Community Cloud](https://streamlit.io/cloud) (free).

---

## Features

| Page | Description |
|---|---|
| 🏠 Home | Concept overview, problem statement, solution pillars |
| 🍽️ Menu | Filter meals by category, diet type, and calories. View subscription plans. |
| 👥 Segments | Customer segmentation analysis with interactive charts |
| 📋 Survey | Live survey form — collect and download real responses |
| 📊 Dashboard | Financial projections with adjustable assumptions |
| 🔬 Analytics | ML subscription predictor with live customer scoring |

---

## Quickstart (local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/nourishbox.git
cd nourishbox

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repo, branch (`main`), and set **Main file path** to `app.py`
5. Click **Deploy** — your app will be live in ~60 seconds

---

## Project structure

```
nourishbox/
├── app.py                    # Home page
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml           # Theme & server config
├── data/
│   └── data.py               # Dataset generator + menu/plan data
└── pages/
    ├── 1_🍽️_Menu.py          # Menu & subscription plans
    ├── 2_👥_Segments.py       # Customer segmentation charts
    ├── 3_📋_Survey.py         # Live survey form
    ├── 4_📊_Dashboard.py      # Financial dashboard
    └── 5_🔬_Analytics.py      # ML predictor
```

---

## Tech stack

- [Streamlit](https://streamlit.io) — UI framework
- [Pandas](https://pandas.pydata.org) — data manipulation
- [NumPy](https://numpy.org) — numerical computing & logistic regression
- [Plotly](https://plotly.com/python/) — interactive charts

No external APIs. No database required. Fully self-contained.

---

## Customisation

- **Menu items** — edit `data/data.py` → `MENU_ITEMS` list
- **Subscription plans** — edit `data/data.py` → `SUBSCRIPTION_PLANS` list
- **Survey questions** — edit `pages/3_📋_Survey.py`
- **Financial model** — adjust defaults in `pages/4_📊_Dashboard.py`
- **Theme colours** — edit `.streamlit/config.toml`
