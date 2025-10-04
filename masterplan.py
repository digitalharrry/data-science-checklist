import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="📅 Data Science 52-Week Tracker", layout="centered")
st.title("📅 Data Science 52-Week Learning Plan Tracker")

st.markdown("""
Welcome to your personalized **Data Science Learning Tracker** 🎯  
Upload your `52_week_plan.csv` and track your daily & weekly progress easily.  
""")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader("📂 Upload your 52-week plan (CSV format)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Expected columns
    required_cols = ["Week", "Start_Date", "End_Date", "Task", "Status"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Your CSV must have the following columns: {required_cols}")
        st.stop()

    # Convert date columns
    df["Start_Date"] = pd.to_datetime(df["Start_Date"]).dt.date
    df["End_Date"] = pd.to_datetime(df["End_Date"]).dt.date

    # ----------------------------
    # Determine current week
    # ----------------------------
    today = datetime.today().date()
    current_week = df[(df["Start_Date"] <= today) & (df["End_Date"] >= today)]

    if current_week.empty:
        st.warning("✅ Either your plan hasn’t started yet or it’s completed!")
    else:
        week_no = current_week["Week"].values[0]
        st.subheader(f"📆 Current Week: **Week {week_no}**")
        st.write(f"🗓️ Date Range: {current_week['Start_Date'].values[0]} → {current_week['End_Date'].values[0]}")

        # Show current week tasks
        st.markdown("### 📘 This Week's Focus")
        st.info(current_week["Task"].values[0])

    # ----------------------------
    # Progress Section
    # ----------------------------
    st.markdown("---")
    st.subheader("📊 Progress Tracker")

    completed = df[df["Status"].str.lower() == "done"]
    progress = len(completed) / len(df)
    st.progress(progress)
    st.write(f"✅ **{len(completed)} / {len(df)} weeks completed** ({progress*100:.1f}%)")

    # ----------------------------
    # Update Progress (Mark Week Done)
    # ----------------------------
    st.markdown("### ✅ Mark Week as Done")
    selected_week = st.selectbox("Select Week to mark as complete:", df["Week"].tolist())
    if st.button("Mark as Done"):
        df.loc[df["Week"] == selected_week, "Status"] = "Done"
        df.to_csv("progress_saved.csv", index=False)
        st.success(f"Week {selected_week} marked as Done! Progress saved locally.")

    # ----------------------------
    # Show Full Plan
    # ----------------------------
    st.markdown("---")
    with st.expander("📅 View Full 52-Week Plan"):
        st.dataframe(df.style.applymap(
            lambda x: "background-color: #b6f5b6" if x == "Done" else "",
            subset=["Status"]
        ))

    # ----------------------------
    # Motivation Section
    # ----------------------------
    st.markdown("---")
    st.markdown("### 💡 Motivation Zone")
    quotes = [
        "Consistency beats intensity — keep showing up daily.",
        "Every data scientist started where you are today.",
        "Code. Learn. Repeat. You’re building something powerful.",
        "Don’t aim to be perfect. Aim to be better than yesterday."
    ]
    import random
    st.success(random.choice(quotes))

else:
    st.info("👆 Upload your CSV plan above to begin tracking progress.")
    st.markdown("""
    **CSV Format Example:**
    | Week | Start_Date | End_Date | Task | Status |
    |------|-------------|-----------|------|--------|
    | 1 | 2025-10-04 | 2025-10-10 | Python basics, loops, functions | Pending |
    | 2 | 2025-10-11 | 2025-10-17 | Numpy, Pandas, Matplotlib | Pending |
    | … | … | … | … | … |
    """)

