
import streamlit as st
import pandas as pd

# Load the dataset
equipment_df = pd.read_excel(r"C:\Users\satya\OneDrive\Desktop\gym_equipment_master_dataset.xlsx")

equipment_df.columns = [col.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for col in equipment_df.columns]
print("Original columns:", equipment_df.columns.tolist())  # Debug print
def recommend_equipment(user_row, equipment_df):
    age = int(user_row['age'])
    gender = user_row['gender']
    fitness_goals = [x.strip().lower() for x in user_row['fitness_goal'].split(",")]
    health_conditions = [x.strip().lower() for x in user_row['health_conditions'].split(",")]
    budget_min = int(user_row['budget_min'])
    budget_max = int(user_row['budget_max'])
    impact_preference = user_row['impact_preference'].lower()

    def is_goal_match(eq_goals):
        eq_goals_list = [x.strip().lower() for x in str(eq_goals).split(",")]
        return any(goal in eq_goals_list for goal in fitness_goals)

    def is_health_condition_match(eq_conditions):
        eq_conditions_lower = str(eq_conditions).lower()
        return any(cond.split()[0] in eq_conditions_lower for cond in health_conditions)

    def is_age_suitable(age_range):
        try:
            if "+" in age_range:
                return age >= int(age_range.replace("+", ""))
            elif "-" in age_range:
                min_age, max_age = map(int, age_range.split("-"))
                return min_age <= age <= max_age
        except:
            return True
        return True

    def is_price_in_budget(price_range):
        try:
            price_range = price_range.replace("–", "-").replace("—", "-")
            min_price, max_price = map(int, price_range.split("-"))
            return budget_min <= max_price and budget_max >= min_price
        except:
            return True

    def is_impact_match(level):
        return str(level).lower() == impact_preference

    # Step 1: Goal Matching
    step1 = equipment_df[equipment_df['target_goals'].apply(is_goal_match)].copy()
    print(f"\nAfter Goal Filter ({len(step1)} items):")  # Fixed missing parenthesis
    print(step1[['equipment_name', 'target_goals']].head())

    # Step 2: Health Conditions
    if 'none' not in [h.lower() for h in health_conditions]:
        step2 = step1[step1['suitable_health_conditions'].apply(is_health_condition_match)].copy()
    else:
        step2 = step1.copy()
    print(f"\nAfter Health Filter ({len(step2)} items):")
    print(step2[['equipment_name', 'suitable_health_conditions']].head())

    # Step 3: Age Group
    step3 = step2[step2['suitable_age_group'].apply(is_age_suitable)].copy()
    print(f"\nAfter Age Filter ({len(step3)} items):")
    print(step3[['equipment_name', 'suitable_age_group']].head())

    # Step 4: Budget
    step4 = step3[step3['price_range_inr'].apply(is_price_in_budget)].copy()
    print(f"\nAfter Budget Filter ({len(step4)} items):")
    print(step4[['equipment_name', 'price_range_inr']].head())

    # Step 5: Impact Level
    step5 = step4[step4['impact_level'].str.lower() == impact_preference].copy()
    print(f"\nAfter Impact Filter ({len(step5)} items):")
    print(step5[['equipment_name', 'impact_level']].head())

    return step5[['equipment_name', 'target_goals', 'price_range_inr', 'impact_level', 'equipment_type']]
st.title("Smart Gym Equipment Recommender")
st.write("Fill the form below to get your personalized gym equipment recommendations!")

with st.form("user_input_form"):
    age = st.number_input("Age", min_value=10, max_value=100, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    fitness_goal = st.multiselect("Fitness Goals", ["Fat Loss", "Muscle Gain", "Rehab", "Senior Fitness", "Endurance", "Flexibility"])
    health_conditions = st.multiselect("Health Conditions", ["Knee Pain", "Back Pain", "Heart Condition", "None"])
    budget_min = st.number_input("Budget Min (INR)", value=5000)
    budget_max = st.number_input("Budget Max (INR)", value=30000)
    impact_pref = st.selectbox("Impact Preference", ["Low", "Medium", "High"])

    submitted = st.form_submit_button("Get Recommendations")

if submitted:
    user_input = {
        'age': age,
        'gender': gender,
        'fitness_goal': ", ".join(fitness_goal),
        'health_conditions': ", ".join(health_conditions),
        'budget_min': budget_min,
        'budget_max': budget_max,
        'impact_preference': impact_pref
    }

    user_df = pd.DataFrame([user_input])
    recommendations = recommend_equipment(user_df.iloc[0], equipment_df)

    if not recommendations.empty:
        st.subheader("Recommended Equipment:")
        for _, row in recommendations.iterrows():
            st.markdown(f"""
            **{row['equipment_name']}**
            - Target Goals: {row['target_goals']}
            - Price Range: {row['price_range_inr']}
            - Impact Level: {row['impact_level']}
            - Equipment Type: {row['equipment_type']}
            """)
    else:
        st.warning("No matching equipment found for the selected inputs.")
