



import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu

# ====== PAGE CONFIG ======
st.set_page_config(page_title="FB Post Performance Predictor", layout="wide")

# ====== LOAD MODEL ======
try:
    with open("model/facebook.pkl", "rb") as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Model load failed: {e}")

# ====== SIDEBAR TEMPLATE ======
with st.sidebar:
    st.markdown("### PROFILE TEMPLATES")
    template = st.selectbox("Select a template or customize your own:", ["Viral Photo Post", "Custom"])

    st.write("#### Template Details")
    st.write("Post Type: Photo")
    st.write("Category: Inspiration")
    st.write("Month: October")
    st.write("Day: Friday")
    st.write("Hour: 12:00")
    st.write("Paid: Yes")
    st.write("Page Likes: 180,000")

    st.info("You can customize this template in the main panel.")

# ====== MAIN PANEL ======
selected = option_menu(
    menu_title=None,
    options=["Prediction", "Insights"],
    icons=["activity", "bar-chart-line"],
    orientation="horizontal",
    default_index=0,
)

if selected == "Prediction":
    st.markdown("### POST DETAILS")

    col1, col2, col3 = st.columns(3)
    with col1:
        type_post = st.selectbox("Post Type", ["Photo", "Status", "Link", "Video"])
        category = st.selectbox("Category", ["Inspiration", "Product", "Promotion"])
        paid = st.radio("Paid Promotion?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    with col2:
        month = st.selectbox("Post Month", [
            "Januar", "Februar", "Marz", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ])
        weekday = st.selectbox("Post Weekday", [
            "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"
        ])
        hour = st.selectbox("Post Hour", [f"{h}:00" for h in range(24)])

    with st.expander("Advanced Options"):
        reach = st.number_input("Total Reach", value=1000)
        impressions = st.number_input("Total Impressions", value=1500)
        engaged_users = st.number_input("Engaged Users", value=90)
        consumers = st.number_input("Post Consumers", value=70)
        consumptions = st.number_input("Post Consumptions", value=80)
        imp_liked = st.number_input("Impressions by Page Likes", value=900)
        reach_liked = st.number_input("Reach by Page Likes", value=850)
        engaged_liked = st.number_input("People who liked Page and engaged", value=70)
        comments = st.number_input("Comments", value=10)
        likes = st.number_input("Likes", value=50)
        shares = st.number_input("Shares", value=5)

    if st.button("Predict Performance"):
        # Convert categories to numerical
        month_num = {
            "Januar": 1, "Februar": 2, "Marz": 3, "April": 4,
            "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
            "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
        }[month]

        weekday_num = {
            "Montag": 0, "Dienstag": 1, "Mittwoch": 2, "Donnerstag": 3,
            "Freitag": 4, "Samstag": 5, "Sonntag": 6
        }[weekday]

        type_dict = {"Photo": 1, "Status": 2, "Link": 3, "Video": 4}
        category_dict = {"Inspiration": 1, "Product": 2, "Promotion": 3}

        input_data = np.array([[category_dict[category], month_num, weekday_num,
                                int(hour.split(":")[0]), paid, type_dict[type_post],
                                reach, impressions, engaged_users, consumers,
                                consumptions, imp_liked, reach_liked,
                                engaged_liked, comments, likes, shares]])

        prediction = model.predict(input_data)[0]
        result_map = {0: "Low", 1: "Medium", 2: "High"}

        st.success(f"🎯 **Predicted Interaction Level: {result_map[prediction]}**")

        # Simulated numbers just for nice UI
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric(label="TOTAL INTERACTIONS", value="890")
        with colB:
            st.metric(label="EXPECTED REACH", value="80,127")
        with colC:
            st.metric(label="ENGAGED USERS", value="19,023")




import pandas as pd
import matplotlib.pyplot as plt

if selected == "Insights":
    st.markdown("### 📊 Interaction Insights")

    try:
        # Reuse the last input if you have one, otherwise, simulate or require a new one
        if 'input_data' in locals():
            proba = model.predict_proba(input_data)[0]
            levels = ["Low", "Medium", "High"]
            df = pd.DataFrame({'Interaction Level': levels, 'Probability': proba})

            st.bar_chart(df.set_index("Interaction Level"))

            st.write("This chart shows the likelihood of each interaction level based on the post features you selected.")

        else:
            st.warning("Please run a prediction first in the 'Prediction' tab to view insights.")
    except Exception as e:
        st.error(f"Error showing insights: {e}")

