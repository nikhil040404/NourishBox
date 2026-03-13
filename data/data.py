import pandas as pd
import numpy as np

def generate_survey_data(n=100, seed=42):
    np.random.seed(seed)

    ages         = ["Under 22","22–28","29–35","36–45","46 and above"]
    age_w        = [0.08, 0.35, 0.30, 0.20, 0.07]

    genders      = ["Male","Female","Non-binary","Prefer not to say"]
    gender_w     = [0.48, 0.46, 0.04, 0.02]

    occupations  = ["Tech / IT","Finance / Consulting","Healthcare","Education","Business / Entrepreneur","Other"]
    occ_w        = [0.30, 0.22, 0.15, 0.10, 0.13, 0.10]

    incomes      = ["Below ₹30,000","₹30,000–₹60,000","₹60,000–₹1,00,000","₹1,00,000–₹1,50,000","Above ₹1,50,000"]
    income_w     = [0.10, 0.25, 0.32, 0.20, 0.13]

    frequencies  = ["Rarely","1–2 times/week","3–4 times/week","5–6 times/week","Daily"]
    freq_w       = [0.10, 0.25, 0.30, 0.22, 0.13]

    meal_prefs   = ["High-protein lunch bowls","Low-calorie dinner meals","Keto meal plan","Vegan meal plan","Balanced mixed meals"]
    meal_w       = [0.30, 0.18, 0.22, 0.15, 0.15]

    price_ranges = ["Below ₹150","₹150–₹250","₹250–₹350","₹350–₹500","Above ₹500"]
    price_w      = [0.08, 0.22, 0.38, 0.22, 0.10]

    diet_types   = ["No specific diet","High-protein","Keto","Vegan","Low-calorie","Balanced"]
    diet_w       = [0.20, 0.25, 0.18, 0.12, 0.15, 0.10]

    fitness_lvls = ["Sedentary","Lightly active","Moderately active","Very active"]
    fitness_w    = [0.15, 0.30, 0.35, 0.20]

    food_spends  = ["Below ₹1,000","₹1,000–₹2,500","₹2,500–₹4,000","₹4,000–₹6,000","Above ₹6,000"]
    spend_w      = [0.08, 0.22, 0.30, 0.25, 0.15]

    health_scores = np.random.choice([1,2,3,4,5], n, p=[0.05,0.10,0.20,0.35,0.30])
    sub_scores    = np.clip(health_scores + np.random.randint(-1, 2, n), 1, 5)

    rows = []
    for i in range(n):
        rows.append({
            "Participant_ID":        f"P{str(i+1).zfill(3)}",
            "Age":                   np.random.choice(ages, p=age_w),
            "Gender":                np.random.choice(genders, p=gender_w),
            "Occupation":            np.random.choice(occupations, p=occ_w),
            "Income":                np.random.choice(incomes, p=income_w),
            "Order_Frequency":       np.random.choice(frequencies, p=freq_w),
            "Health_Consciousness":  int(health_scores[i]),
            "Meal_Preference":       np.random.choice(meal_prefs, p=meal_w),
            "Price_Range":           np.random.choice(price_ranges, p=price_w),
            "Subscription_Interest": int(sub_scores[i]),
            "Fitness_Level":         np.random.choice(fitness_lvls, p=fitness_w),
            "Diet_Type":             np.random.choice(diet_types, p=diet_w),
            "Monthly_Food_Spend":    np.random.choice(food_spends, p=spend_w),
        })

    return pd.DataFrame(rows)


MENU_ITEMS = [
    {"name": "High-Protein Chicken Bowl",   "category": "High-Protein", "diet": "High-protein", "calories": 480, "protein": 42, "carbs": 35, "fat": 12, "price": 299},
    {"name": "Paneer Power Bowl",            "category": "High-Protein", "diet": "Vegan",        "calories": 440, "protein": 32, "carbs": 38, "fat": 14, "price": 279},
    {"name": "Egg White Oats Bowl",          "category": "High-Protein", "diet": "High-protein", "calories": 390, "protein": 36, "carbs": 42, "fat": 8,  "price": 249},
    {"name": "Keto Grilled Salmon",          "category": "Keto",         "diet": "Keto",         "calories": 520, "protein": 38, "carbs": 6,  "fat": 34, "price": 349},
    {"name": "Keto Avocado Egg Platter",     "category": "Keto",         "diet": "Keto",         "calories": 460, "protein": 22, "carbs": 8,  "fat": 38, "price": 319},
    {"name": "Keto Chicken Lettuce Wraps",   "category": "Keto",         "diet": "Keto",         "calories": 410, "protein": 34, "carbs": 7,  "fat": 28, "price": 299},
    {"name": "Vegan Buddha Bowl",            "category": "Vegan",        "diet": "Vegan",        "calories": 420, "protein": 18, "carbs": 58, "fat": 12, "price": 269},
    {"name": "Tofu Stir-Fry & Quinoa",       "category": "Vegan",        "diet": "Vegan",        "calories": 390, "protein": 20, "carbs": 52, "fat": 10, "price": 259},
    {"name": "Chickpea & Greens Salad",      "category": "Vegan",        "diet": "Vegan",        "calories": 340, "protein": 16, "carbs": 45, "fat": 9,  "price": 239},
    {"name": "Low-Cal Grilled Chicken Salad","category": "Low-Calorie",  "diet": "Low-calorie",  "calories": 320, "protein": 30, "carbs": 22, "fat": 8,  "price": 259},
    {"name": "Zucchini Pasta & Veggies",     "category": "Low-Calorie",  "diet": "Low-calorie",  "calories": 290, "protein": 14, "carbs": 38, "fat": 7,  "price": 229},
    {"name": "Miso Soup & Brown Rice Bowl",  "category": "Low-Calorie",  "diet": "Low-calorie",  "calories": 310, "protein": 12, "carbs": 44, "fat": 6,  "price": 219},
]

SUBSCRIPTION_PLANS = [
    {"name": "Starter",    "meals_per_week": 5,  "price_per_week": 1299, "price_per_month": 4999,  "diet_options": 2, "description": "5 lunches per week. Perfect for the weekday professional."},
    {"name": "Complete",   "meals_per_week": 10, "price_per_week": 2199, "price_per_month": 7999,  "diet_options": 4, "description": "Lunch + dinner, 5 days. Full weekday nutrition covered."},
    {"name": "Elite",      "meals_per_week": 14, "price_per_week": 2999, "price_per_month": 10999, "diet_options": 6, "description": "All 7 days, lunch + dinner. Maximum health commitment."},
]
