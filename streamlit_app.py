#Main app file 
import pandas as pd
import plotly.express as px
import streamlit as st
from utils.db_helper import get_summary_counts, get_all_students, get_student_interactions, get_recommendations, get_course_completion_rates, get_average_completion_rate

st.set_page_config(page_title="Personalized Learning Recommendation Engine",layout="wide")

st.title("📚 Personalized Learning Recommendation Engine")
st.subheader("Welcome to the smart education dashboard!")

students, courses, interactions = get_summary_counts()

st.markdown("### 📊 Overview")
col1, col2, col3 = st.columns(3)

col1.metric("Total Students", students)
col2.metric("Total Courses", courses)
col3.metric("Total interactions", interactions)

st.markdown("---")
st.header("🎓 Student Dashboard")

student_options = get_all_students()
student_dict = {f"{s_id} - {name}": s_id for s_id, name in student_options}

selected = st.selectbox("Select a student", list(student_dict.keys()))

if selected:
    s_id = student_dict[selected]
    data = get_student_interactions(s_id)

    if data:
        st.markdown(f"### 📘 Interations for {selected}")
        st.table(
            pd.DataFrame(data, columns=["Course Title", "Time Spent (min)", "Score", "Completed"])
        )
    else:
        st.info("No course interactions found for this student.")

    st.markdown("### 🎯 Recommended Courses")
    recommendations = get_recommendations(s_id)

    if recommendations:
        rec_df = pd.DataFrame(recommendations, columns=["Course ID", "Title", "Popularity"])
        st.dataframe(rec_df)
    else:
        st.info("No recommendations available for this student.")

st.markdown("---")
st.header("🏁 Course Completion Insights")

completion_df = get_course_completion_rates()

if not completion_df.empty:
    top_course = completion_df.sort_values(by='completion_percentage', ascending=False).iloc[0]
    bottom_course = completion_df.sort_values(by='completion_percentage', ascending=True).iloc[0]

    col1, col2 = st.columns(2)
    col1.write(f"🏆 **Top Completed Course:** {top_course['course_title']} ({top_course['completion_percentage']}%)")

    st.write(f"⚠️ **Lowest Completed Course:** {bottom_course['course_title']} ({bottom_course['completion_percentage']}%)")

    with st.expander("📋 See Full Course Completion Table"):
        st.dataframe(completion_df)
else:
    st.info("No course completion data available.")

