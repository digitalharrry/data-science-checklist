import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="📅 52-Week Data Science Plan", layout="centered")
st.title("📅 52-Week Data Science Learning Tracker")

st.markdown("""
Welcome to your **Data Science 52-Week Tracker** 🎯  
Upload your `52_week_plan.xlsx` and track your weekly learning journey across different domains.
""")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader("📂 Upload your Excel plan", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read the Excel file: {e}")
        st.stop()

    # Add a 'Status' column if it doesn't exist
    if "Status" not in df.columns:
        df["Status"] = "Pending"

    # Extract week number and start date (for logic)
    df["Week_Number"] = df["Week"].str.extract(r"Week\s*(\d+)", expand=False)
    df["Week_Number"] = pd.to_numeric(df["Week_Number"], errors='coerce')

    # Optional: use today's date to determine current week
    today = datetime.today().date()
    current_week_row = df[df["Status"] != "Done"].head(1)

    if not current_week_row.empty:
        current_week = current_week_row.iloc[0]
        st.subheader(f"📆 Current Week: **{current_week['Week']}**")

        # Display all sections for the current week
        st.markdown("### 📘 This Week's Focus")
        topics = ["Coding (Python / Libraries)", "Maths / Stats", "SQL / Excel / BI", "ML / DL / NLP", "Career / Projects / Notes"]
        for topic in topics:
            if topic in df.columns and pd.notna(current_week[topic]):
                st.markdown(f"**{topic}**: {current_week[topic]}")
    else:
        st.success("🎉 All weeks are marked as done! Great job!")

    # ----------------------------
    # Mark Week as Done
    # ----------------------------
    st.markdown("---")
    st.subheader("✅ Mark a Week as Done")
    week_options = df["Week"].tolist()
    selected_week = st.selectbox("Select Week:", week_options)

    if st.button("Mark as Done"):
        df.loc[df["Week"] == selected_week, "Status"] = "Done"
        df.to_excel("progress_updated.xlsx", index=False)
        st.success(f"✅ Week '{selected_week}' marked as Done! Saved to `progress_updated.xlsx`.")

    # ----------------------------
    # Progress Tracker
    # ----------------------------
    st.markdown("---")
    st.subheader("📊 Progress Overview")

    done_weeks = df[df["Status"].str.lower() == "done"]
    progress = len(done_weeks) / len(df)
    st.progress(progress)
    st.write(f"✅ **{len(done_weeks)} / {len(df)} weeks completed** ({progress*100:.1f}%)")

    # ----------------------------
    # View Full Plan
    # ----------------------------
    st.markdown("---")
    with st.expander("📅 View Full 52-Week Plan"):
        st.dataframe(df.style.applymap(
            lambda x: "background-color: #b6f5b6" if x == "Done" else "",
            subset=["Status"]
        ))

    # ----------------------------
    # Motivation Zone
    # ----------------------------
    st.markdown("---")
    st.markdown("### 💡 Motivation Zone")
    quotes = [
        "Keep pushing—consistency is your superpower!",
        "Every great data scientist was once a beginner.",
        "Focus on progress, not perfection.",
        "Small steps every day lead to big results.",
        "You’re building the future. One week at a time."
    ]
    st.success(random.choice(quotes))

else:
    st.info("👆 Upload your Excel file to get started.")
    st.markdown("""
**Expected Excel format:**

| Week | Coding (Python / Libraries) | Maths / Stats | SQL / Excel / BI | ML / DL / NLP | Career / Projects / Notes |
|------|------------------------------|----------------|-------------------|----------------|-----------------------------|
| Week 1 (Oct 4–10, 2025) | Python Basics: variables, loops | Arithmetic, Fractions | SQL Basics: SELECT, WHERE | | Practice problems |
| ... | ... | ... | ... | ... | ... |
""")
