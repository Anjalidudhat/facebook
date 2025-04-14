


import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
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

    # Move the prediction button INSIDE the Prediction block
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

        # Store the prediction in session state
        st.session_state.prediction = prediction

        st.success(f"🎯 **Predicted Interaction Level: {result_map[prediction]}**")

    

# ====== INSIGHTS PAGE ======
elif selected == "Insights":
    st.markdown("### 📊 Insights Based on Prediction")

    # Check if prediction exists in session state
    if "prediction" not in st.session_state:
        st.warning("Please make a prediction first on the Prediction tab.")
        st.stop()  # This stops execution of the rest of the code in this tab

    pred = st.session_state.prediction
    result_map = {0: "Low", 1: "Medium", 2: "High"}
    
    st.success(f"Currently showing insights for: {result_map[pred]} performance")

    # Dynamic visualization based on prediction value
    if pred == 0:  # Low performance
        values = [800, 40, 3, 1]  # Reach, Engagements, Comments, Shares
        color = '#ff7f7f'  # Light red
        tips = [
            "Try posting during evenings (6-9 PM)",
            "Use more emotional or inspirational content",
            "Include clear call-to-actions"
        ]
    elif pred == 1:  # Medium performance
        values = [5000, 150, 15, 10]
        color = '#7fb8ff'  # Light blue
        tips = [
            "Experiment with different content formats",
            "Analyze your top-performing posts for patterns",
            "Consider boosting high-potential posts"
        ]
    else:  # High performance
        values = [20000, 1000, 80, 50]
        color = '#7fff7f'  # Light green
        tips = [
            "Double down on what's working",
            "Create similar content with variations",
            "Consider creating a content series"
        ]

    # Metrics visualization
    st.markdown("### Performance Metrics")
    metrics = ["Reach", "Engagements", "Comments", "Shares"]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(metrics, values, color=color)
    ax.set_title(f"{result_map[pred]} Performance Metrics")
    ax.set_ylabel("Count")
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    st.pyplot(fig)

    # Improvement tips section
    st.markdown("### Improvement Tips")
    for i, tip in enumerate(tips, 1):
        st.write(f"{i}. {tip}")

    # Comparison with other levels
    st.markdown("### How You Compare")
    all_values = {
        "Low": [800, 40, 3, 1],
        "Medium": [5000, 150, 15, 10],
        "High": [20000, 1000, 80, 50]
    }
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    width = 0.25
    x = np.arange(len(metrics))
    
    for i, (level, vals) in enumerate(all_values.items()):
        offset = width * i
        ax2.bar(x + offset, vals, width, label=level,
               color='#ff7f7f' if level == "Low" else '#7fb8ff' if level == "Medium" else '#7fff7f')
    
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(metrics)
    ax2.legend(title="Performance Level")
    ax2.set_title("Comparison with All Performance Levels")
    ax2.set_ylabel("Count")
    
    st.pyplot(fig2)
