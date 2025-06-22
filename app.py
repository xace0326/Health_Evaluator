import streamlit as st
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# === Define Fuzzy Variables ===
calories = ctrl.Antecedent(np.arange(1000, 4001, 1), 'calories')
exercise = ctrl.Antecedent(np.arange(0, 181, 1), 'exercise')
sleep = ctrl.Antecedent(np.arange(0, 13, 0.5), 'sleep')
wintensity = ctrl.Antecedent(np.arange(0, 11, 1), 'wintensity')
wellness = ctrl.Consequent(np.arange(0, 101, 1), 'wellness')

# === Membership Functions ===
calories['very_low'] = fuzz.gaussmf(calories.universe, 1000, 200)
calories['low'] = fuzz.gaussmf(calories.universe, 1600, 250)
calories['medium'] = fuzz.gaussmf(calories.universe, 2200, 250)
calories['high'] = fuzz.gaussmf(calories.universe, 2800, 250)
calories['very_high'] = fuzz.gaussmf(calories.universe, 4000, 200)

exercise['very_low'] = fuzz.gaussmf(exercise.universe, 0, 15)
exercise['low'] = fuzz.gaussmf(exercise.universe, 30, 20)
exercise['medium'] = fuzz.gaussmf(exercise.universe, 60, 20)
exercise['high'] = fuzz.gaussmf(exercise.universe, 120, 25)
exercise['very_high'] = fuzz.gaussmf(exercise.universe, 180, 25)

sleep['very_low'] = fuzz.gaussmf(sleep.universe, 0, 1.5)
sleep['low'] = fuzz.gaussmf(sleep.universe, 2.5, 1.25)
sleep['medium'] = fuzz.gaussmf(sleep.universe, 6.5, 1)
sleep['high'] = fuzz.gaussmf(sleep.universe, 9, 1.25)
sleep['very_high'] = fuzz.gaussmf(sleep.universe, 12, 1.5)

wintensity['low'] = fuzz.gaussmf(wintensity.universe, 0, 1.5)
wintensity['medium'] = fuzz.gaussmf(wintensity.universe, 5, 1.25)
wintensity['high'] = fuzz.gaussmf(wintensity.universe, 10, 1.5)

wellness['poor'] = fuzz.gaussmf(wellness.universe, 0, 10)
wellness['below_avg'] = fuzz.gaussmf(wellness.universe, 35, 7.5)
wellness['average'] = fuzz.gaussmf(wellness.universe, 55, 5)
wellness['good'] = fuzz.gaussmf(wellness.universe, 75, 6.25)
wellness['excellent'] = fuzz.gaussmf(wellness.universe, 100, 7.5)

# === Fuzzy Rules ===
rules = [
    ctrl.Rule(calories['high'] & exercise['high'] & sleep['high'] & wintensity['high'], wellness['excellent']),
    ctrl.Rule(calories['medium'] & exercise['medium'] & sleep['medium'] & wintensity['medium'], wellness['good']),
    ctrl.Rule(calories['low'] & exercise['low'] & sleep['low'] & wintensity['low'], wellness['poor']),
    ctrl.Rule(sleep['high'] & calories['low'], wellness['average']),
    ctrl.Rule(exercise['high'] & sleep['low'], wellness['below_avg'])
]

wellness_ctrl = ctrl.ControlSystem(rules)
wellness_sim = ctrl.ControlSystemSimulation(wellness_ctrl)

# === Streamlit UI ===
st.set_page_config(page_title="Fuzzy Health Evaluator", layout="centered")
st.title("💪 Fuzzy Logic Health Evaluator")
st.markdown("""Enter your lifestyle details and let fuzzy logic estimate your wellness score!""")

# === Input Selections ===
cal_level = st.selectbox("Calories Intake Level", ['very_low', 'low', 'medium', 'high', 'very_high'])
calories_input = np.random.uniform(*{
    'very_low': (1000, 1300),
    'low': (1400, 1800),
    'medium': (2000, 2500),
    'high': (2600, 3200),
    'very_high': (3300, 4000)
}[cal_level])

exercise_input = st.slider("Exercise Duration (minutes)", 0, 180, 60)
sleep_input = st.slider("Sleep Hours", 0.0, 12.0, 7.0, step=0.5)

intensity_level = st.selectbox("Workout Intensity Level", ['low', 'medium', 'high'])
wintensity_input = np.random.uniform(*{
    'low': (0.0, 3.5),
    'medium': (3.5, 6.5),
    'high': (6.5, 10.0)
}[intensity_level])

if st.button("Evaluate My Wellness"):
    wellness_sim.input['calories'] = calories_input
    wellness_sim.input['exercise'] = exercise_input
    wellness_sim.input['sleep'] = sleep_input
    wellness_sim.input['wintensity'] = wintensity_input
    wellness_sim.compute()

    score = wellness_sim.output['wellness']
    st.subheader(f"🧠 Estimated Wellness Score: {score:.2f} / 100")

    # === Recommendation ===
    recs = []
    if calories_input < 2000:
        recs.append("🔹 Eat more — your calorie intake is on the lower side.")
    elif calories_input > 3000:
        recs.append("🔹 Watch your calorie intake — might be too high.")
    if exercise_input < 30:
        recs.append("🔹 Try to exercise more regularly.")
    elif exercise_input > 120:
        recs.append("🔹 Don't forget to rest — exercise duration is very high.")
    if sleep_input < 6:
        recs.append("🔹 Sleep more — 7-9 hours is ideal.")
    if wintensity_input < 4:
        recs.append("🔹 Increase workout intensity gradually.")
    elif wintensity_input > 8:
        recs.append("🔹 Avoid overtraining — your intensity is very high.")

    if not recs:
        recs.append("✅ Great job! Your lifestyle is well-balanced.")

    st.markdown("### 💡 Recommendations")
    for r in recs:
        st.write(r)